# =============================================================================
# HİBRİT ARAMA (HYBRID SEARCH) YARDIMCI MODÜLÜ
# Bu dosya, hibrit arama uygulaması için gerekli fonksiyonları içerir.
# BM25, FAISS ve EnsembleRetriever kullanarak farklı arama yöntemlerini uygular.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# FAISS: Facebook AI tarafından geliştirilen hızlı vektör benzerlik arama kütüphanesi.
# Milyonlarca vektör üzerinde milisaniyeler içinde arama yapabilir.
from langchain_community.vectorstores import FAISS

# OpenAIEmbeddings: OpenAI'nin text-embedding modelini kullanarak metinleri vektörlere dönüştürür.
from langchain_openai import OpenAIEmbeddings

# BM25Retriever: Best Matching 25 algoritmasını uygulayan retriever.
# Klasik bilgi getirme yöntemlerinden biri olup, TF-IDF'in geliştirilmiş versiyonudur.
from langchain_community.retrievers import BM25Retriever

# EnsembleRetriever: Birden fazla retriever'ı ağırlıklı olarak birleştiren sınıf.
# Hibrit arama stratejilerini uygulamak için kullanılır.
from langchain.retrievers import EnsembleRetriever

# RecursiveCharacterTextSplitter: Uzun metinleri parçalara ayırır.
# Karakter sayısına göre böler ve doğal bölme noktalarını korur.
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Document: LangChain'in temel doküman sınıfı.
# Sayfa içeriği (page_content) ve metadata bilgilerini içerir.
from langchain_core.documents import Document

# WebBaseLoader: Web sayfalarından içerik yüklemek için kullanılır.
# HTML'i parse eder ve metin içeriğini çıkarır.
from langchain_community.document_loaders import WebBaseLoader

# os: İşletim sistemi işlemleri için (ortam değişkenleri vb.)
import os

# dotenv: .env dosyasından API anahtarlarını güvenli şekilde yükler.
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# ORTAM DEĞİŞKENLERİNİN YÜKLENMESİ
# -----------------------------------------------------------------------------

# .env dosyasındaki gizli değişkenleri ortam değişkeni olarak yükle.
load_dotenv()

# OpenAI API anahtarını ortam değişkenlerinden al.
my_key_openai = os.getenv("openai_apikey")

# -----------------------------------------------------------------------------
# GLOBAL YAPILANDIRMALAR
# -----------------------------------------------------------------------------

# OpenAI embedding modelini yapılandır.
# Bu model, metinleri yüksek boyutlu vektörlere dönüştürür.
embeddings = OpenAIEmbeddings(api_key=my_key_openai)

# -----------------------------------------------------------------------------
# ÖRNEK VERİ SETİ (TEST İÇİN)
# -----------------------------------------------------------------------------

# Örnek doküman listesi - elma ve meyve temalı metinler.
# Bu liste, modülün test edilmesi için kullanılabilir.
doc_list = [
    "I like apples",                                                    # Elma sevgisi
    "I like oranges",                                                   # Portakal sevgisi
    "Apples and oranges are fruits",                                    # Meyve tanımı
    "I like computers by Apple",                                        # Apple bilgisayar (farklı anlam)
    "I love fruit juice but particularly apples as apples are the best",# Meyve suyu tercihi
    "Air Cana serves apple juice",                                      # Havayolu servisi
    "Beetlejuice is a terrible movie",                                  # Film referansı (alakasız)
    "That country literally is a banana republic",                      # Politik terim
    "The iPhone made its manufacturer rich",                            # Apple ürünü
    "I dislike apples",                                                 # Elma sevmeme
]

# -----------------------------------------------------------------------------
# DOKÜMAN YÜKLEME VE PARÇALAMA FONKSİYONU
# -----------------------------------------------------------------------------

def load_and_split_documents(target_url):
    """
    Verilen URL'den web sayfasını yükler ve parçalara ayırır.
    
    Bu fonksiyon:
    1. Web sayfasını indirir
    2. HTML içeriğini parse eder
    3. Metni 1000 karakterlik parçalara böler
    4. Her parçaya benzersiz bir ID atar
    
    Args:
        target_url (str): İçerik yüklenecek web sayfasının URL'si
    
    Returns:
        list[Document]: Her biri benzersiz ID'ye sahip Document nesneleri listesi
    """
    # Web sayfası yükleyici oluştur
    loader = WebBaseLoader(target_url)

    # Web sayfasını yükle ve Document listesine dönüştür
    raw_documents = loader.load()

    # Metin parçalayıcı oluştur
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # Her parça maksimum 1000 karakter
        chunk_overlap=0,       # Parçalar arasında örtüşme yok
        length_function=len    # Uzunluk ölçümü için Python len() fonksiyonu
    )

    # Dokümanları parçalara ayır
    splitted_documents = text_splitter.split_documents(raw_documents)

    # Özelleştirilmiş dokümanlar listesi
    custom_documents = []

    # Her parçaya benzersiz ID ekleyerek yeni Document nesneleri oluştur
    for i, raw_doc in enumerate(splitted_documents):

        # Yeni Document nesnesi oluştur
        new_doc = Document(
            page_content=raw_doc.page_content,  # Orijinal içeriği koru
            metadata = {
                "source": raw_doc.metadata["source"],           # Kaynak URL
                "title" : raw_doc.metadata["title"],            # Sayfa başlığı
                "description" : raw_doc.metadata["description"],# Sayfa açıklaması
                "language" : raw_doc.metadata["language"],      # Dil bilgisi
                "doc_id" : i                                    # Benzersiz doküman ID'si
            }
        )

        # Listeye ekle
        custom_documents.append(new_doc)

    return custom_documents

