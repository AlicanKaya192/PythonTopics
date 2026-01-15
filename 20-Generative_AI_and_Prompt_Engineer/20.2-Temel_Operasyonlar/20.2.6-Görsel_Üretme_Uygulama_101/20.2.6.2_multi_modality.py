# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 6: Görsel Üretme Uygulama 101
# 19.2.6.2 - Çoklu Modalite (Multimodality) - Görsel Anlama
# ============================================================================
# Bu dosya, farklı AI Vision modelleri kullanarak:
# - Görsel içerik analizi (Image Understanding)
# - Görsel soru-cevap (Visual Question Answering - VQA)
# - Görsel betimleme (Image Captioning)
# işlemlerini Streamlit arayüzü ile göstermektedir.
#
# GÖRSEL ANLAMA VS GÖRSEL ÜRETME
# ==============================
# Bu dosya 19.2.6.1 (image_ops.py) ile TERS yönde çalışır:
#
# | 19.2.6.1 (Image Generation) | 19.2.6.2 (Image Understanding) |
# |-----------------------------|--------------------------------|
# | Metin → Görsel              | Görsel → Metin                 |
# | DALL-E, Stable Diffusion    | GPT-4 Vision, Gemini Vision    |
# | Yaratıcı (Generative)       | Analitik (Understanding)       |
#
# MULTİMODALİTE NEDİR?
# ====================
# Multimodal AI, birden fazla veri tipini (metin, görsel, ses) 
# aynı anda anlayabilen ve işleyebilen modellerdir.
#
# Örnek Kullanım Senaryoları:
# - "Bu resimde kaç kişi var?" → Sayma
# - "Bu grafik ne anlatıyor?" → Grafik analizi
# - "Bu ürünün fiyatını oku" → OCR (metin okuma)
# - "Bu resmi detaylı betimle" → Betimleme
# - "Bu iki resim arasındaki fark ne?" → Karşılaştırma
#
# KULLANILAN MODELLER
# ===================
# 1. GPT-4 Vision (OpenAI):
#    - GPT-4'ün görsel anlama yetenekli versiyonu
#    - Yüksek doğruluk ve detaylı açıklamalar
#    - URL veya Base64 ile görsel kabul eder
#
# 2. Gemini Pro Vision (Google):
#    - Google'ın multimodal AI modeli
#    - Görsel + metin birlikte işleme
#    - PIL.Image nesnesi olarak görsel kabul eder
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# OpenAI: GPT-4 Vision API erişimi için
# google.generativeai: Gemini Vision API için
# base64: Yerel görseli Base64'e encode etmek için
# PIL.Image: Görsel dosyalarını açmak için (Pillow kütüphanesi)
# requests: HTTP istekleri (OpenAI REST API için)
# os: Ortam değişkenlerine erişim
# dotenv: .env dosyasından API anahtarlarını okumak için
# streamlit: Web arayüzü oluşturmak için

from openai import OpenAI
import google.generativeai as genai
import base64
import PIL.Image
import requests
import os
from dotenv import load_dotenv
import streamlit as st


# ============================================================================
# 2. API YAPILANDIRMASI
# ============================================================================
# İki farklı API için anahtar yükleme:
# - OpenAI: GPT-4 Vision için
# - Google: Gemini Pro Vision için
#
# .env dosyası örnek formatı:
# openai_apikey=sk-xxxxxxxxxxxxxxxxxxxxx
# google_apikey=AIzaxxxxxxxxxxxxxxxxxxxxx

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_google = os.getenv("google_apikey")


# ============================================================================
# 3. OPENAI İSTEMCİSİ OLUŞTURMA
# ============================================================================
# GPT-4 Vision API çağrıları için OpenAI istemcisi

client = OpenAI(api_key=my_key_openai)


# ============================================================================
# 4. GOOGLE GEMINI API YAPILANDIRMASI
# ============================================================================
# Gemini Vision API için global yapılandırma

genai.configure(
    api_key=my_key_google
)


