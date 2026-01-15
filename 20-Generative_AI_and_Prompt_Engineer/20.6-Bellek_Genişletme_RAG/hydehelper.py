# =============================================================================
# HyDE (HYPOTHETICAL DOCUMENT EMBEDDINGS) YARDIMCI MODÜLÜ
# Bu dosya, HyDE tekniğini uygulamak için gerekli fonksiyonları içerir.
# Kurgusal doküman oluşturma, vektör araması ve RAG pipeline'ını yönetir.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# RecursiveCharacterTextSplitter: Metinleri akıllı bir şekilde parçalara ayırır.
# Paragraf, cümle ve kelime sınırlarını koruyarak böler.
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Chroma: Açık kaynaklı vektör veritabanı.
# Embedding vektörlerini saklar ve benzerlik araması yapar.
from langchain_community.vectorstores.chroma import Chroma

# WebBaseLoader: Web sayfalarından içerik çekmek için kullanılır.
from langchain_community.document_loaders import WebBaseLoader

# Document: LangChain'in temel doküman sınıfı.
# İçerik ve metadata bilgilerini birlikte saklar.
from langchain_core.documents import Document

# ChatGoogleGenerativeAI: Google Gemini modeli ile etkileşim sağlar.
from langchain_google_genai import ChatGoogleGenerativeAI

# ChatOpenAI: OpenAI GPT modelleri ile etkileşim sağlar.
from langchain_openai import ChatOpenAI

# OpenAIEmbeddings: Metinleri embedding vektörlerine dönüştürür.
from langchain_openai import OpenAIEmbeddings

# os: İşletim sistemi işlemleri için
import os

# dotenv: .env dosyasından API anahtarlarını yükler.
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# ORTAM DEĞİŞKENLERİNİN YÜKLENMESİ
# -----------------------------------------------------------------------------

# .env dosyasındaki gizli değişkenleri yükle.
load_dotenv()

# API anahtarlarını ortam değişkenlerinden al.
my_key_openai = os.getenv("openai_apikey")
my_key_google = my_key_google = os.getenv("google_apikey")

# -----------------------------------------------------------------------------
# MODEL VE EMBEDDİNG YAPILANDIRMALARI
# -----------------------------------------------------------------------------

# OpenAI embedding modelini yapılandır.
# Bu model, metinleri yüksek boyutlu vektörlere dönüştürür.
embeddings = OpenAIEmbeddings(api_key=my_key_openai)

# Google Gemini Pro modelini yapılandır.
# Bu model, doğal dil üretimi ve RAG yanıtları için kullanılır.
llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro")

# OpenAI GPT-4 modelini yapılandır.
# Alternatif LLM olarak kullanılabilir (şu an kullanılmıyor).
llm_openai = ChatOpenAI(api_key=my_key_openai, model="gpt-4-0125-preview")

# -----------------------------------------------------------------------------
# DOKÜMAN YÜKLEME VE PARÇALAMA FONKSİYONU
# -----------------------------------------------------------------------------

def load_and_split_documents(target_url):
    """
    Web sayfasını yükler ve işlenebilir parçalara ayırır.
    
    Bu fonksiyon, RAG pipeline'ının ilk adımını oluşturur:
    1. Web sayfasını indir
    2. HTML'i parse et
    3. Metni chunk'lara böl
    4. Her chunk'a benzersiz ID ata
    
    Args:
        target_url (str): Yüklenecek web sayfasının URL'si
    
    Returns:
        list[Document]: İşlenmiş ve ID'lenmiş doküman parçaları listesi
    """
    # Web sayfası loader'ı oluştur
    loader = WebBaseLoader(target_url)

    # Web sayfasını yükle (HTML parse edilir, metin çıkarılır)
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

    # Her parçaya benzersiz metadata ekle
    for i, raw_doc in enumerate(splitted_documents):

        # Yeni Document nesnesi oluştur
        new_doc = Document(
            page_content=raw_doc.page_content,  # Metin içeriği
            metadata = {
                "source": raw_doc.metadata["source"],           # Kaynak URL
                "title" : raw_doc.metadata["title"],            # Sayfa başlığı
                "description" : raw_doc.metadata["description"],# Meta açıklama
                "language" : raw_doc.metadata["language"],      # Dil kodu
                "doc_id" : i                                    # Benzersiz ID
            }
        )

        custom_documents.append(new_doc)

    return custom_documents

# -----------------------------------------------------------------------------
# İLGİLİ DOKÜMANLARI GETİRME FONKSİYONU
# -----------------------------------------------------------------------------

def get_relevant_documents(prompt, documents):
    """
    Verilen prompt ile en alakalı dokümanları getirir.
    
    Bu fonksiyon, MMR (Maximum Marginal Relevance) algoritması kullanarak
    hem alakalı hem de çeşitli sonuçlar döndürür.
    
    Args:
        prompt (str): Arama sorgusu (kullanıcı sorusu veya HyDE yanıtı)
        documents (list[Document]): Arama yapılacak doküman havuzu
    
    Returns:
        list[Document]: En alakalı doküman parçaları
    """
    # ChromaDB vektör deposu oluştur
    # Her doküman için embedding hesaplanır ve saklanır
    vectorstore = Chroma.from_documents(documents, embeddings)

    # MMR tipi retriever oluştur
    # MMR, hem alaka hem de çeşitlilik sağlar
    retriever = vectorstore.as_retriever(search_type="mmr")

    # Sorguya en uygun dokümanları getir
    relevant_documents = retriever.get_relevant_documents(prompt)

    return relevant_documents

