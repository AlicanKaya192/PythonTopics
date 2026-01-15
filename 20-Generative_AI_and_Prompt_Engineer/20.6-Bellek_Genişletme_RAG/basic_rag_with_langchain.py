# =============================================================================
# LANGCHAIN İLE TEMEL RAG (RETRIEVAL-AUGMENTED GENERATION) ÖRNEĞİ
# Bu dosya, LangChain kütüphanesi kullanarak web sayfalarından bilgi çekerek
# RAG sistemi oluşturur. Kullanıcı soruları, web sayfasından alınan bilgilerle
# zenginleştirilerek yanıtlanır.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# ChatGoogleGenerativeAI: Google'ın Gemini modeliyle etkileşim kurmak için kullanılır.
# Bu sınıf, Gemini Pro modelini kullanarak doğal dil işleme görevlerini gerçekleştirir.
from langchain_google_genai import ChatGoogleGenerativeAI

# WebBaseLoader: Web sayfalarının içeriğini yüklemek için kullanılır.
# URL'deki HTML içeriğini ayrıştırır ve metin olarak döndürür.
from langchain_community.document_loaders import WebBaseLoader

# FAISS: Facebook AI tarafından geliştirilen hızlı benzerlik arama kütüphanesi.
# Vektörleri verimli bir şekilde saklar ve benzerlik aramalarını hızlandırır.
from langchain_community.vectorstores.faiss import FAISS

# RecursiveCharacterTextSplitter: Uzun metinleri parçalara ayırmak için kullanılır.
# Metinleri karakter sayısına göre böler ve parça örtüşmesi sağlar.
from langchain.text_splitter import RecursiveCharacterTextSplitter

# CohereEmbeddings: Cohere'in embedding modelini kullanarak metinleri vektörlere dönüştürür.
# Çok dilli desteğiyle Türkçe metinler için de etkili sonuçlar verir.
from langchain_community.embeddings import CohereEmbeddings

# os: İşletim sistemi işlemleri için (ortam değişkenleri okuma vb.)
import os

# dotenv: .env dosyasından API anahtarlarını yüklemek için kullanılır.
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# ORTAM DEĞİŞKENLERİNİN YÜKLENMESİ
# -----------------------------------------------------------------------------

# .env dosyasındaki gizli değişkenleri (API anahtarları) ortam değişkeni olarak yükler.
load_dotenv()

# Google API anahtarını .env dosyasından al.
# Bu anahtar, Gemini modelini kullanmak için gereklidir.
my_key_google = os.getenv("google_apikey")

# Cohere API anahtarını .env dosyasından al.
# Bu anahtar, metin embedding'leri oluşturmak için gereklidir.
my_key_cohere = os.getenv("cohere_apikey")

# -----------------------------------------------------------------------------
# MODEL VE EMBEDDİNG YAPILANDIRMASI
# -----------------------------------------------------------------------------

# Google Gemini Pro modelini yapılandır.
# Bu model, kullanıcı sorularına yanıt üretmek için kullanılacak.
llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro")

# Cohere'in çok dilli embedding modelini yapılandır.
# embed-multilingual-v3.0 modeli, Türkçe dahil 100+ dili destekler.
# Bu model, metinleri 1024 boyutlu vektörlere dönüştürür.
embeddings = CohereEmbeddings(cohere_api_key=my_key_cohere, model="embed-multilingual-v3.0")

# -----------------------------------------------------------------------------
# YARDIMCI FONKSİYONLAR
# -----------------------------------------------------------------------------

def ask_gemini(prompt):
    """
    Gemini modeline doğrudan bir prompt gönderip yanıt alır.
    
    Bu fonksiyon, RAG sistemi tarafından oluşturulan zenginleştirilmiş
    prompt'u Gemini modeline iletir ve doğal dil yanıtı alır.
    
    Args:
        prompt (str): Modele gönderilecek metin (soru ve bağlam bilgisi içerir)
    
    Returns:
        str: Modelin ürettiği yanıt metni
    """
    # Gemini modeline prompt'u gönder ve yanıt al.
    # invoke() metodu, modeli çağırır ve AIMessage nesnesi döndürür.
    AI_Response = llm_gemini.invoke(prompt)

    # AIMessage nesnesinden sadece içerik (content) kısmını döndür.
    return AI_Response.content


