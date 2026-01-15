# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 5: Metin Üretme Uygulama 101
# 19.5.4 - Cohere Command API Kullanımı
# ============================================================================
# Bu dosya, Cohere'in Command modelini kullanarak metin üretmeyi
# ve Streamlit ile basit bir arayüz oluşturmayı göstermektedir.
#
# COHERE NEDİR?
# -------------
# Cohere, kurumsal odaklı büyük dil modelleri sunan bir AI şirketidir.
# Öne çıkan özellikleri:
# - Enterprise-grade güvenlik ve gizlilik
# - Düşük maliyet ve yüksek performans
# - Özelleştirilebilir modeller (Fine-tuning)
# - RAG (Retrieval Augmented Generation) desteği
#
# COHERE MODELLERİ:
# -----------------
# - command: Genel amaçlı metin üretimi
# - command-light: Daha hızlı ve ekonomik
# - command-nightly: En son güncellemeler
# - embed: Metin gömme (embedding) için
# - rerank: Sonuç sıralama için
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# cohere: Cohere API için resmi Python kütüphanesi
# os: Ortam değişkenlerine erişim
# dotenv: .env dosyasından güvenli anahtar okuma

import cohere
import os
from dotenv import load_dotenv


# ============================================================================
# 2. API YAPILANDIRMASI
# ============================================================================
# .env dosyasından Cohere API anahtarını yükle
#
# .env dosyası örnek formatı:
# cohere_apikey=xxxxxxxxxxxxxxxxxxxxx
#
# API anahtarı almak için: https://dashboard.cohere.com/

load_dotenv()

my_key = os.getenv("cohere_apikey")


# ============================================================================
# 3. COHERE İSTEMCİSİ OLUŞTURMA
# ============================================================================
# cohere.Client(): Cohere API ile iletişim kuracak istemci nesnesi
# api_key: Kimlik doğrulama için gerekli

client = cohere.Client(
    api_key=my_key
)


# ============================================================================
# 4. YANIT ÜRETME FONKSİYONU
# ============================================================================
# Cohere Chat API çağrısı yapan fonksiyon
#
# PARAMETRELER:
# -------------
# model: Kullanılacak Cohere modeli
#   - "command": Ana üretim modeli
#   - "command-light": Hafif ve hızlı versiyon
#   - "command-nightly": En güncel özellikler
#
# temperature: Yaratıcılık seviyesi (0-1 arası)
#
# max_tokens: Üretilecek maksimum token sayısı
#
# chat_history: Önceki konuşma geçmişi
#   - Cohere'de roller: "USER" ve "CHATBOT"
#   - Format: [{"role": "USER", "message": "..."}, ...]
#   - Bu özel format, bağlam sağlamak için kullanılır
#
# message: Kullanıcının mevcut mesajı (ayrı parametre olarak geçilir)
#
# COHERE FARKI:
# -------------
# OpenAI/Claude'dan farklı olarak, Cohere'de:
# - chat_history ve message ayrı parametreler
# - Roller büyük harfle yazılır: "USER", "CHATBOT"
# - Yanıt direkt .text ile alınır

def generate_response(prompt):
    """
    Kullanıcı promptu alır, Cohere API'ye gönderir ve yanıtı döndürür.
    
    Args:
        prompt (str): Kullanıcının girdiği mesaj
        
    Returns:
        str: Command modelinin ürettiği yanıt metni
    """
    AI_Response = client.chat(
        model = "command",
        temperature=0,
        max_tokens=256,
        # Örnek sohbet geçmişi - bağlam sağlamak için
        # Gerçek uygulamada bu dinamik olarak yönetilir
        chat_history=[
            {"role": "USER", "message":"Yer çekimini kim bulmuştur?"},
            {"role": "CHATBOT", "message": "Çekim yasalarını formülize eden Sir Isaac Newton"}
        ],
        message=prompt  # Mevcut kullanıcı mesajı
    )

    # Cohere yanıt yapısı:
    # AI_Response.text: Doğrudan metin yanıtı
    return AI_Response.text


# ============================================================================
# 5. STREAMLIT ARAYÜZÜ
# ============================================================================
import streamlit as st

# Sayfa başlığı
st.header("Command ile İletişim Kurun")
st.divider()


# ============================================================================
# 6. KULLANICI GİRDİSİ VE BUTON
# ============================================================================
# Basit form yapısı: text_input + button

prompt = st.text_input("Mesajınızı Giriniz:")
submit_btn = st.button("Gönder")


# ============================================================================
# 7. YANIT GÖSTERME
# ============================================================================
# Butona tıklandığında API çağrısı yapılır ve yanıt gösterilir

if submit_btn:
    response = generate_response(prompt)
    st.markdown(response)


# ============================================================================
# COHERE API ÖZELLİKLERİ
# ============================================================================
#
# 1. CHAT API (Bu örnekte kullanılan):
#    - Sohbet tarzı etkileşimler
#    - chat_history ile bağlam yönetimi
#    - message ile yeni sorgu
#
# 2. GENERATE API (Alternatif):
#    - Metin tamamlama tarzı
#    - Daha düşük seviye kontrol
#
# 3. EMBED API:
#    - Metin vektörleri oluşturma
#    - Anlamsal arama için kullanılır
#
# 4. RERANK API:
#    - Arama sonuçlarını sıralama
#    - RAG uygulamalarında kritik
#
# COHERE'İN AVANTAJLARI:
# ----------------------
# - Kurumsal kullanım için optimize
# - Rekabetçi fiyatlandırma
# - Hızlı inference süreleri
# - Kolay fine-tuning imkanı
# ============================================================================