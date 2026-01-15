# =============================================================================
# FARKLI EMBEDDİNG MODELLERİNİ KARŞILAŞTIRMA UYGULAMASI
# Bu dosya, OpenAI, Cohere ve Hugging Face'in embedding modellerini
# yan yana karşılaştıran interaktif bir Streamlit uygulaması oluşturur.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# OpenAI: OpenAI'nin resmi Python kütüphanesi.
# GPT modelleri ve embedding API'leri için kullanılır.
from openai import OpenAI

# cohere: Cohere AI platformunun Python SDK'sı.
# NLP ve embedding modelleri için güçlü bir alternatif sunar.
import cohere

# streamlit: İnteraktif web uygulamaları oluşturmak için.
import streamlit as st

# requests: HTTP istekleri yapmak için standart Python kütüphanesi.
# Hugging Face Inference API'ye erişmek için kullanılır.
import requests

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
my_key_openai = os.getenv("openai_apikey")       # OpenAI API anahtarı
my_key_cohere = os.getenv("cohere_apikey")       # Cohere API anahtarı
my_key_hf = os.getenv("huggingface_access_token") # Hugging Face erişim tokeni

# -----------------------------------------------------------------------------
# API CLİENT'LARININ OLUŞTURULMASI
# -----------------------------------------------------------------------------

# OpenAI client'ı oluştur - embedding ve diğer API çağrıları için.
OpenAI_client = OpenAI(api_key=my_key_openai)

# Cohere client'ı oluştur - embedding ve NLP görevleri için.
Cohere_client = cohere.Client(api_key=my_key_cohere)

# -----------------------------------------------------------------------------
# ÖRNEK METİN
# -----------------------------------------------------------------------------

# Test için kullanılacak örnek metin - mevsimler hakkında bir soru.
# Bu metin, farklı modellerin aynı içeriği nasıl vektörleştirdiğini gösterecek.
sample_text ="Mevsimler neden oluşur? Dünya kendi etrafında döndüğü için mi?"

# -----------------------------------------------------------------------------
# EMBEDDİNG FONKSİYONLARI
# -----------------------------------------------------------------------------

def get_openai_embeddings(text):
    """
    OpenAI'nin text-embedding modelini kullanarak metin embedding'i oluşturur.
    
    OpenAI text-embedding-3-small modeli:
    - Boyut: 1536 (varsayılan)
    - Çok dilli destek
    - Yüksek kaliteli semantik temsil
    - Maliyet-etkin seçenek
    
    Args:
        text (str): Vektörleştirilecek metin
    
    Returns:
        list[float]: 1536 boyutlu embedding vektörü
    """
    # OpenAI embedding API'sini çağır
    response = OpenAI_client.embeddings.create(
        input=text,                          # Vektörleştirilecek metin
        model="text-embedding-3-small"       # Kullanılacak model
    )
    
    # Yanıttan embedding vektörünü çıkar
    # response.data[0].embedding: İlk (ve tek) girişin embedding'i
    embeddings = response.data[0].embedding
    
    return embeddings

def get_cohere_embeddings(text):
    """
    Cohere'in embed modelini kullanarak metin embedding'i oluşturur.
    
    Cohere embed-multilingual-v3.0 modeli:
    - Boyut: 1024
    - 100+ dil desteği (Türkçe dahil)
    - Arama ve sınıflandırma için optimize edilmiş
    - Farklı input_type seçenekleri mevcut
    
    Args:
        text (str): Vektörleştirilecek metin
    
    Returns:
        list[float]: 1024 boyutlu embedding vektörü
    """
    # Cohere embed API'sini çağır
    response=Cohere_client.embed(
        texts=[text],                        # Vektörleştirilecek metin(ler) - liste olmalı
        input_type="classification",         # Kullanım tipi: classification, search_document, search_query
        model="embed-multilingual-v3.0"      # Çok dilli embedding modeli
    )
    
    # İlk metnin embedding'ini döndür
    return response.embeddings[0]

def get_hf_embeddings(text):
    """
    Hugging Face Inference API kullanarak metin embedding'i oluşturur.
    
    sentence-transformers/all-MiniLM-L6-v2 modeli:
    - Boyut: 384
    - Hızlı ve hafif model
    - Sentence-level embedding'ler için optimize
    - Açık kaynak ve ücretsiz kullanılabilir
    
    Args:
        text (str): Vektörleştirilecek metin
    
    Returns:
        list[float]: 384 boyutlu embedding vektörü
    """
    # Kullanılacak model ID'si
    # Sentence Transformers ailesinden popüler bir model
    model_id = "sentence-transformers/all-MiniLM-L6-v2"

    # Hugging Face Inference API endpoint'i oluştur
    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
    
    # Yetkilendirme başlıkları
    headers = {"Authorization": f"Bearer {my_key_hf}"}

    # POST isteği gönder
    # wait_for_model: Model soğuksa yüklenmesini bekle
    response = requests.post(api_url, headers=headers, json={"inputs": text, "options":{"wait_for_model":True}})
    
    # JSON yanıtı döndür
    return response.json()