def rag_with_url(target_url, prompt):
    """
    Verilen URL'den bilgi çekerek RAG tabanlı soru-cevap yapar.
    
    Bu fonksiyon, RAG pipeline'ının tamamını yönetir:
    1. Web sayfasını yükler
    2. Metni parçalara ayırır
    3. Vektör veritabanı oluşturur
    4. İlgili dokümanları getirir
    5. Bağlam ile zenginleştirilmiş yanıt üretir
    
    Args:
        target_url (str): Bilgi çekilecek web sayfasının URL'si
        prompt (str): Kullanıcının sorusu
    
    Returns:
        tuple: (AI_Response, relevant_documents)
            - AI_Response: Modelin ürettiği yanıt
            - relevant_documents: Bulunan ilgili doküman parçaları
    """
    # URL'deki web sayfasını yüklemek için loader oluştur.
    # WebBaseLoader, sayfanın HTML içeriğini alır ve metne dönüştürür.
    loader = WebBaseLoader(target_url)

    # Web sayfasını yükle ve Document nesnelerine dönüştür.
    # Her Document, sayfa içeriğini ve metadata bilgilerini içerir.
    raw_documents = loader.load()

    # Metin parçalayıcı oluştur.
    # RecursiveCharacterTextSplitter, metni akıllıca parçalara ayırır.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Her parça maksimum 1000 karakter olacak
        chunk_overlap=0,       # Parçalar arasında örtüşme olmayacak (0 karakter)
        length_function=len    # Uzunluk hesaplama fonksiyonu olarak Python'un len() fonksiyonu kullanılacak
    )

    # Yüklenen dokümanları parçalara ayır.
    # Bu adım, uzun metinlerin vektör veritabanında etkili bir şekilde aranmasını sağlar.
    splitted_documents = text_splitter.split_documents(raw_documents)

    # Parçalanmış dokümanlardan FAISS vektör veritabanı oluştur.
    # Bu adımda her parça için embedding vektörü hesaplanır ve saklanır.
    vectorstore = FAISS.from_documents(splitted_documents, embeddings)
    
    # Vektör veritabanından bir retriever (getirici) oluştur.
    # Retriever, sorguya en benzer dokümanları bulmak için kullanılır.
    retriever = vectorstore.as_retriever()

    # Kullanıcının sorusuna en benzer doküman parçalarını getir.
    # Varsayılan olarak en benzer 4 doküman döndürülür.
    relevant_documents = retriever.get_relevant_documents(prompt)

    # Bulunan dokümanların içeriklerini birleştirerek bağlam metni oluştur.
    context_data = ""

    # Her bir ilgili dokümanın içeriğini bağlam metnine ekle.
    for document in relevant_documents:
        context_data = context_data + " " + document.page_content

    # RAG prompt'unu oluştur.
    # Bu prompt, kullanıcının sorusunu ve ilgili bağlam bilgisini birleştirir.
    # Model, yalnızca verilen bağlam bilgisini kullanarak yanıt üretmek zorundadır.
    final_prompt = f"""Şöyle bir sorum var: {prompt}
    Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data} .
    Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla çıkma.
    """

    # Zenginleştirilmiş prompt'u Gemini modeline gönder ve yanıt al.
    AI_Response = ask_gemini(prompt=final_prompt)

    # Hem AI yanıtını hem de bulunan ilgili dokümanları döndür.
    # Bu sayede kullanıcı, yanıtın hangi kaynaklardan oluşturulduğunu görebilir.
    return AI_Response, relevant_documents

# -----------------------------------------------------------------------------
# TEST KISMI - ANA PROGRAM
# -----------------------------------------------------------------------------

# Test için kullanılacak URL.
# KPMG'nin üretken yapay zeka hakkındaki makalesini içeriyor.
test_url = "https://kpmg.com/tr/tr/home/gorusler/2023/12/uretken-yapay-zeka-uygulamalarinin-kurumsallasma-yaklasimi.html"

# Test sorusu: Yapay zeka uygulamalarının hayata geçirilmesindeki sorunları sorguluyoruz.
test_question = "Üretken yapay zeka uygulamalarının hayata geçirirken yaşanan temel sorunlar neler?"

# RAG fonksiyonunu çağırarak yanıt ve ilgili dokümanları al.
AI_Response, relevant_documents = rag_with_url(target_url=test_url, prompt=test_question)

# -----------------------------------------------------------------------------
# SONUÇLARIN YAZDIRMASI
# -----------------------------------------------------------------------------

# Soruyu yazdır
print(f"SORU: {test_question}")

# Görsel ayırıcı çizgi
print("-"*100)

# Yapay zeka yanıtını yazdır
print(f"YZ YANITI: {AI_Response}")

# Görsel ayırıcı çizgi
print("-"*100)

# Bulunan ilgili dokümanları yazdır.
# Bu, RAG sisteminin şeffaflığını sağlar - kullanıcı hangi kaynaklardan yanıt üretildiğini görebilir.
for doc in relevant_documents:
    print(doc.page_content)
    print("*"*100)