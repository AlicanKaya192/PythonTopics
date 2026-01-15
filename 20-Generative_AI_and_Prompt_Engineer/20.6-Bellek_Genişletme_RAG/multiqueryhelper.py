# =============================================================================
# MULTI-QUERY RAG YARDIMCI MODÜLÜ
# Bu dosya, Multi-Query RAG tekniğini uygulamak için gerekli tüm fonksiyonları içerir.
# Sorgu çeşitlendirme, doküman getirme, de-duplikasyon, reranking ve RAG işlemlerini yönetir.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# ChatGoogleGenerativeAI: Google'ın Gemini modeliyle etkileşim sağlar.
# Doğal dil üretimi ve RAG yanıtları için kullanılır.
from langchain_google_genai import ChatGoogleGenerativeAI

# ChatOpenAI: OpenAI'nin GPT modellerini kullanmak için.
# Multi-query oluşturmada GPT-4 kullanılır (daha iyi sorgu çeşitlendirmesi için).
from langchain_openai import ChatOpenAI

# OpenAIEmbeddings: Metinleri embedding vektörlerine dönüştürür.
# Semantik arama için temel bileşendir.
from langchain_openai import OpenAIEmbeddings

# WebBaseLoader: Web sayfalarından içerik çekmek için kullanılır.
from langchain_community.document_loaders import WebBaseLoader

# PyPDFLoader: PDF dosyalarından metin çıkarmak için kullanılır.
# Bu projede şu an kullanılmasa da, ileride PDF desteği için hazır.
from langchain_community.document_loaders import PyPDFLoader

# FAISS: Facebook AI tarafından geliştirilen hızlı vektör benzerlik arama kütüphanesi.
from langchain_community.vectorstores import FAISS

# RecursiveCharacterTextSplitter: Metinleri akıllıca parçalara ayırır.
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Document: LangChain'in temel doküman sınıfı.
from langchain_core.documents import Document

# cohere: Cohere AI platformu - reranking için kullanılır.
# Cross-encoder modeli ile dokümanları yeniden sıralar.
import cohere

# os: İşletim sistemi işlemleri için
import os

# dotenv: .env dosyasından API anahtarlarını güvenli şekilde yükler.
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# ORTAM DEĞİŞKENLERİNİN YÜKLENMESİ
# -----------------------------------------------------------------------------

# .env dosyasındaki gizli değişkenleri ortam değişkeni olarak yükle.
load_dotenv()

# API anahtarlarını ortam değişkenlerinden al.
my_key_openai = os.getenv("openai_apikey")   # OpenAI için
my_key_google = os.getenv("google_apikey")    # Google Gemini için
my_key_cohere = os.getenv("cohere_apikey")    # Cohere reranking için

# -----------------------------------------------------------------------------
# MODEL VE CLIENT YAPILANDIRMALARI
# -----------------------------------------------------------------------------

# Google Gemini Pro modelini yapılandır - RAG yanıtları için kullanılacak.
llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro")

# OpenAI GPT-4 modelini yapılandır - sorgu çeşitlendirme için kullanılacak.
# GPT-4, farklı bakış açılarından sorgu üretmede çok başarılı.
llm_openai = ChatOpenAI(api_key=my_key_openai, model="gpt-4-0125-preview")

# OpenAI embedding modelini yapılandır.
embeddings = OpenAIEmbeddings(api_key=my_key_openai)

# Cohere client'ı yapılandır - reranking için kullanılacak.
cohere_client = cohere.Client(api_key=my_key_cohere)

# -----------------------------------------------------------------------------
# ÇOKLU SORGU OLUŞTURMA FONKSİYONU
# -----------------------------------------------------------------------------

