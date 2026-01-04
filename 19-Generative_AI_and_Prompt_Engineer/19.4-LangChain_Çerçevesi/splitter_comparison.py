# ==============================================================================
# LangChain Text Splitter Karşılaştırma Uygulaması
# ==============================================================================
# Bu script, LangChain kütüphanesinde bulunan farklı metin bölme (text splitting)
# stratejilerini karşılaştırmak için tasarlanmış bir Streamlit web uygulamasıdır.
#
# Peki neden metinleri bölmemiz gerekiyor?
# -----------------------------------------
# Büyük dil modelleri (LLM) ile çalışırken, genellikle uzun metinler veya belgeler
# işlememiz gerekir. Ancak bu modellerin bir "bağlam penceresi" (context window)
# limiti vardır. Yani aynı anda işleyebilecekleri metin miktarı sınırlıdır.
# Bu yüzden uzun metinleri "chunk" (kesit/parça) denilen daha küçük parçalara
# bölmemiz gerekir. Bu bölme işlemi, RAG (Retrieval-Augmented Generation) 
# sistemlerinin temel taşlarından biridir.
#
# Bu uygulamada 3 farklı bölme stratejisini karşılaştırıyoruz:
# 1. Character Splitter: Metni basitçe karakter sayısına göre böler
# 2. Recursive Character Splitter: Daha akıllı bir yaklaşımla paragraf, cümle gibi
#    doğal bölme noktalarını kullanarak böler
# 3. Semantic Splitter: Anlam bazlı bölme yapar. En gelişmiş yöntemdir çünkü
#    cümlelerin birbirleriyle olan anlamsal yakınlığına bakar.
# ==============================================================================

# Gerekli kütüphanelerin içe aktarılması
# Google'ın Gemini modelini LangChain üzerinden kullanmak için gerekli sınıf
from langchain_google_genai import ChatGoogleGenerativeAI
# OpenAI'ın embedding (metin vektörleştirme) özelliğini kullanmak için
from langchain_openai import OpenAIEmbeddings
# Web sayfalarından içerik çekmek için kullanacağımız loader
from langchain_community.document_loaders import WebBaseLoader
# Metin bölme işlemleri için kullanacağımız splitter sınıfları
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
# Semantik (anlam bazlı) bölme için deneysel modül - dikkat: henüz stabil değil
from langchain_experimental.text_splitter import SemanticChunker
# Ortam değişkenlerini yönetmek için gerekli modüller
import os
from dotenv import load_dotenv

# .env dosyasındaki API anahtarlarını yükle
# Bu dosyada openai_apikey ve google_apikey gibi değerler saklanmalı
load_dotenv()

# Ortam değişkenlerinden API anahtarlarını al
# Güvenlik açısından API anahtarlarını asla kodun içine yazmayız!
my_key_openai = os.getenv("openai_apikey")
my_key_google = os.getenv("google_apikey")

# Google Gemini modelini LangChain wrapper'ı ile başlat
# Not: Bu örnekte model aslında kullanılmıyor, sadece tanımlanmış
# convert_system_message_to_human: Gemini'de sistem mesajı desteği olmadığından
# bu parametre sistem mesajlarını insan mesajına dönüştürür
llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro", convert_system_message_to_human=True)

# OpenAI Embeddings modelini başlat
# Embedding nedir? Metinleri sayısal vektörlere dönüştüren bir işlemdir.
# Bu vektörler sayesinde metin benzerliği hesaplayabilir, semantik arama yapabiliriz.
# SemanticChunker bu embedding'leri kullanarak anlamca benzer cümleleri gruplar.
embeddings = OpenAIEmbeddings(api_key=my_key_openai)