# -----------------------------------------------------------------------------
# BM25 İLE ARAMA FONKSİYONU
# -----------------------------------------------------------------------------

def get_relevant_documents_with_bm25(documents, query):
    """
    BM25 algoritması kullanarak anahtar kelime bazlı arama yapar.
    
    BM25 (Best Matching 25):
    - TF-IDF'in geliştirilmiş versiyonudur
    - Doküman uzunluğunu normalize eder
    - Term frequency saturationu uygular
    - Klasik bilgi getirmede standart algoritma
    
    Args:
        documents (list[Document]): Arama yapılacak doküman listesi
        query (str): Arama sorgusu
    
    Returns:
        tuple: (relevant_documents, bm25_retriever)
            - relevant_documents: Bulunan en alakalı dokümanlar
            - bm25_retriever: Hibrit aramada kullanılmak üzere retriever nesnesi
    """
    # BM25 retriever oluştur
    bm25_retriever = BM25Retriever.from_documents(documents=documents)
    
    # Döndürülecek doküman sayısını 4 olarak ayarla
    bm25_retriever.k = 4

    # Sorguya en uygun dokümanları getir
    bm25_relevant_documents = bm25_retriever.get_relevant_documents(query=query)

    # Hem dokümanları hem de retriever'ı döndür
    return bm25_relevant_documents, bm25_retriever

# -----------------------------------------------------------------------------
# FAISS İLE SEMANTİK ARAMA FONKSİYONU
# -----------------------------------------------------------------------------

def get_relevant_documents_with_FAISS(documents, query):
    """
    FAISS kullanarak vektör tabanlı semantik arama yapar.
    
    FAISS (Facebook AI Similarity Search):
    - Yüksek boyutlu vektörlerde hızlı benzerlik araması
    - Embedding vektörleri arasında kosinüs benzerliği hesaplar
    - Anlamsal olarak benzer içerikleri bulur
    
    Args:
        documents (list[Document]): Arama yapılacak doküman listesi
        query (str): Arama sorgusu
    
    Returns:
        tuple: (relevant_documents, faiss_retriever)
            - relevant_documents: Semantik olarak en benzer dokümanlar
            - faiss_retriever: Hibrit aramada kullanılmak üzere retriever nesnesi
    """
    # Dokümanlardan FAISS vektör deposu oluştur
    # Bu adımda her doküman için embedding vektörü hesaplanır
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Retriever oluştur ve döndürülecek doküman sayısını 4 olarak ayarla
    faiss_retriever = vectorstore.as_retriever(search_kwargs = {"k":4})

    # Sorguya semantik olarak en benzer dokümanları getir
    FAISS_relevant_documents = faiss_retriever.get_relevant_documents(query)

    # Hem dokümanları hem de retriever'ı döndür
    return FAISS_relevant_documents, faiss_retriever

# -----------------------------------------------------------------------------
# HİBRİT ARAMA FONKSİYONU
# -----------------------------------------------------------------------------

def get_relevant_documents_for_hybrid_search(query, retriever1, retriever2, weight1=0.5, weight2=0.5):
    """
    İki farklı retriever'ı ağırlıklı olarak birleştirerek hibrit arama yapar.
    
    Hibrit arama avantajları:
    - Anahtar kelime eşleşmelerini yakalar (BM25)
    - Anlamsal benzerlikleri yakalar (FAISS)
    - Her iki yöntemin zayıf noktalarını telafi eder
    
    Args:
        query (str): Arama sorgusu
        retriever1: İlk retriever (tipik olarak BM25)
        retriever2: İkinci retriever (tipik olarak FAISS)
        weight1 (float): İlk retriever'ın ağırlığı (0-1 arası)
        weight2 (float): İkinci retriever'ın ağırlığı (0-1 arası)
    
    Returns:
        list[Document]: Ağırlıklı birleştirilmiş sonuçlar
    
    Not:
        weight1 + weight2 = 1 olmalıdır.
        Örnek: weight1=0.7, weight2=0.3 ise BM25'e daha fazla ağırlık verilir.
    """
    # EnsembleRetriever oluştur - birden fazla retriever'ı birleştirir
    ensemble_retriever = EnsembleRetriever(
                                retrievers=[retriever1, retriever2],  # Retriever listesi
                                weights=[weight1, weight2]            # Ağırlık listesi
                            )

    # Hibrit arama yap ve sonuçları döndür
    hybrid_relevant_documents = ensemble_retriever.get_relevant_documents(query)

    return hybrid_relevant_documents

# =============================================================================
# ENSEMBLE RETRİEVER ÇALIŞMA PRENSİBİ:
# =============================================================================
# 1. Her retriever bağımsız olarak sorguyu çalıştırır
# 2. Her retriever'dan dönen sonuçlar toplanır
# 3. Sonuçlar, belirlenen ağırlıklara göre sıralanır
# 4. Tekrarlanan dokümanlar birleştirilir
# 5. En yüksek puanlı dokümanlar döndürülür
#
# Örnek:
# - BM25 sonuçları: [Doc1: 0.8, Doc3: 0.7, Doc5: 0.6]
# - FAISS sonuçları: [Doc2: 0.9, Doc1: 0.85, Doc4: 0.7]
# - weight1=0.5, weight2=0.5 ile:
#   Doc1 puanı = 0.5*0.8 + 0.5*0.85 = 0.825
#   Doc2 puanı = 0.5*0 + 0.5*0.9 = 0.45
#   vb.
# =============================================================================