def generate_multi_query(original_prompt):
    """
    Tek bir kullanıcı sorusundan birden fazla alternatif sorgu üretir.
    
    Bu fonksiyon, Multi-Query RAG'ın kalbini oluşturur:
    - LLM'den, aynı sorunun farklı ifadelerini üretmesini ister
    - Bu sayede vektör aramasının kapsamı genişletilir
    - Kelime mismatch problemi azaltılır
    
    Args:
        original_prompt (str): Kullanıcının orijinal sorusu
    
    Returns:
        list[str]: Orijinal soru + alternatif sorgular listesi
    
    Örnek:
        Giriş: "Yapay zeka tehlikeleri nelerdir?"
        Çıkış: [
            "Yapay zeka tehlikeleri nelerdir?",  # Orijinal
            "AI'ın potansiyel riskleri neler?",
            "Makine öğrenmesi zararları nelerdir?",
            "Otonom sistemlerin olumsuz etkileri?"
        ]
    """
    # Multi-query prompt şablonu.
    # GPT-4'ten, sorgunun 3 farklı versiyonunu üretmesini istiyoruz.
    multiquery_prompt = f"""Sen bir yapay zeka asistanısın.

    Bir vektör veri tabanından, kullanıcı sorusuna en fazla benzerlik gösteren dokümanların getirilmesi için, sana verilen kullanıcı girdisinin 3 farklı versiyonunu yazmakla görevlisin.

    Bunu yaparken amacın ise vektörleri karşılaştırırken kullanılan mesafe ölçümlerinin bazı sınırlılıklarını aşmak için, verilen soruyla ilgili birden çok bakış açısı geliştirerek kullanıcıya yardımcı olmak.

    Bu yazacağın alternatif soruları ayrı ayrı satırlarda olacak şekilde yaz.
    Alternatif soruları yazarken bunların 1, 2, 3 gibi numaralandırmalar koyma.

    Kullanıcı girdisi şöyle: {original_prompt}"""

    # GPT-4'ten alternatif sorguları ürettir.
    generated_queries = llm_openai.invoke(input=multiquery_prompt)

    # Yanıtı satırlara ayır (her satır bir sorgu).
    temp_list = generated_queries.content.strip().split("\n")

    # Orijinal soruyu listenin başına ekle.
    # Bu sayede orijinal soru da aramaya dahil edilir.
    query_list = [original_prompt]
    query_list.extend(temp_list)

    return query_list

# -----------------------------------------------------------------------------
# İLGİLİ DOKÜMANLARI GETİRME FONKSİYONU
# -----------------------------------------------------------------------------

def get_relevant_documents(target_url, prompt):
    """
    Verilen URL'den doküman yükler ve prompt'a en alakalı olanları döndürür.
    
    Bu fonksiyon, RAG pipeline'ının temel arama bileşenidir:
    1. Web sayfasını yükler
    2. Metni parçalara ayırır
    3. FAISS ile vektör araması yapar
    4. En alakalı dokümanları döndürür
    
    Args:
        target_url (str): Web sayfası URL'si
        prompt (str): Arama sorgusu
    
    Returns:
        list[Document]: En alakalı doküman parçaları
    """
    # Web sayfası loader'ı oluştur
    loader = WebBaseLoader(target_url)

    # Sayfayı yükle
    raw_documents = loader.load()

    # Metin parçalayıcı oluştur
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # Her parça maksimum 1000 karakter
        chunk_overlap=0,       # Parçalar arası örtüşme yok
        length_function=len    # Uzunluk hesaplama fonksiyonu
    )

    # Dokümanları parçalara ayır
    splitted_documents = text_splitter.split_documents(raw_documents)

    # Özelleştirilmiş dokümanlar listesi
    custom_documents = []

    # Her parçaya benzersiz ID ve metadata ekle
    for i, raw_doc in enumerate(splitted_documents):

        new_doc = Document(
            page_content=raw_doc.page_content,
            metadata = {
                "source": raw_doc.metadata["source"],
                "title" : raw_doc.metadata["title"],
                "description" : raw_doc.metadata["description"],
                "language" : raw_doc.metadata["language"],
                "doc_id" : i  # Benzersiz doküman ID'si
            }
        )

        custom_documents.append(new_doc)

    # FAISS vektör deposu oluştur
    vectorstore = FAISS.from_documents(custom_documents, embeddings)
    
    # Retriever oluştur
    retriever = vectorstore.as_retriever()

    # En alakalı dokümanları getir
    relevant_documents = retriever.get_relevant_documents(prompt)

    return relevant_documents