def split_content(splitter_type, target_url="", chunk_size=500, chunk_overlap=0):
    """
    Verilen URL'deki içeriği belirtilen stratejiye göre böler.
    
    Bu fonksiyon, web'den bir sayfa çeker ve istenen bölme yöntemini
    uygulayarak parçalanmış dökümanları döndürür.
    
    Parametreler:
    ------------
    splitter_type : str
        Kullanılacak bölme stratejisi. "Character", "Recursive" veya "Semantic"
    
    target_url : str
        İçeriği çekilecek web sayfasının adresi
    
    chunk_size : int
        Her bir parçanın maksimum karakter sayısı (Semantic için geçerli değil)
    
    chunk_overlap : int
        Ardışık parçalar arasındaki örtüşme miktarı (karakter sayısı)
        Örtüşme neden önemli? Bir cümle iki parçanın tam ortasına denk gelirse,
        bağlamı kaybetmemek için biraz örtüşme yararlı olabilir.
    
    Döndürür:
    --------
    list : Bölünmüş döküman parçalarının listesi
    """
    
    # WebBaseLoader ile hedef URL'den içeriği çek
    # Bu loader, sayfanın HTML içeriğini alır ve temizler
    loader = WebBaseLoader(target_url)
    
    # Dökümanı yükle - bu bir liste döner çünkü bazı loader'lar birden fazla döküman döner
    raw_documents = loader.load()

    # Hangi splitter kullanılacağını belirle
    if splitter_type == "Character":
        # CharacterTextSplitter: En basit yöntem
        # Sadece karakter sayısına göre böler, paragraf veya cümle sınırlarına bakmaz
        # Avantajı: Hızlı ve tahmin edilebilir
        # Dezavantajı: Kelimelerin ortasından bile bölebilir!
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,      # Her parçanın maksimum büyüklüğü
            chunk_overlap=chunk_overlap, # Parçalar arası örtüşme
            length_function=len          # Uzunluk hesaplama fonksiyonu
        )

    elif splitter_type == "Recursive":
        # RecursiveCharacterTextSplitter: Daha akıllı bir yöntem
        # Önce paragraflardan (\n\n), sonra satırlardan (\n), sonra cümlelerden (. ) böler
        # Eğer hala chunk_size'ı aşıyorsa, daha küçük birimlere iner
        # Böylece anlamlı kesim noktaları bulunmaya çalışılır
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    elif splitter_type == "Semantic":
        # SemanticChunker: En gelişmiş yöntem
        # Embedding kullanarak cümlelerin anlamsal benzerliğini ölçer
        # Birbirine yakın anlamlı cümleler aynı chunk'ta tutulur
        # chunk_size parametresi burada kullanılmaz - tamamen anlam bazlı
        # Not: Bu yöntem daha yavaş çünkü her cümle için embedding hesaplanır
        text_splitter = SemanticChunker(embeddings)

    # Seçilen splitter ile dökümanları böl ve döndür
    splitted_documents = text_splitter.split_documents(raw_documents)

    return splitted_documents


# ==============================================================================
# Streamlit Web Arayüzü
# ==============================================================================
# Streamlit, Python ile hızlıca web arayüzü oluşturmamızı sağlayan harika bir araç.
# Veri bilimi ve makine öğrenmesi projelerinde sıkça kullanılır.
# ==============================================================================

import streamlit as st

# Sayfa konfigürasyonu - tarayıcı sekmesindeki başlık ve sayfa düzeni
st.set_page_config(page_title="Splitter Karşılaştırması", layout="wide")

# Ana başlık
st.title("Splitter Karşılaştırması")
st.divider()

# Kullanıcıdan işlenecek web adresini al
# Bu adresteki içerik çekilip farklı yöntemlerle bölünecek
target_url = st.text_input(label="İşlenecek Web Adresini Giriniz:")
st.divider()

# Kesit (chunk) büyüklüğü ayarı
# Bu değer, Character ve Recursive splitter'lar için her parçanın maksimum boyutunu belirler
# Küçük değerler: Daha fazla parça, daha hassas arama ama daha fazla işlem
# Büyük değerler: Daha az parça, daha hızlı ama bağlam kaybı riski
chunk_size = st.slider(
    label="Kesit büyüklüğünü belirleyiniz:",
    min_value=100, 
    max_value=2000, 
    value=1000,  # Varsayılan değer
    step=100, 
    key="url_chunk_size"
)
st.divider()

# Çakışma (overlap) büyüklüğü ayarı
# Parçalar arasındaki örtüşme miktarı
# Bu sayede bir cümle iki parçanın sınırına denk gelirse bile kaybolmaz
chunk_overlap = st.slider(
    label="Çakışma büyüklüğünü belirleyiniz:",
    min_value=0, 
    max_value=1000, 
    value=0,  # Varsayılan: örtüşme yok
    step=100, 
    key="url_chunk_overlap"
)
st.divider()

# Bölme işlemini başlatan düğme
submit_btn = st.button(label="Başla", key="url_button")
st.divider()

# Düğmeye basıldığında sonuçları göster
if submit_btn:
    # Üç sütun oluştur - her splitter türü için bir sütun
    # Böylece sonuçları yan yana karşılaştırabiliriz
    col_character, col_recursive, col_semantic = st.columns(3)

    # --- Character Splitter Sonuçları ---
    with col_character:
        splitted_documents = split_content(
            splitter_type="Character", 
            target_url=target_url, 
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        st.subheader("Character Splitter")
        # Her parçayı yeşil bir kutu içinde göster
        for splitted_document in splitted_documents:
            st.success(splitted_document.page_content)

    # --- Recursive Character Splitter Sonuçları ---
    with col_recursive:
        splitted_documents = split_content(
            splitter_type="Recursive", 
            target_url=target_url, 
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        st.subheader("Recursive Character Splitter")
        # Her parçayı mavi bir kutu içinde göster
        for splitted_document in splitted_documents:
            st.info(splitted_document.page_content)

    # --- Semantic Splitter Sonuçları ---
    with col_semantic:
        splitted_documents = split_content(
            splitter_type="Semantic", 
            target_url=target_url, 
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        st.subheader("Semantic Splitter")
        # Her parçayı sarı bir kutu içinde göster
        for splitted_document in splitted_documents:
            st.warning(splitted_document.page_content)