# -----------------------------------------------------------------------------
# STREAMLIT SAYFA YAPILANDIRMASI
# -----------------------------------------------------------------------------

# Sayfa başlığı ve düzenini ayarla
st.set_page_config("Embedding Modelleri Karşılaştırması", layout="wide")

# Ana başlık
st.title("Farklı Embedding Modelleriyle Vektörizasyon")

# Görsel ayırıcı
st.divider()

# -----------------------------------------------------------------------------
# SAYFA DÜZENİ
# -----------------------------------------------------------------------------

# Dört sütunlu düzen: giriş, OpenAI, Cohere, Hugging Face
col_input, col_openai, col_cohere, col_hf = st.columns([2,1,1,1])

# Giriş alanı
with col_input:
    # Metin giriş alanı oluştur
    text_input = st.text_area(label="Metin Girdisi", value=sample_text)
    
    # Gönder butonu
    submit_btn = st.button(label="Gönder")

    # Buton tıklandığında tüm embedding'leri hesapla
    if submit_btn:

        # ---------------------------------------------------------------------
        # OPENAİ EMBEDDİNG SONUÇLARI
        # ---------------------------------------------------------------------
        with col_openai:
            st.header("OpenAI")
            
            # OpenAI embedding'lerini al
            openai_embeddings = get_openai_embeddings(text=sample_text)
            
            # Vektör boyutunu göster
            st.success(f"Vektördeki Boyut Sayısı: {len(openai_embeddings)}")
            
            # Her bir embedding değerini göster
            for i, embedding in enumerate(openai_embeddings):
                col_openai.code(f"{i+1}: {embedding}")
        
        # ---------------------------------------------------------------------
        # COHERE EMBEDDİNG SONUÇLARI
        # ---------------------------------------------------------------------
        with col_cohere:
            st.header("Cohere")
            
            # Cohere embedding'lerini al
            cohere_embeddings = get_cohere_embeddings(text=sample_text)
            
            # Vektör boyutunu göster
            st.info(f"Vektördeki Boyut Sayısı: {len(cohere_embeddings)}")
            
            # Her bir embedding değerini göster
            for i, embedding in enumerate(cohere_embeddings):
                col_cohere.code(f"{i+1}: {embedding}")
        
        # ---------------------------------------------------------------------
        # HUGGİNG FACE EMBEDDİNG SONUÇLARI
        # ---------------------------------------------------------------------
        with col_hf:
            st.header("Hugging Face")
            
            # Hugging Face embedding'lerini al
            hf_embeddings = get_hf_embeddings(text=sample_text)
            
            # Vektör boyutunu göster
            st.warning(f"Vektördeki Boyut Sayısı: {len(hf_embeddings)}")
            
            # Her bir embedding değerini göster
            for i, embedding in enumerate(hf_embeddings):
                col_hf.code(f"{i+1}: {embedding}")

# =============================================================================
# EMBEDDİNG MODELLERİ KARŞILAŞTIRMASI:
# =============================================================================
#
# 1. BOYUT FARKLILIKLARI:
#    - OpenAI text-embedding-3-small: 1536 boyut
#    - Cohere embed-multilingual-v3.0: 1024 boyut
#    - Hugging Face all-MiniLM-L6-v2: 384 boyut
#
#    Daha yüksek boyut:
#    + Daha zengin semantik temsil
#    + Daha hassas benzerlik hesaplama
#    - Daha fazla bellek kullanımı
#    - Daha yavaş arama
#
# 2. MALİYET KARŞILAŞTIRMASI:
#    - OpenAI: Token başına ücretlendirme
#    - Cohere: Token/karakter başına ücretlendirme
#    - Hugging Face: Inference API (sınırlı ücretsiz, sonra ücretli)
#                    veya kendi sunucunuzda barındırma (ücretsiz ama altyapı gerek)
#
# 3. ÇOK DİLLİ DESTEK:
#    - OpenAI: Geniş dil desteği
#    - Cohere: 100+ dil (embed-multilingual ile)
#    - Hugging Face: Modele bağlı (MiniLM ağırlıklı İngilizce)
#
# 4. KULLANIM ÖNERİLERİ:
#    - Yüksek kalite & kolay entegrasyon: OpenAI
#    - Çok dilli projeler: Cohere embed-multilingual
#    - Düşük maliyet & açık kaynak: Hugging Face
#    - Özel/hassas veri: Kendi sunucunuzda Hugging Face modeli
#
# 5. EMBEDDİNG KULLANIM ALANLARI:
#    - Semantik arama
#    - Benzer içerik bulma
#    - Kümeleme (clustering)
#    - Sınıflandırma
#    - Öneri sistemleri
#    - RAG (Retrieval-Augmented Generation)
#
# =============================================================================