# -----------------------------------------------------------------------------
# RAG ÇALIŞTIRMA FONKSİYONU
# -----------------------------------------------------------------------------

def run_rag(relevant_documents, prompt):
    """
    RAG pipeline'ını çalıştırarak yanıt üretir.
    
    Args:
        relevant_documents (list[Document]): Bağlam olarak kullanılacak dokümanlar
        prompt (str): Kullanıcının orijinal sorusu
    
    Returns:
        str: LLM'in ürettiği yanıt
    """
    # Bağlam metnini oluştur
    context_data = ""

    # Tüm dokümanların içeriğini birleştir
    for document in relevant_documents:
        context_data = context_data + " " + document.page_content

    # RAG prompt'u oluştur
    final_prompt = f"""Şöyle bir sorum var: {prompt}
    Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data} .
    Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla çıkma.
    """

    # Gemini'den yanıt al
    AI_Response = llm_gemini.invoke(input=final_prompt)

    return AI_Response.content

# -----------------------------------------------------------------------------
# URL İLE RAG FONKSİYONU (TAM PİPELİNE)
# -----------------------------------------------------------------------------

def rag_with_url(target_url, prompt):
    """
    URL'den doküman yükleyip RAG ile yanıt üreten tam pipeline fonksiyonu.
    
    Bu fonksiyon, get_relevant_documents ve run_rag fonksiyonlarını birleştirir.
    Tek fonksiyon çağrısıyla tam RAG işlemi gerçekleştirir.
    
    Args:
        target_url (str): Web sayfası URL'si
        prompt (str): Kullanıcı sorusu
    
    Returns:
        tuple: (AI_Response, relevant_documents)
    """
    # Web sayfasını yükle
    loader = WebBaseLoader(target_url)
    raw_documents = loader.load()

    # Metni parçala
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )
    splitted_documents = text_splitter.split_documents(raw_documents)

    # Özelleştirilmiş dokümanlar oluştur
    custom_documents = []

    for i, raw_doc in enumerate(splitted_documents):
        new_doc = Document(
            page_content=raw_doc.page_content,
            metadata = {
                "source": raw_doc.metadata["source"],
                "title" : raw_doc.metadata["title"],
                "description" : raw_doc.metadata["description"],
                "language" : raw_doc.metadata["language"],
                "doc_id" : i
            }
        )
        custom_documents.append(new_doc)

    # Vektör deposu ve retriever oluştur
    vectorstore = FAISS.from_documents(custom_documents, embeddings)
    retriever = vectorstore.as_retriever()

    # Alakalı dokümanları getir
    relevant_documents = retriever.get_relevant_documents(prompt)

    # Bağlam oluştur
    context_data = ""
    for document in relevant_documents:
        context_data = context_data + " " + document.page_content

    # RAG prompt'u oluştur ve yanıt al
    final_prompt = f"""Şöyle bir sorum var: {prompt}
    Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data} .
    Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla çıkma.
    """

    AI_Response = llm_gemini.invoke(input=final_prompt)

    return AI_Response.content, relevant_documents

# -----------------------------------------------------------------------------
# BENZERSİZ DOKÜMANLARI ELDE ETME FONKSİYONU (DE-DUPLIKASYON)
# -----------------------------------------------------------------------------

def get_unique_documents(retrieved_documents):
    """
    Tekrarlayan dokümanları kaldırarak benzersiz dokümanları döndürür.
    
    Multi-Query aramada aynı doküman birden fazla sorguyla bulunabilir.
    Bu fonksiyon, doc_id'ye göre tekrarları filtreler.
    
    Args:
        retrieved_documents (list[Document]): Tüm getirilen dokümanlar (tekrarlı olabilir)
    
    Returns:
        list[Document]: Benzersiz dokümanlar listesi
    
    Örnek:
        Giriş: [Doc1, Doc2, Doc1, Doc3, Doc2]  (5 doküman, 3 benzersiz)
        Çıkış: [Doc1, Doc2, Doc3]  (3 benzersiz doküman)
    """
    # doc_id -> Document eşlemesi için sözlük
    unique_docs = {}

    # Her dokümanda döngü
    for doc in retrieved_documents:
        doc_id = doc.metadata['doc_id']

        # Eğer bu ID daha önce görülmediyse, sözlüğe ekle
        if doc_id not in unique_docs:
            unique_docs[doc_id] = doc

    # Sözlükteki değerleri (benzersiz dokümanları) liste olarak döndür
    return list(unique_docs.values())

