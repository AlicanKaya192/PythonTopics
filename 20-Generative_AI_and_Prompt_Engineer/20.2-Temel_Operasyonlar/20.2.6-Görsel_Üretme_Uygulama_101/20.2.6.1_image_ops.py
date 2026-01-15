# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 6: Görsel Üretme Uygulama 101
# 19.2.6.1 - AI ile Görsel Üretme ve Manipülasyon
# ============================================================================
# Bu dosya, farklı AI görsel üretme API'leri kullanarak:
# - Metinden görsel oluşturma (Text-to-Image)
# - Görsel varyasyonları oluşturma (Image Variation)
# - Farklı modeller ile karşılaştırmalı üretim
# işlemlerini Streamlit arayüzü ile göstermektedir.
#
# GÖRSEL ÜRETME TEKNOLOJİLERİ
# ===========================
# 1. DALL-E (OpenAI):
#    - GPT mimarisi tabanlı görsel üretim modeli
#    - Yüksek kaliteli, gerçekçi görseller
#    - Prompt'u otomatik iyileştirme (revised_prompt)
#    - DALL-E 2: Varyasyon ve düzenleme desteği
#    - DALL-E 3: Daha yüksek kalite, sadece üretim
#
# 2. Stable Diffusion (Stability AI):
#    - Açık kaynak diffusion modeli
#    - Yüksek özelleştirme imkanı
#    - Negative prompt desteği
#    - Çeşitli boyut ve kalite seçenekleri
#    - Topluluk tarafından geliştirilen modeller (LoRA, vb.)
#
# DİFÜZYON MODELLERİ NASIL ÇALIŞIR?
# ==================================
# Diffusion modelleri iki aşamadan oluşur:
# 1. Forward Process (Gürültü Ekleme):
#    - Orijinal görsel → Noise (rastgele gürültü)
#    - Kademeli olarak görsel tamamen gürültüye dönüşür
#
# 2. Reverse Process (Gürültü Çıkarma):
#    - Noise → Orijinal görsel
#    - Model, metin promptuna göre gürültüyü temizler
#    - Her adımda daha net bir görsel ortaya çıkar
#
# Bu süreç "denoising" (gürültü giderme) olarak adlandırılır.
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# OpenAI: DALL-E API erişimi için
# streamlit: Web arayüzü oluşturmak için
# requests: HTTP istekleri (görsel indirme ve Stability AI API)
# BytesIO: Binary veriyi bellek içinde dosya gibi işlemek için
# base64: Base64 kodlanmış görsel verisi çözümlemek için
# os: Ortam değişkenlerine erişim
# dotenv: .env dosyasından API anahtarlarını okumak için

from openai import OpenAI
import streamlit as st
import requests
from io import BytesIO
import base64
import os
from dotenv import load_dotenv


# ============================================================================
# 2. API YAPILANDIRMASI
# ============================================================================
# İki farklı API için anahtar yükleme:
# - OpenAI: DALL-E görsel üretimi için
# - Stability AI: Stable Diffusion XL için
#
# .env dosyası örnek formatı:
# openai_apikey=sk-xxxxxxxxxxxxxxxxxxxxx
# stabilityai_apikey=sk-xxxxxxxxxxxxxxxxxxxxx
#
# API anahtarları almak için:
# - OpenAI: https://platform.openai.com/api-keys
# - Stability AI: https://platform.stability.ai/account/keys

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_stabilityai = os.getenv("stabilityai_apikey")


# ============================================================================
# 3. OPENAI İSTEMCİSİ OLUŞTURMA
# ============================================================================
# DALL-E API çağrıları için OpenAI istemcisi

client = OpenAI(
    api_key=my_key_openai
)


