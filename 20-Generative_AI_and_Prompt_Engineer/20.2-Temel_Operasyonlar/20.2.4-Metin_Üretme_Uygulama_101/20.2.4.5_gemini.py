# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 5: Metin Üretme Uygulama 101
# 19.5.5 - Google Gemini API Kullanımı
# ============================================================================
# Bu dosya, Google'ın Gemini modelini kullanarak metin üretmeyi
# ve Streamlit ile basit bir arayüz oluşturmayı göstermektedir.
#
# GEMINI NEDİR?
# -------------
# Gemini, Google DeepMind tarafından geliştirilen multimodal AI modelidir.
# Öne çıkan özellikleri:
# - Multimodal: Metin, görsel, ses ve video anlama
# - Uzun bağlam penceresi (1M+ token Gemini 1.5'te)
# - Google ekosistemi ile entegrasyon
# - Rekabetçi fiyatlandırma
#
# GEMINI MODELLERİ:
# -----------------
# - gemini-pro: Metin tabanlı görevler için (1.0)
# - gemini-pro-vision: Görsel + metin anlama (1.0)
# - gemini-1.5-pro: En gelişmiş model (1M token bağlam)
# - gemini-1.5-flash: Hızlı ve ekonomik
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# google.generativeai: Google Gemini API için resmi kütüphane
# os: Ortam değişkenlerine erişim
# dotenv: .env dosyasından güvenli anahtar okuma

import google.generativeai as genai
import os
from dotenv import load_dotenv


# ============================================================================
# 2. API YAPILANDIRMASI
# ============================================================================
# .env dosyasından Google API anahtarını yükle
#
# .env dosyası örnek formatı:
# google_apikey=AIzaXXXXXXXXXXXXXXXXXXXXXXXX
#
# API anahtarı almak için: https://makersuite.google.com/app/apikey

load_dotenv()

my_key = os.getenv("google_apikey")


# ============================================================================
# 3. GEMINI API YAPILANDIRMASI
# ============================================================================
# genai.configure(): API anahtarını global olarak ayarlar
# Bu fonksiyon bir kez çağrılmalı, tüm sonraki işlemler bu ayarı kullanır

genai.configure(
    api_key=my_key
)


# ============================================================================
# 4. GENERATIVE MODEL OLUŞTURMA
# ============================================================================
# genai.GenerativeModel(): Belirli bir model için istemci oluşturur
# model_name: Kullanılacak Gemini modeli
#   - "gemini-pro": Metin üretimi için optimize
#   - "gemini-pro-vision": Görsel anlama için
#   - "gemini-1.5-pro": En gelişmiş, multimodal
#   - "gemini-1.5-flash": Hızlı inferans

client = genai.GenerativeModel(
    model_name="gemini-pro"
)


# ============================================================================
# 5. YANIT ÜRETME FONKSİYONU
# ============================================================================
# Gemini ile sohbet tabanlı metin üretimi
#
# CHAT API YAKLAŞIMI:
# -------------------
# client.start_chat(): Yeni bir sohbet oturumu başlatır
#   - history: Önceki mesaj geçmişi (boş liste = yeni sohbet)
#   
# chat.send_message(): Mesaj gönderir ve yanıt alır
#   - generation_config: Üretim parametreleri
#     - temperature: Yaratıcılık seviyesi (0-1)
#     - max_output_tokens: Maksimum çıktı token sayısı
#
# ALTERNATİF: generate_content()
# ------------------------------
# Tek seferlik üretim için (dosya sonunda yorum satırlarında örnek var)
# Sohbet geçmişi tutmak gerekmediğinde kullanılabilir

def generate_response(prompt):
    """
    Kullanıcı promptu alır, Gemini API'ye gönderir ve yanıtı döndürür.
    
    Args:
        prompt (str): Kullanıcının girdiği mesaj
        
    Returns:
        str: Gemini'nin ürettiği yanıt metni
    """
    # Yeni sohbet oturumu başlat
    # history=[] ile boş geçmiş - her çağrıda sıfırdan başlar
    chat = client.start_chat(history=[])

    # Mesaj gönder ve yapılandırma ile yanıt al
    AI_Response = chat.send_message(
        prompt,  # Kullanıcı mesajı
        generation_config=genai.GenerationConfig(
            temperature=0,        # Deterministik yanıtlar
            max_output_tokens=256 # Maksimum çıktı uzunluğu
        )
    )

    # Yanıt yapısı:
    # AI_Response.text: Üretilen metin içeriği
    return AI_Response.text


# ============================================================================
# 6. STREAMLIT ARAYÜZÜ
# ============================================================================
import streamlit as st

# Sayfa başlığı
st.header("Gemini ile İletişim Kurun")
st.divider()


# ============================================================================
# 7. KULLANICI GİRDİSİ VE BUTON
# ============================================================================
# Basit form yapısı: text_input + button

prompt = st.text_input("Mesajınızı Giriniz:")
submit_btn = st.button("Gönder")


# ============================================================================
# 8. YANIT GÖSTERME
# ============================================================================
# Butona tıklandığında API çağrısı yapılır ve yanıt gösterilir

if submit_btn:
    response = generate_response(prompt)
    st.markdown(response)


# ============================================================================
# ALTERNATİF KULLANIM: generate_content()
# ============================================================================
# Sohbet oturumu olmadan direkt içerik üretimi için kullanılabilir
# Tek seferlik sorular için daha basit bir yaklaşım

# AI_Response = client.generate_content(
#     "Mevsimler neden oluşur?",
#     generation_config=genai.GenerationConfig(
#         temperature=0,
#         max_output_tokens=256
#         )
# )
# print(AI_Response.text)


# ============================================================================
# GEMINI API ÖZELLİKLERİ
# ============================================================================
#
# 1. METIN ÜRETİMİ (Bu örnekte kullanılan):
#    - generate_content(): Tek seferlik üretim
#    - start_chat(): Sohbet tabanlı üretim
#
# 2. GÖRSEL ANLAMA (gemini-pro-vision veya gemini-1.5):
#    - Resim + metin girişi kabul eder
#    - Görsel içerik analizi yapabilir
#
# 3. EMBEDDING:
#    - embed_content(): Metin vektörleri oluşturma
#
# GEMINI'NİN AVANTAJLARI:
# -----------------------
# - Çok uzun bağlam penceresi (1M+ token)
# - Multimodal yetenekler (metin, görsel, ses, video)
# - Google ürünleri ile entegrasyon
# - Ücretsiz tier mevcut (sınırlı kullanım)
# - Rekabetçi performans/fiyat oranı
#
# SINIRLAMALAR:
# -------------
# - Bazı bölgelerde erişim kısıtlaması olabilir
# - Günlük istek limitleri var (ücretsiz tier'da)
# ============================================================================