# -----------------------------------------------------------------------------
# YENİDEN SIRALAMA (RERANKING) FONKSİYONU
# -----------------------------------------------------------------------------

def get_reranked_documents(documents, query, document_count=4):
    """
    Cohere'in rerank modelini kullanarak dokümanları yeniden sıralar.
    
    Reranking, semantik aramadan daha hassas bir sıralama sağlar:
    - Cross-encoder modeli kullanılır
    - Her doküman-soru çifti birlikte değerlendirilir
    - Daha doğru alaka skorları elde edilir
    
    Args:
        documents (list[Document]): Sıralanacak dokümanlar
        query (str): Orijinal kullanıcı sorusu
        document_count (int): Döndürülecek maksimum doküman sayısı
    
    Returns:
        list[Document]: Yeniden sıralanmış en alakalı dokümanlar
    
    Not:
        Cohere rerank-multilingual-v2.0 modeli kullanılır.
        Bu model, Türkçe dahil 100+ dili destekler.
    """
    # Doküman içeriklerini metin listesine dönüştür
    # Cohere API, Document nesneleri yerine string listesi bekler
    document_contents = []

    for doc in documents:
        document_contents.append(doc.page_content)

    # Cohere rerank API'sini çağır
    reranked_documents = cohere_client.rerank(
        model="rerank-multilingual-v2.0",  # Çok dilli rerank modeli
        query=query,                        # Sıralama kriteri olarak kullanıcı sorusu
        documents=document_contents,        # Sıralanacak dokümanlar
        top_n=document_count                # Döndürülecek doküman sayısı
    )

    # Yeniden sıralanmış dokümanları orijinal Document nesneleri olarak döndür
    reranked_documents_list = []

    # Cohere, rerank sonuçlarında orijinal listedeki indeksi döndürür
    # Bu indeksi kullanarak orijinal Document nesnesini alıyoruz
    # for reranked_doc in reranked_documents:
    #     reranked_documents_list.append(reranked_doc.document['text'])
    
    for reranked_doc in reranked_documents:
        # reranked_doc.index: Bu dokümanın orijinal listedeki konumu
        reranked_documents_list.append(documents[reranked_doc.index])

    return reranked_documents_list

# =============================================================================
# MULTI-QUERY RAG TEKNİK DETAYLARI:
# =============================================================================
#
# 1. SORGU ÇEŞİTLENDİRME MEKANİZMASI:
#    - GPT-4, verilen soruyu analiz eder
#    - Farklı kelimeler ve cümle yapıları kullanarak varyasyonlar üretir
#    - Her varyasyon, farklı embedding vektörü oluşturur
#    - Bu sayede arama kapsamı genişler
#
# 2. RERANKING VS BİRİNCİ AŞAMA ARAMA:
#    Bi-encoder (İlk arama):
#    - Soru ve doküman ayrı ayrı encode edilir
#    - Hızlı ama daha az hassas
#    
#    Cross-encoder (Reranking):
#    - Soru ve doküman birlikte encode edilir
#    - Yavaş ama çok daha hassas
#    - İlk aramadan gelen sonuçları iyileştirir
#
# 3. PİPELİNE AKIŞI:
#    Kullanıcı Sorusu
#         ↓
#    Multi-Query Oluşturma (GPT-4)
#         ↓
#    Her sorgu için FAISS araması
#         ↓
#    Sonuçları birleştir
#         ↓
#    De-duplikasyon
#         ↓
#    Reranking (Cohere)
#         ↓
#    RAG yanıt üretimi (Gemini)
#
# =============================================================================