# ============================================================================
# 4. DALL-E 3 İLE GÖRSEL ÜRETME FONKSİYONU
# ============================================================================
# Metinden görsel oluşturma (Text-to-Image) işlemi
#
# client.images.generate() PARAMETRELER:
# --------------------------------------
# model: Kullanılacak DALL-E modeli
#   - "dall-e-3": En güncel ve kaliteli model
#   - "dall-e-2": Önceki versiyon (varyasyon desteği var)
#
# size: Görsel boyutu
#   - DALL-E 3: "1024x1024", "1792x1024", "1024x1792"
#   - DALL-E 2: "256x256", "512x512", "1024x1024"
#
# quality: Görsel kalitesi (sadece DALL-E 3)
#   - "standard": Standart kalite (daha hızlı, daha ucuz)
#   - "hd": Yüksek detay (daha yavaş, daha pahalı)
#
# n: Üretilecek görsel sayısı
#   - DALL-E 3: Sadece 1 (API kısıtlaması)
#   - DALL-E 2: 1-10 arası
#
# response_format: Yanıt formatı
#   - "url": Görsel URL'si döner (1 saat geçerli)
#   - "b64_json": Base64 kodlanmış görsel verisi
#
# prompt: Görsel açıklaması (metin)
#
# DALL-E 3 ÖZELLİĞİ - REVISED PROMPT:
# -----------------------------------
# DALL-E 3, verilen prompt'u otomatik olarak iyileştirir.
# Örnek: "kedi" → "A fluffy orange tabby cat sitting gracefully..."
# revised_prompt alanında bu iyileştirilmiş prompt döner.

def generate_image(prompt):
    """
    Metin promptundan DALL-E 3 ile görsel üretir.
    
    Args:
        prompt (str): Üretilecek görselin metin açıklaması
        
    Returns:
        tuple: (image_bytes, revised_prompt)
            - image_bytes: Görsel verisi (BytesIO nesnesi)
            - revised_prompt: DALL-E'nin iyileştirdiği prompt
    """
    # DALL-E 3 API çağrısı
    AI_Response = client.images.generate(
        model = "dall-e-3",
        size = "1024x1024",
        quality="hd",
        n=1,
        response_format="url",
        prompt=prompt
    )

    # API yanıtından URL ve iyileştirilmiş prompt'u al
    # AI_Response.data: Üretilen görsellerin listesi
    # AI_Response.data[0].url: İlk görselin URL'si
    # AI_Response.data[0].revised_prompt: İyileştirilmiş prompt
    image_url = AI_Response.data[0].url
    revised_prompt = AI_Response.data[0].revised_prompt

    # URL'den görseli indir
    # requests.get(): HTTP GET isteği
    # response.content: Binary görsel verisi
    response = requests.get(image_url)
    
    # BytesIO: Binary veriyi dosya gibi kullanmak için
    # Streamlit st.image() direkt BytesIO kabul eder
    image_bytes = BytesIO(response.content)

    return image_bytes, revised_prompt


# ============================================================================
# 5. DALL-E İLE GÖRSEL VARYASYONU OLUŞTURMA FONKSİYONU
# ============================================================================
# Mevcut bir görselden benzer ama farklı varyasyonlar üretme
#
# ÖNEMLİ: create_variation() sadece DALL-E 2 ile çalışır!
# DALL-E 3 henüz varyasyon desteği sunmuyor.
#
# client.images.create_variation() PARAMETRELER:
# ----------------------------------------------
# image: Kaynak görsel (dosya nesnesi, binary modda açılmalı)
# size: Çıktı boyutu
# n: Üretilecek varyasyon sayısı (1-10)
# response_format: "url" veya "b64_json"
#
# VARYASYON VS EDİT:
# ------------------
# - Varyasyon: Tüm görseli yeniden yorumlar
# - Edit (inpaint): Görselin belirli bölümlerini değiştirir
#   (Bu örnekte edit kullanılmamış)

def create_image_variation(source_image_url):
    """
    Mevcut bir görselden varyasyon oluşturur (DALL-E 2).
    
    Args:
        source_image_url (str): Kaynak görsel dosya yolu
        
    Returns:
        BytesIO: Üretilen varyasyon görseli
    """
    # Görsel dosyasını binary modda aç ve API'ye gönder
    # open(..., "rb"): Read Binary mode
    AI_Response = client.images.create_variation(
        image=open(source_image_url, "rb"),
        size="1024x1024",
        n=1,
        response_format="url"
    )

    # Üretilen varyasyonun URL'sini al
    generated_image_url = AI_Response.data[0].url

    # URL'den görseli indir
    response = requests.get(generated_image_url)
    image_bytes = BytesIO(response.content)

    return image_bytes