# ============================================================================
# 5. GPT-4 VISION - URL İLE GÖRSEL ANLAMA
# ============================================================================
# İnternetteki bir görseli URL üzerinden analiz etme
#
# GPT-4 Vision MESAJ YAPISI:
# --------------------------
# messages listesinde "content" alanı artık liste olabilir:
# [
#   {"type": "text", "text": "..."},      # Metin prompt
#   {"type": "image_url", "image_url": {...}}  # Görsel
# ]
#
# image_url PARAMETRELERI:
# ------------------------
# url: Görsel URL'si veya Base64 data URI
# detail: Analiz detay seviyesi (opsiyonel)
#   - "low": Düşük çözünürlük, hızlı, ucuz
#   - "high": Yüksek çözünürlük, yavaş, pahalı
#   - "auto": Otomatik seçim (varsayılan)
#
# max_tokens: Yanıt için maksimum token sayısı
#   - Vision modellerinde mutlaka belirtilmeli

def gpt_vision_with_url(image_url, prompt="Bu resmin içeriğini betimle"):
    """
    URL'deki görseli GPT-4 Vision ile analiz eder.
    
    Args:
        image_url (str): Görselin web adresi
        prompt (str): Görsel hakkında sorulacak soru
        
    Returns:
        str: AI'ın görsel hakkındaki yanıtı
    """
    # GPT-4 Vision API çağrısı
    AI_Response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                # Metin promptu
                {"type": "text", "text": prompt},
                # Görsel (URL olarak)
                {
                    "type": "image_url",
                    "image_url": {
                            "url": image_url,
                            },
                },
            ],
        }
    ],
    max_tokens=300
    )

    # Yanıt metnini döndür
    return AI_Response.choices[0].message.content


# ============================================================================
# 6. BASE64 ENCODE YARDIMCI FONKSİYONU
# ============================================================================
# Yerel görsel dosyasını Base64 string'e dönüştürme
#
# NEDEN BASE64?
# -------------
# - HTTP üzerinden binary veri göndermek için
# - JSON payload içinde görsel taşımak için
# - URL gerektirmeyen senaryolar için (gizlilik)
#
# Base64, binary veriyi ASCII karakterlere dönüştürür.
# Boyut ~%33 artar ama metin olarak taşınabilir hale gelir.

def encode_image(image_path):
    """
    Görsel dosyasını Base64 string'e dönüştürür.
    
    Args:
        image_path (str): Görsel dosya yolu
        
    Returns:
        str: Base64 encoded string
    """
    # Dosyayı binary modda aç ve oku
    with open(image_path, "rb") as image_file:
        # base64.b64encode(): Binary → Base64 bytes
        # .decode('utf-8'): Bytes → String
        return base64.b64encode(image_file.read()).decode('utf-8')


# ============================================================================
# 7. GPT-4 VISION - YEREL DOSYA İLE GÖRSEL ANLAMA
# ============================================================================
# Bilgisayardaki bir görseli Base64 encode ederek analiz etme
#
# DATA URI FORMATI:
# -----------------
# "data:image/jpeg;base64,{base64_encoded_data}"
#
# Parçalar:
# - data: URI şeması
# - image/jpeg: MIME tipi (jpeg, png, gif, webp)
# - base64: Encoding türü
# - {data}: Base64 encoded görsel verisi
#
# NOT: Bu fonksiyon requests ile direkt REST API kullanıyor
# OpenAI SDK'sı da aynı işlemi yapabilir

