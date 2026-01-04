# ==============================================================================
# RAG Yardımcı Modülü (RAG Helper)
# ==============================================================================
# Bu modül, Retrieval-Augmented Generation (RAG) işlemleri için gerekli
# fonksiyonları içerir.
#
# RAG Mimarisi:
# 1. Yükle (Load): Veri kaynağından dokümanları al
# 2. Böl (Split): Büyük dokümanları küçük parçalara ayır
# 3. Vektörleştir (Embed): Parçaları sayısal vektörlere dönüştür
# 4. Depola (Store): Vektörleri bir veritabanına kaydet
# 5. Sorgula (Retrieve): Kullanıcı sorusuna en benzer parçaları bul
# 6. Üret (Generate): Bulunan parçaları context olarak kullanarak yanıt üret
# ==============================================================================

# LangChain bileşenlerini içe aktar
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini modeli
from langchain_openai import OpenAIEmbeddings  # OpenAI embedding modeli
from langchain_community.document_loaders import WebBaseLoader  # Web içerik yükleyici
from langchain_community.document_loaders import PyPDFLoader  # PDF yükleyici
from langchain_community.vectorstores import FAISS  # Facebook'un vektör veritabanı
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Akıllı metin bölücü
from langchain_community.embeddings import CohereEmbeddings  # Cohere embedding (alternatif)
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings  # HF embedding
import os
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

# API anahtarlarını al
my_key_openai = os.getenv("openai_apikey")
my_key_google = os.getenv("google_apikey")
my_key_cohere = os.getenv("cohere_apikey")
my_key_hf = os.getenv("huggingface_access_token")

# Google Gemini modelini başlat - yanıt üretmek için kullanacağız
llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro")

# Embedding modeli seçimi - 3 farklı seçenek var:
# 1. OpenAI: En kaliteli ama ücretli
# embeddings = OpenAIEmbeddings(api_key=my_key_openai)

# 2. Cohere: Çok dilli destek için iyi
# embeddings = CohereEmbeddings(cohere_api_key=my_key_cohere, model="embed-multilingual-v3.0")

# 3. HuggingFace: Ücretsiz ve açık kaynak
# sentence-transformers/all-MiniLM-l6-v2: Hızlı ve etkili bir model
embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=my_key_hf,
    model_name="sentence-transformers/all-MiniLM-l6-v2"
)


def ask_gemini(prompt):
    """
    Basit Gemini sorgusu - RAG olmadan.
    Karşılaştırma için kullanılır.
    """
    AI_Response = llm_gemini.invoke(prompt)
    return AI_Response.content


def rag_with_url(target_url, prompt):
    """
    URL tabanlı RAG - Web sayfasından bilgi çekerek yanıt üretir.
    
    Adımlar:
    1. WebBaseLoader ile URL'den içerik çek
    2. RecursiveCharacterTextSplitter ile parçalara böl
    3. FAISS ile vektör veritabanı oluştur
    4. Kullanıcı sorusuna en benzer parçaları bul
    5. Bu parçaları context olarak kullanarak Gemini'den yanıt al
    """
    
    # 1. URL'den içeriği yükle
    loader = WebBaseLoader(target_url)
    raw_documents = loader.load()

    # 2. Dokümanları parçalara böl
    # chunk_size=1000: Her parça max 1000 karakter
    # chunk_overlap=0: Parçalar arasında örtüşme yok
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )
    splitted_documents = text_splitter.split_documents(raw_documents)

    # 3-4. Vektör veritabanı oluştur ve retriever ayarla
    # FAISS: Facebook'un geliştirdiği hızlı benzerlik arama kütüphanesi
    vectorstore = FAISS.from_documents(splitted_documents, embeddings)
    retriever = vectorstore.as_retriever()

    # 5. Kullanıcı sorusuna benzer dokümanları bul
    relevant_documents = retriever.get_relevant_documents(prompt)

    # Bulunan dokümanları birleştir
    context_data = ""
    for document in relevant_documents:
        context_data = context_data + " " + document.page_content

    # 6. Zenginleştirilmiş prompt oluştur ve yanıt al
    final_prompt = f"""Şöyle bir sorum var: {prompt}
    Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data} .
    Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla çıkma.
    """

    AI_Response = llm_gemini.invoke(final_prompt)
    return AI_Response.content


def rag_with_pdf(filepath, prompt):
    """
    PDF tabanlı RAG - PDF dosyasından bilgi çekerek yanıt üretir.
    URL tabanlı RAG ile aynı mantık, sadece kaynak farklı.
    
    Not: İlgili dokümanları da döndürür (şeffaflık için)
    """
    
    # PDF'i yükle - her sayfa ayrı bir doküman olur
    loader = PyPDFLoader(filepath)
    raw_documents = loader.load()

    # Dokümanları parçala
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )
    splitted_documents = text_splitter.split_documents(raw_documents)

    # Vektör veritabanı oluştur
    vectorstore = FAISS.from_documents(splitted_documents, embeddings)
    retriever = vectorstore.as_retriever()

    # İlgili dokümanları bul
    relevant_documents = retriever.get_relevant_documents(prompt)

    # Context oluştur
    context_data = ""
    for document in relevant_documents:
        context_data = context_data + " " + document.page_content

    # Yanıt üret
    final_prompt = f"""Şöyle bir sorum var: {prompt}
    Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data} .
    Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla çıkma.
    """

    AI_Response = llm_gemini.invoke(final_prompt)
    return AI_Response.content, relevant_documents