# ============================================================================
# 6. STABLE DIFFUSION XL İLE GÖRSEL ÜRETME FONKSİYONU
# ============================================================================
# Stability AI'nin Stable Diffusion XL modeli ile görsel üretim
#
# STABLE DIFFUSION XL (SDXL) ÖZELLİKLERİ:
# ----------------------------------------
# - 1024x1024 native çözünürlük
# - İki aşamalı üretim (base + refiner)
# - Gelişmiş kompozisyon ve detay
# - Açık kaynak model ağırlıkları
#
# API ENDPOINT:
# -------------
# POST https://api.stability.ai/v1/generation/{engine_id}/text-to-image
# engine_id: "stable-diffusion-xl-1024-v1-0"
#
# REQUEST BODY PARAMETRELERİ:
# ---------------------------
# steps: Diffusion adım sayısı (10-50 arası, fazla = daha detaylı)
# width/height: Görsel boyutları
# seed: Rastgelelik seed'i (0 = rastgele, sabit değer = tekrarlanabilir sonuç)
# cfg_scale: Classifier-Free Guidance Scale (1-35 arası)
#   - Düşük değer: Daha yaratıcı, prompt'a daha az bağlı
#   - Yüksek değer: Prompt'a daha sadık, daha az yaratıcı
# samples: Üretilecek görsel sayısı
#
# TEXT_PROMPTS YAPISI:
# --------------------
# Positive prompt: weight > 0 (istenen özellikler)
# Negative prompt: weight < 0 (istenmeyen özellikler)
#
# Örnek:
# {"text": "beautiful sunset", "weight": 1}    # İstenen
# {"text": "blurry, bad", "weight": -1}        # İstenmeyen
#
# Negative prompt, istenmeyen özellikleri engellemek için kritiktir.
# "blurry, bad, ugly, distorted" gibi terimler yaygın kullanılır.

def generate_with_SD(prompt):
    """
    Stable Diffusion XL ile görsel üretir.
    
    Args:
        prompt (str): Üretilecek görselin metin açıklaması
        
    Returns:
        dict: API yanıtı (artifacts listesi içerir)
    """
    # Stability AI API endpoint
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    # HTTP Headers
    # Accept: Yanıt formatı (JSON)
    # Content-Type: İstek formatı (JSON)
    # Authorization: API anahtarı (Bearer token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {my_key_stabilityai}",
    }

    # Request Body
    body = {
        "steps": 40,           # Diffusion adım sayısı (kalite için 40 iyi bir değer)
        "width": 1024,         # Görsel genişliği
        "height": 1024,        # Görsel yüksekliği
        "seed": 0,             # Rastgele seed (tekrarlanabilirlik için sabit değer kullan)
        "cfg_scale": 5,        # Prompt'a bağlılık (5-7 genellikle dengeli)
        "samples": 1,          # Üretilecek görsel sayısı
        "text_prompts": [
            {
                "text": prompt,    # Positive prompt - istenen özellikler
                "weight": 1
            },
            {
                "text": "blurry, bad",  # Negative prompt - istenmeyen özellikler
                "weight": -1
            }
        ],
    }

    # POST isteği gönder
    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    # JSON yanıtı döndür
    # Yanıt yapısı: {"artifacts": [{"base64": "...", "seed": ..., ...}]}
    data = response.json()

    return data


# ============================================================================
# 7. STREAMLIT ARAYÜZÜ - SEKMELER
# ============================================================================
# Üç farklı işlem için sekmeli arayüz:
# 1. Resim Üret: DALL-E 3 ile metinden görsel
# 2. Varyasyon Oluştur: Mevcut görselden varyasyon
# 3. Stable Diffusion: SDXL ile metinden görsel
#
# st.tabs(): Sekmeli içerik alanları oluşturur
# Her sekme bağımsız widget'lara sahip olabilir

tab_generate, tab_variation, tab_SD = st.tabs(["Resim Üret", "Varyasyon Oluştur", "Stable Diffusion"])


# ============================================================================
# 7.1 TAB 1: DALL-E 3 İLE GÖRSEL OLUŞTURMA
# ============================================================================
# Kullanıcıdan metin alır ve DALL-E 3 ile görsel üretir

with tab_generate:
    st.subheader("DALL-E 3 ile Görsel Oluşturma")
    st.divider()
    
    # Metin giriş alanı
    prompt = st.text_input("Oluşturmak istediğiniz görseli tarif ediniz")
    
    # Oluştur butonu
    generate_btn = st.button("Oluştur")

    # Butona tıklandığında görsel üret
    if generate_btn:
        # Görsel verisi ve iyileştirilmiş prompt'u al
        image_data, revised_prompt = generate_image(prompt)

        # Görseli ekranda göster
        st.image(image=image_data)
        st.divider()
        
        # DALL-E'nin iyileştirdiği prompt'u göster
        # st.caption(): Küçük, soluk metin (açıklama için)
        st.caption(revised_prompt)