def gpt_vision_with_local_file(image_path, prompt="Bu resmin içeriğini betimle"):
    """
    Yerel görsel dosyasını GPT-4 Vision ile analiz eder.
    
    Args:
        image_path (str): Görsel dosya yolu
        prompt (str): Görsel hakkında sorulacak soru
        
    Returns:
        str: AI'ın görsel hakkındaki yanıtı
    """
    # Görseli Base64'e encode et
    base64_image = encode_image(image_path)

    # OpenAI API endpoint
    gpt_vision_url = "https://api.openai.com/v1/chat/completions"

    # HTTP Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {my_key_openai}"
    }

    # Request payload
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt
                },
                {
                "type": "image_url",
                "image_url": {
                    # Data URI formatında Base64 görsel
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
    }

    # POST isteği gönder
    AI_Response = requests.post(url=gpt_vision_url, headers=headers, json=payload)

    # JSON yanıtından metin çıkar
    final_response = AI_Response.json()['choices'][0]['message']['content']

    return final_response


# ============================================================================
# 8. GEMINI PRO VISION - YEREL DOSYA İLE GÖRSEL ANLAMA
# ============================================================================
# Google Gemini modeli ile görsel analizi
#
# GEMINI VISION ÖZELLİKLERİ:
# --------------------------
# - PIL.Image nesnesi olarak görsel kabul eder
# - Metin ve görsel birlikte liste olarak gönderilir
# - generate_content() ile multimodal içerik üretimi
# - resolve() ile asenkron yanıtı bekle
#
# GEMINI VS GPT-4 VISION:
# -----------------------
# | Özellik       | GPT-4 Vision    | Gemini Pro Vision |
# |---------------|-----------------|-------------------|
# | Görsel Girdi  | URL veya Base64 | PIL.Image         |
# | Çoklu Görsel  | Evet            | Evet              |
# | Video Analizi | Hayır           | Evet (1.5)        |
# | Maliyet       | Yüksek          | Düşük             |

def gemini_vision_with_local_file(image_path, prompt="Bu resmin içeriğini betimle"):
    """
    Yerel görsel dosyasını Gemini Pro Vision ile analiz eder.
    
    Args:
        image_path (str): Görsel dosya yolu
        prompt (str): Görsel hakkında sorulacak soru
        
    Returns:
        str: AI'ın görsel hakkındaki yanıtı
    """
    # Gemini Vision modeli oluştur
    client = genai.GenerativeModel(
        model_name="gemini-pro-vision"
    )

    # PIL ile görseli aç
    # PIL.Image: Python Imaging Library (Pillow)
    source_image = PIL.Image.open(image_path)

    # Multimodal içerik gönder
    # Liste formatı: [metin, görsel, metin, görsel, ...]
    AI_Response = client.generate_content(
        [
            prompt,        # Metin promptu
            source_image   # PIL.Image nesnesi
        ]
    )

    # Asenkron yanıtı bekle (safety check dahil)
    AI_Response.resolve()

    # Yanıt metnini döndür
    return AI_Response.text


# ============================================================================
# 9. STREAMLIT ARAYÜZÜ - BAŞLIK
# ============================================================================
# Sayfa başlığı ve ayraç

st.title("Çoklu Modalite - Görsel Anlama")
st.divider()


# ============================================================================
# 10. STREAMLIT ARAYÜZÜ - SEKMELER
# ============================================================================
# Üç farklı yöntem için sekmeli arayüz:
# 1. GPT-4 Vision ile URL'den analiz
# 2. GPT-4 Vision ile yerel dosyadan analiz
# 3. Gemini Pro Vision ile yerel dosyadan analiz

tab_url, tab_local, tab_gemini = st.tabs(
   [
      "GPT-4 Vision ile URL'den Çalışma", 
      "GPT-4 Vision ile Yerel Dosyadan Çalışma", 
      "Gemini Pro Vision ile Yerel Dosyadan Çalışma"
    ]
)


# ============================================================================
# 10.1 TAB 1: GPT-4 VISION - URL İLE ANALİZ
# ============================================================================
# Kullanıcı bir görsel URL'si ve soru girer, AI analiz eder

with tab_url:
    st.subheader("GPT-4 Vision ile URL'den Görsel Analizi")
    st.divider()

    # Görsel URL'si giriş alanı
    image_url = st.text_input(
        label="Görselin bulunduğu web adresini giriniz", 
        key="imageurl_url",
        placeholder="https://example.com/image.jpg"
    )

    # Prompt giriş alanı
    prompt = st.text_input(
        label="Görsel hakkında sormak istediğiniz soruyu yazınız", 
        key="prompt_url",
        placeholder="Bu resimde ne görüyorsun?"
    )

    # Gönder butonu
    submit_btn = st.button(label="Analiz Et", key="submit_url")

    # Butona tıklandığında analiz yap
    if submit_btn:
        if image_url and prompt:
            # GPT-4 Vision ile analiz
            response = gpt_vision_with_url(image_url=image_url, prompt=prompt)

            # Sonucu göster
            st.success(response)

            # Görseli de göster
            st.image(image=image_url)
        else:
            st.warning("Lütfen görsel URL'si ve soru giriniz!")


# ============================================================================
# 10.2 TAB 2: GPT-4 VISION - YEREL DOSYA İLE ANALİZ
# ============================================================================
# Kullanıcı bilgisayarından görsel yükler, AI analiz eder

with tab_local:
    st.subheader("GPT-4 Vision ile Yerel Dosyadan Görsel Analizi")
    st.divider()

    # Prompt giriş alanı
    prompt = st.text_input(
        label="Görsel hakkında sormak istediğiniz soruyu yazınız", 
        key="prompt_gpt",
        placeholder="Bu resimde kaç nesne var?"
    )

    # Dosya yükleme bileşeni
    selected_image = st.file_uploader(
        label="Analiz edilecek görseli seçiniz", 
        type=["png", "jpg", "jpeg"], 
        key="image_gpt"
    )

    # Dosya yüklendiyse önizleme göster
    if selected_image:
        # Yüklenen dosyayı geçici olarak kaydet
        temp_path = f"../../assets/temp_gpt_{selected_image.name}"
        with open(temp_path, "wb") as f:
            f.write(selected_image.getbuffer())
        
        st.image(image=selected_image)

    # Gönder butonu
    submit_btn = st.button(label="Analiz Et", key="submit_gpt")

    # Butona tıklandığında analiz yap
    if submit_btn:
        if selected_image and prompt:
            temp_path = f"../../assets/temp_gpt_{selected_image.name}"
            response = gpt_vision_with_local_file(image_path=temp_path, prompt=prompt)
            st.success(response)
        else:
            st.warning("Lütfen görsel yükleyin ve soru giriniz!")


# ============================================================================
# 10.3 TAB 3: GEMINI PRO VISION - YEREL DOSYA İLE ANALİZ
# ============================================================================
# Google Gemini modeli ile görsel analizi

with tab_gemini:
    st.subheader("Gemini Pro Vision ile Yerel Dosyadan Görsel Analizi")
    st.divider()

    # Prompt giriş alanı
    prompt = st.text_input(
        label="Görsel hakkında sormak istediğiniz soruyu yazınız", 
        key="prompt_gemini",
        placeholder="Bu resmi detaylı olarak betimle"
    )

    # Dosya yükleme bileşeni
    selected_image = st.file_uploader(
        label="Analiz edilecek görseli seçiniz", 
        type=["png", "jpg", "jpeg"], 
        key="image_gemini"
    )

    # Dosya yüklendiyse önizleme göster
    if selected_image:
        # Yüklenen dosyayı geçici olarak kaydet
        temp_path = f"../../assets/temp_gemini_{selected_image.name}"
        with open(temp_path, "wb") as f:
            f.write(selected_image.getbuffer())
        
        st.image(image=selected_image)

    # Gönder butonu
    submit_btn = st.button(label="Analiz Et", key="submit_gemini")

    # Butona tıklandığında analiz yap
    if submit_btn:
        if selected_image and prompt:
            temp_path = f"../../assets/temp_gemini_{selected_image.name}"
            response = gemini_vision_with_local_file(image_path=temp_path, prompt=prompt)
            st.success(response)
        else:
            st.warning("Lütfen görsel yükleyin ve soru giriniz!")


# ============================================================================
# ÖZET: GÖRSEL ANLAMA MODELLERİ KARŞILAŞTIRMASI
# ============================================================================
#
# | Model             | Şirket  | Görsel Girdi    | Özellikler              |
# |-------------------|---------|-----------------|-------------------------|
# | GPT-4 Vision      | OpenAI  | URL, Base64     | Yüksek doğruluk, detay  |
# | GPT-4o            | OpenAI  | URL, Base64     | Daha hızlı, ucuz        |
# | Gemini Pro Vision | Google  | PIL.Image       | Video desteği, ekonomik |
# | Gemini 1.5 Pro    | Google  | PIL.Image       | 1M token, video         |
# | Claude 3 Vision   | Anthro. | Base64          | Güvenlik odaklı         |
# | LLaVA             | Açık K. | PIL.Image       | Ücretsiz, self-host     |
#
# GÖRSEL ANLAMA KULLANIM ALANLARI:
# --------------------------------
# 1. Görsel Soru-Cevap (VQA): "Bu resimde kaç kişi var?"
# 2. Görsel Betimleme: "Bu resmi açıkla"
# 3. OCR (Metin Okuma): "Bu belgedeki metni oku"
# 4. Grafik Analizi: "Bu grafiğin trendi ne?"
# 5. Tıbbi Görüntüleme: "Bu röntgende anormal bir şey var mı?"
# 6. Ürün Tanıma: "Bu ürün ne ve markası ne?"
# 7. Erişilebilirlik: Görme engelliler için görsel açıklama
#
# MALİYET TAHMİNLERİ (2024):
# --------------------------
# - GPT-4 Vision: ~$0.01-0.03 / görsel (boyuta göre)
# - Gemini Pro Vision: ~$0.0025 / görsel
# - Claude 3 Opus: ~$0.024 / görsel
# ============================================================================