# -----------------------------------------------------------------------------
# RAG ÇALIŞTIRMA FONKSİYONU
# -----------------------------------------------------------------------------

def run_rag(relevant_documents, prompt):
    """
    RAG pipeline'ını çalıştırarak yanıt üretir.
    
    Bu fonksiyon:
    1. İlgili dokümanları birleştirerek bağlam oluşturur
    2. Bağlamı ve soruyu içeren prompt hazırlar
    3. LLM'den yanıt alır
    
    Args:
        relevant_documents (list[Document]): Bağlam olarak kullanılacak dokümanlar
        prompt (str): Kullanıcının orijinal sorusu
    
    Returns:
        str: LLM'in ürettiği yanıt
    """
    # Bağlam metnini oluştur
    context_data = ""

    # Tüm ilgili dokümanların içeriğini birleştir
    for document in relevant_documents:
        context_data = context_data + " " + document.page_content

    # RAG prompt'u oluştur
    # Model, yalnızca verilen bağlam bilgisini kullanmaya zorlanır
    final_prompt = f"""Şöyle bir sorum var: {prompt}
    Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data} .
    Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla çıkma.
    """

    # Gemini modeline prompt'u gönder ve yanıt al
    AI_Response = llm_gemini.invoke(input=final_prompt)

    # Yanıt içeriğini döndür
    return AI_Response.content

# -----------------------------------------------------------------------------
# KURGUSAL (HİPOTETİK) DOKÜMAN OLUŞTURMA FONKSİYONU - HyDE'NİN KALBİ
# -----------------------------------------------------------------------------

def generate_hypothetical_document(prompt):
    """
    HyDE tekniğinin temel fonksiyonu: Kurgusal yanıt üretir.
    
    Bu fonksiyon, kullanıcı sorusuna varsayımsal bir cevap üretir.
    Bu cevap, gerçek bilgi içermek zorunda değildir - amacı,
    arama için daha iyi bir sorgu oluşturmaktır.
    
    HyDE Mantığı:
    - Sorular ve cevaplar farklı semantik uzayda bulunur
    - "Yapay zeka nedir?" sorusu ile "Yapay zeka, bilgisayarların..." cevabı
      farklı embedding'lere sahiptir
    - Kurgusal cevap, gerçek cevaplara daha yakın embedding'e sahip olur
    - Bu sayede vektör araması daha etkili çalışır
    
    Args:
        prompt (str): Kullanıcının orijinal sorusu
    
    Returns:
        str: LLM tarafından üretilen kurgusal paragraf
    
    Örnek:
        Giriş: "Yapay zeka tehlikeleri nelerdir?"
        Çıkış: "Yapay zeka teknolojileri, işsizlik, gizlilik ihlalleri ve
                özerk silah sistemleri gibi çeşitli riskler taşımaktadır.
                Ayrıca algoritmik önyargı ve veri güvenliği konuları da
                önemli endişe kaynakları arasındadır."
    """
    # HyDE prompt'u oluştur
    # Modelden kısa bir paragraf yazmasını iste
    HyDE_Prompt = f"""Kullanıcının sorusunu cevaplamak için kısa bir paragraf yaz.
    Kullanıcı Sorusu: {prompt}
    """

    # Gemini modeline prompt'u gönder
    hypothetical_answer = llm_gemini.invoke(input=HyDE_Prompt)

    # Üretilen kurgusal yanıtı döndür
    return hypothetical_answer.content

# =============================================================================
# HyDE TEKNİĞİ TEKNİK DETAYLARI:
# =============================================================================
#
# 1. SEMANTİK BOŞLUK PROBLEMİ:
#    - Soru: "Mevsimler neden oluşur?"
#    - Doküman: "Dünya'nın eksen eğikliği, güneş ışınlarının farklı açılarla
#                düşmesine neden olarak mevsimleri oluşturur."
#    - Bu iki metin, anlamsal olarak ilişkili olsa da farklı yapıdadır.
#
# 2. HyDE ÇÖZÜMÜ:
#    - Kurgusal Yanıt: "Mevsimler, Dünya'nın güneş etrafındaki yörüngesinde
#                       hareket ederken eksen eğikliğinden kaynaklanır."
#    - Bu kurgusal yanıt, gerçek dokümana daha benzer yapıdadır.
#
# 3. MATEMATİKSEL AÇIKLAMA:
#    - Soru embedding'i: Q
#    - Doküman embedding'i: D
#    - Kurgusal yanıt embedding'i: H
#    - Tipik olarak: sim(H, D) > sim(Q, D)
#    - Bu nedenle H ile arama, daha alakalı D'ler bulur.
#
# 4. SINIRLAMALAR:
#    - LLM halüsinasyon yapabilir (yanlış bilgi üretebilir)
#    - Ek maliyet ve gecikme ekler
#    - Çok spesifik teknik sorularda etkisiz olabilir
#
# =============================================================================