# ============================================================================
# 7.2 TAB 2: GÖRSEL VARYASYONU OLUŞTURMA
# ============================================================================
# Kullanıcının yüklediği görselden varyasyon üretir
#
# NOT: Bu özellik DALL-E 2 kullanır (DALL-E 3 desteklemiyor)
# Yüklenen görsel PNG formatında ve kare olmalı

with tab_variation:
    st.subheader("DALL-E 2 ile Görsel Varyasyonu Oluşturma")
    st.divider()
    
    # Dosya yükleme bileşeni
    # type=["png"]: Sadece PNG dosyaları kabul et
    selected_file = st.file_uploader("PNG formatında bir görsel seçiniz", type=["png"])

    # Dosya yüklendiyse önizleme göster
    if selected_file:
        st.image(image=selected_file)

    # Varyasyon oluştur butonu
    variation_btn = st.button("Varyasyon Oluştur")

    # Butona tıklandığında varyasyon üret
    if variation_btn:
        if selected_file:
            # Yüklenen dosyayı geçici olarak kaydet
            # Çünkü API dosya yoluna ihtiyaç duyuyor
            with open("temp_image.png", "wb") as f:
                f.write(selected_file.getbuffer())
            
            # Varyasyon oluştur
            image_data = create_image_variation("temp_image.png")
            
            # Üretilen varyasyonu göster
            st.image(image=image_data)
        else:
            st.warning("Lütfen önce bir görsel yükleyiniz!")


# ============================================================================
# 7.3 TAB 3: STABLE DIFFUSION XL İLE GÖRSEL OLUŞTURMA
# ============================================================================
# Stability AI API kullanarak SDXL ile görsel üretir
#
# DALL-E vs STABLE DIFFUSION KARŞILAŞTIRMASI:
# -------------------------------------------
# | Özellik          | DALL-E 3         | Stable Diffusion XL |
# |------------------|------------------|--------------------|
# | Prompt yorumlama | Otomatik iyileştirme | Manuel kontrol   |
# | Negative prompt  | Yok              | Var                |
# | Açık kaynak      | Hayır            | Evet               |
# | Özelleştirme     | Sınırlı          | Yüksek (LoRA vb.) |
# | Hız              | Hızlı            | Orta               |
# | Fiyat            | Kredi başına     | Saniye başına      |

with tab_SD:
    st.subheader("Stable Diffusion XL ile Görsel Oluşturma")
    st.divider()
    
    # Metin giriş alanı
    # key: Aynı widget tipini birden fazla kullanırken benzersiz anahtar
    SD_prompt = st.text_input("Oluşturmak istediğiniz görseli tarif ediniz", key="sd_text_input")
    
    # Oluştur butonu
    SD_generate_btn = st.button("Oluştur", key="sd_button")

    # Butona tıklandığında görsel üret
    if SD_generate_btn:
        # API çağrısı yap
        data = generate_with_SD(SD_prompt)

        # Üretilen görselleri göster
        # artifacts: Üretilen görsellerin listesi
        # Her artifact: {"base64": "...", "seed": ..., "finishReason": "..."}
        for image in data["artifacts"]:
            # Base64 kodunu çöz
            # base64.b64decode(): Base64 string → binary data
            image_bytes = base64.b64decode(image["base64"])
            
            # Görseli ekranda göster
            st.image(image=image_bytes)


# ============================================================================
# ÖZET: GÖRSEL ÜRETME API'LERİ KARŞILAŞTIRMASI
# ============================================================================
#
# 1. DALL-E (OpenAI):
#    + Yüksek kaliteli sonuçlar
#    + Basit API kullanımı
#    + Prompt otomatik iyileştirme
#    - Kapalı kaynak
#    - Sınırlı özelleştirme
#
# 2. Stable Diffusion (Stability AI):
#    + Açık kaynak
#    + Negative prompt desteği
#    + Yüksek özelleştirme (LoRA, ControlNet vb.)
#    + Kendi sunucunuzda çalıştırabilirsiniz
#    - Daha teknik kullanım
#
# 3. Midjourney:
#    + En yüksek estetik kalite
#    - Discord üzerinden kullanım
#    - API yok (resmi olmayan çözümler var)
#
# MALİYET TAHMİNLERİ (2024):
# --------------------------
# - DALL-E 3 HD: ~$0.080 / görsel
# - DALL-E 3 Standard: ~$0.040 / görsel
# - DALL-E 2: ~$0.020 / görsel
# - Stability AI: ~$0.002 / saniye
# ============================================================================