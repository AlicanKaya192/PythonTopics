# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 5: Metin Üretme Uygulama 101
# 19.5.3 - Anthropic Claude API Kullanımı
# ============================================================================
# Bu dosya, Anthropic'in Claude modelini kullanarak metin üretmeyi
# ve Streamlit ile basit bir arayüz oluşturmayı göstermektedir.
#
# CLAUDE NEDİR?
# -------------
# Claude, Anthropic tarafından geliştirilen büyük dil modelidir.
# Öne çıkan özellikleri:
# - Güvenlik odaklı tasarım (Constitutional AI)
# - Uzun bağlam penceresi (100K+ token)
# - Dürüst ve yardımsever yanıtlar
# - GPT'ye alternatif güçlü bir model
#
# CLAUDE MODELLERİ:
# -----------------
# - claude-3-opus: En güçlü model (karmaşık görevler)
# - claude-3-sonnet: Dengeli performans/maliyet
# - claude-3-haiku: En hızlı ve ekonomik
# - claude-2.1: Önceki nesil (bu örnekte kullanılan)
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# anthropic: Anthropic Claude API için resmi Python kütüphanesi
# os: Ortam değişkenlerine erişim
# dotenv: .env dosyasından güvenli anahtar okuma

import anthropic
import os
from dotenv import load_dotenv


# ============================================================================
# 2. API YAPILANDIRMASI
# ============================================================================
# .env dosyasından Anthropic API anahtarını yükle
# 
# .env dosyası örnek formatı:
# anthropic_apikey=sk-ant-xxxxxxxxxxxxxxxxxxxxx
#
# API anahtarı almak için: https://console.anthropic.com/

load_dotenv()

my_key = os.getenv("anthropic_apikey")


# ============================================================================
# 3. ANTHROPIC İSTEMCİSİ OLUŞTURMA
# ============================================================================
# anthropic.Anthropic(): Claude API ile iletişim kuracak istemci nesnesi
# api_key: Kimlik doğrulama için gerekli

client = anthropic.Anthropic(
    api_key=my_key
)


# ============================================================================
# 4. YANIT ÜRETME FONKSİYONU
# ============================================================================
# Claude API çağrısı yapan fonksiyon
#
# PARAMETRELER:
# -------------
# model: Kullanılacak Claude modeli
#   - "claude-2.1": Önceki nesil model
#   - "claude-3-opus-20240229": En güçlü Claude 3
#   - "claude-3-sonnet-20240229": Dengeli seçenek
#   - "claude-3-haiku-20240307": En hızlı
#
# temperature: Yaratıcılık seviyesi (0-1 arası)
#   - 0: Tutarlı, deterministik cevaplar
#   - 1: Maksimum yaratıcılık
#
# max_tokens: Üretilecek maksimum token sayısı
#
# messages: Mesaj listesi
#   - Claude'da system parametresi ayrı bir argüman olarak geçilebilir
#   - messages listesinde sadece user ve assistant rolleri bulunur
#
# NOT: client.beta.messages.create() beta endpoint kullanıyor
# Güncel sürümde client.messages.create() kullanılabilir

def generate_response(prompt):
    """
    Kullanıcı promptu alır, Claude API'ye gönderir ve yanıtı döndürür.
    
    Args:
        prompt (str): Kullanıcının girdiği mesaj
        
    Returns:
        str: Claude'un ürettiği yanıt metni
    """
    AI_Response = client.beta.messages.create(
        model = "claude-2.1",
        temperature=0,
        max_tokens=256,
        messages=[
            {"role":"user", "content":prompt}
        ]
    )

    # Yanıt yapısı:
    # AI_Response.content: İçerik bloklarının listesi
    # AI_Response.content[0]: İlk içerik bloğu
    # AI_Response.content[0].text: Metin içeriği
    return AI_Response.content[0].text


# ============================================================================
# 5. STREAMLIT ARAYÜZÜ
# ============================================================================
import streamlit as st

# Sayfa başlığı
st.header("Claude ile İletişim Kurun")
st.divider()


# ============================================================================
# 6. KULLANICI GİRDİSİ VE BUTON
# ============================================================================
# st.text_input(): Tek satırlık metin giriş alanı
# st.button(): Tıklanabilir buton
#
# NOT: Bu basit bir örnek - her istekte yeni bir sohbet başlar
# Çok turlu sohbet için Session State kullanılmalı (19.5.2_chat.py gibi)

prompt = st.text_input("Mesajınızı Giriniz:")
submit_btn = st.button("Gönder")


# ============================================================================
# 7. YANIT GÖSTERME
# ============================================================================
# Butona tıklandığında:
# 1. generate_response() çağrılır
# 2. Claude yanıtı markdown olarak gösterilir

if submit_btn:
    response = generate_response(prompt)
    st.markdown(response)


# ============================================================================
# CLAUDE VS OPENAI API FARKLARI
# ============================================================================
#
# | Özellik           | OpenAI (GPT)                | Anthropic (Claude)        |
# |-------------------|-----------------------------|-----------------------------|
# | System Prompt     | messages içinde "system"    | Ayrı system parametresi     |
# | Yanıt Yapısı      | choices[0].message.content  | content[0].text             |
# | Token Limiti      | Model bazlı (8K-128K)       | 100K+ (Claude 2.1+)         |
# | Fiyatlandırma     | Token başına                | Token başına                |
#
# CLAUDE'UN AVANTAJLARI:
# ----------------------
# - Daha uzun bağlam penceresi
# - Constitutional AI ile güvenlik odaklı
# - Daha az "halüsinasyon" eğilimi
# - Detaylı ve yapılandırılmış yanıtlar
# ============================================================================
