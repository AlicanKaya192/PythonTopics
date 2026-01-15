# ==============================================================================
# VidChat: RAG Yardımcı Modülü
# ==============================================================================
# Bu modül, video transkriptleri üzerinde RAG (Retrieval-Augmented Generation)
# işlemlerini gerçekleştirir.
#
# RAG Nedir ve Neden Kullanıyoruz?
# --------------------------------
# Normal bir LLM (Gemini, GPT vb.) sadece eğitildiği bilgileri bilir.
# Örneğin, dün yüklenen bir YouTube videosunun içeriğini bilemez.
# 
# RAG bu sorunu şöyle çözer:
# 1. Harici kaynaktan (video transkripti) bilgiyi al
# 2. Kullanıcının sorusuyla en alakalı kısımları bul (semantik arama)
# 3. Bu bilgileri LLM'e "bağlam" (context) olarak ver
# 4. LLM, bu bağlamı kullanarak soruyu yanıtlasın
#
# Böylece LLM, eğitiminde olmayan güncel içerikler hakkında da
# doğru ve güvenilir bilgiler verebilir! Bu teknik, şirket içi dökümanlar,
# güncel haberler veya özel veri setleri için de kullanılabilir.
# ==============================================================================

# LangChain bileşenlerini içe aktar
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini modeli wrapper'ı
from langchain_openai import OpenAIEmbeddings  # Metin vektörleştirme için OpenAI modeli
from langchain_community.vectorstores import FAISS  # Facebook'un hızlı vektör arama kütüphanesi
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Akıllı metin bölücü
import os
from dotenv import load_dotenv

# .env dosyasından API anahtarlarını yükle
# Güvenlik kuralı: API anahtarları ASLA kodun içinde yazılmaz!
load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_google = os.getenv("google_apikey")

# Google Gemini modelini başlat
# Gemini Pro: Google'ın güçlü dil modeli, Türkçe desteği oldukça iyi
# Bu model, RAG'dan gelen bağlamı kullanarak soruları yanıtlayacak
llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro")

# OpenAI Embeddings modelini başlat
# Embedding Nedir? Metinleri sayısal vektörlere dönüştüren bir işlemdir.
# Bu vektörler sayesinde "anlamsal benzerlik" hesaplayabiliriz.
# Örneğin "araba" ve "otomobil" vektörleri birbirine yakın olur,
# böylece kullanıcı "araba" diye sorsa bile "otomobil" içeren kısımlar bulunur.
embeddings = OpenAIEmbeddings(api_key=my_key_openai)


# ==============================================================================
# Fonksiyon 1: Basit Gemini Sorgusu
# ==============================================================================
# Bu fonksiyon RAG olmadan çalışır, sadece modelin kendi bilgisini kullanır.
# Karşılaştırma amacıyla veya RAG gerektirmeyen basit sorular için kullanılabilir.
# ==============================================================================
def ask_gemini(prompt):
    """
    Google Gemini modeline direkt soru sorar.
    
    Parametreler:
    ------------
    prompt : str
        Modele gönderilecek soru veya talimat
    
    Döndürür:
    --------
    str : Modelin metin yanıtı
    """
    AI_Response = llm_gemini.invoke(prompt)

    return AI_Response.content


# ==============================================================================
# Fonksiyon 2: Video Transkripti Üzerinde RAG
# ==============================================================================
# Bu fonksiyon VidChat uygulamasının kalbidir. Video transkriptini alır,
# kullanıcının sorusuna en alakalı kısımları bulur ve bu bilgilerle
# zenginleştirilmiş bir yanıt üretir.
#
# RAG Adımları:
# 1. BÖLME (Chunking): Uzun transkripti küçük parçalara böl
# 2. VEKTÖRLEŞTIRME (Embedding): Her parçayı sayısal vektöre dönüştür
# 3. İNDEKSLEME (FAISS): Vektörleri hızlı arama için depola
# 4. ARAMA (Retrieval): Kullanıcının sorusuna en benzer parçaları bul
# 5. ÜRETME (Generation): Bulunan parçaları bağlam olarak kullanarak yanıt üret
# ==============================================================================
def rag_with_video_transcript(transcript_docs, prompt):
    """
    Video transkripti üzerinde RAG uygulayarak soruyu yanıtlar.
    
    Bu fonksiyon, uzun video içeriklerini parçalar, en alakalı kısımları
    bulur ve bu bilgilerle zenginleştirilmiş bir yanıt üretir.
    
    Parametreler:
    ------------
    transcript_docs : list
        Video transkriptini içeren LangChain Document listesi
        Her document page_content (metin) ve metadata (kaynak bilgisi) içerir
    
    prompt : str
        Kullanıcının sorusu
    
    Döndürür:
    --------
    tuple : (AI_Response, relevant_documents)
        - AI_Response: Modelin metin yanıtı
        - relevant_documents: Yanıtta kullanılan kaynak parçaları (şeffaflık için)
    """
    
    # ADIM 1: Transkripti parçalara böl (Chunking)
    # Neden bölüyoruz?
    # - LLM'lerin context limiti var (Gemini Pro: 32K token)
    # - Küçük parçalar daha iyi arama sonucu verir
    # - İlgisiz bilgiler yanıtı kirletmez
    #
    # chunk_size=1000: Her parça maksimum 1000 karakter
    # chunk_overlap=0: Parçalar arasında örtüşme yok (istersen 100-200 yapılabilir)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )

    # Dökümanları parçalara böl
    splitted_documents = text_splitter.split_documents(transcript_docs)

    # ADIM 2-3: Vektör veritabanı oluştur (Embedding + Indexing)
    # from_documents: Her parçayı vektörleştirir ve FAISS'e ekler
    # FAISS: Facebook AI Research'ün geliştirdiği çok hızlı benzerlik arama kütüphanesi
    # Milyonlarca vektör arasında milisaniyeler içinde arama yapabilir!
    vectorstore = FAISS.from_documents(splitted_documents, embeddings)
    
    # Retriever: Vektör veritabanında arama yapan arayüz
    # Varsayılan olarak en alakalı 4 parçayı getirir (k=4)
    retriever = vectorstore.as_retriever()

    # ADIM 4: Soruya en alakalı dökümanları bul (Retrieval)
    # Bu adım, kullanıcının sorusunu da vektöre çevirir ve
    # en yakın (en benzer) parçaları bulur
    relevant_documents = retriever.get_relevant_documents(prompt)

    # Bulunan tüm parçaları birleştir - bu bizim "bağlamımız" olacak
    context_data = ""

    for document in relevant_documents:
        context_data = context_data + " " + document.page_content

    # ADIM 5: Zenginleştirilmiş prompt oluştur ve yanıt al (Generation)
    # Bu prompt yapısı çok önemli - modele şunları söylüyoruz:
    # 1. Kullanıcının sorusu ne
    # 2. Hangi bilgiler mevcut (bağlam)
    # 3. SADECE bu bilgileri kullan (halüsinasyonu önlemek için kritik!)
    final_prompt = f"""Şöyle bir sorum var: {prompt}
    Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data} .
    Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla çıkma.
    """

    # Gemini'den yanıt al
    AI_Response = ask_gemini(final_prompt)

    # Hem yanıtı hem de kaynak dökümanları döndür
    # Kaynak dökümanlar şeffaflık için önemli - kullanıcı nereden bilgi alındığını görebilir
    return AI_Response, relevant_documents