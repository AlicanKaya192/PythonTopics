# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 5: Metin Üretme Uygulama 101
# 19.5.2 - OpenAI GPT ile Sohbet Botu (Chatbot)
# ============================================================================
# Bu dosya, OpenAI GPT API ve Streamlit kullanarak tam işlevsel bir
# sohbet botu (chatbot) uygulaması geliştirmeyi göstermektedir.
#
# SOHBET BOTU NEDİR?
# ------------------
# Chatbot, kullanıcılarla doğal dil üzerinden etkileşim kurabilen
# yapay zeka uygulamasıdır. Bu örnekte:
# - Çok turlu konuşma desteği (mesaj geçmişi tutulur)
# - Session State ile oturum yönetimi
# - Streamlit Chat UI bileşenleri kullanılmaktadır
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# OpenAI: GPT API erişimi için
# os: Ortam değişkenlerine erişim
# dotenv: .env dosyasından güvenli anahtar okuma

from openai import OpenAI
import os
from dotenv import load_dotenv


# ============================================================================
# 2. API YAPILANDIRMASI
# ============================================================================
# .env dosyasından API anahtarını yükleyip OpenAI istemcisi oluşturuyoruz

load_dotenv()

my_key = os.getenv("openai_apikey")

client = OpenAI(api_key=my_key)


# ============================================================================
# 3. STREAMLIT İMPORTU
# ============================================================================
# Streamlit: Web arayüzü oluşturmak için kullanılan framework
# st.chat_message: Sohbet baloncukları oluşturur
# st.chat_input: Alt kısımda mesaj giriş alanı sağlar

import streamlit as st


# ============================================================================
# 4. SESSION STATE İLE MESAJ GEÇMİŞİ YÖNETİMİ
# ============================================================================
# NEDEN SESSION STATE?
# --------------------
# Streamlit, her kullanıcı etkileşiminde scripti baştan çalıştırır.
# Session State olmadan mesaj geçmişi kaybolur ve AI bağlamı kaybeder.
#
# messages listesi yapısı:
# [
#   {"role": "system", "content": "..."},   # Sistem promptu (AI davranışı)
#   {"role": "user", "content": "..."},      # Kullanıcı mesajları
#   {"role": "assistant", "content": "..."}  # AI yanıtları
# ]
#
# ÇOK TURLU KONUŞMA:
# ------------------
# Her yeni mesajda tüm geçmiş API'ye gönderilir.
# Bu sayede AI, konuşmanın bağlamını hatırlar.

if "messages" not in st.session_state:
    # İlk çalıştırmada boş mesaj listesi oluştur
    st.session_state.messages = []
    # Sistem promptu ekle - AI'ın davranışını belirler
    st.session_state.messages.append({"role": "system", "content":"Sen yardımsever bir asistansın."})


# ============================================================================
# 5. YANIT ÜRETME FONKSİYONU
# ============================================================================
# Bu fonksiyon:
# 1. Kullanıcı mesajını geçmişe ekler
# 2. Tüm geçmişi API'ye gönderir (bağlam korunur)
# 3. AI yanıtını döndürür

def generate_response(prompt):
    """
    Kullanıcı promptu alır, OpenAI API'ye gönderir ve yanıtı döndürür.
    
    Args:
        prompt (str): Kullanıcının girdiği mesaj
        
    Returns:
        str: AI'ın ürettiği yanıt metni
    """
    # Kullanıcı mesajını sohbet geçmişine ekle
    st.session_state.messages.append({"role": "user", "content": prompt})

    # OpenAI API çağrısı
    # Tüm mesaj geçmişi gönderiliyor (çok turlu konuşma için)
    AI_Response = client.chat.completions.create(
        model = "gpt-4-1106-preview",
        messages=st.session_state.messages  # Tüm geçmiş dahil
    )

    # Yanıt metnini döndür
    return AI_Response.choices[0].message.content


# ============================================================================
# 6. STREAMLIT ARAYÜZ TASARIMI
# ============================================================================
# st.header(): Sayfa başlığı
# st.divider(): Görsel ayraç çizgisi

st.header("İlk Sohbet Botum")
st.divider()


# ============================================================================
# 7. MESAJ GEÇMİŞİNİ EKRANDA GÖSTERME
# ============================================================================
# st.session_state.messages[1:] : Sistem promptunu atla (kullanıcıya gösterme)
# st.chat_message(): Rol bazlı sohbet baloncuğu oluşturur
#   - "user": Kullanıcı mesajları (sağda)
#   - "assistant": AI mesajları (solda)
#
# Bu döngü, sayfa her yenilendiğinde tüm geçmişi yeniden render eder

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================================
# 8. KULLANICI GİRDİSİ VE YANIT DÖNGÜSÜ
# ============================================================================
# st.chat_input(): Sayfanın altında mesaj giriş alanı
# := (walrus operator): Değişkene atama yapar VE True/False döner
#   - Kullanıcı mesaj girerse: prompt = mesaj, if bloğu çalışır
#   - Boşsa: prompt = None, if bloğu atlanır
#
# AKIŞ:
# 1. Kullanıcı mesaj yazar ve Enter'a basar
# 2. Kullanıcı mesajı ekranda gösterilir
# 3. generate_response() çağrılır
# 4. AI yanıtı ekranda gösterilir
# 5. AI yanıtı geçmişe eklenir

if prompt := st.chat_input("Mesajınızı Giriniz"):

    # Kullanıcı mesajını hemen ekranda göster
    st.chat_message("user").markdown(prompt)

    # AI yanıtını al
    response = generate_response(prompt)

    # AI yanıtını sohbet baloncuğunda göster
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # AI yanıtını geçmişe ekle (sonraki turlarda bağlam için)
    st.session_state.messages.append({"role": "assistant", "content": response})


# ============================================================================
# ÖZET: SOHBET BOTU MİMARİSİ
# ============================================================================
# 
# [Kullanıcı] --> [Streamlit UI] --> [Session State (Geçmiş)]
#                      |                      |
#                      v                      v
#              [generate_response] <--- [Tüm Mesajlar]
#                      |
#                      v
#              [OpenAI API] --> [GPT-4]
#                      |
#                      v
#              [AI Yanıtı] --> [Ekranda Göster + Geçmişe Ekle]
#
# ÖNEMLİ NOKTALAR:
# ----------------
# 1. Session State ZORUNLU - Aksi halde her mesajda geçmiş sıfırlanır
# 2. Sistem promptu ilk elemanda tutulur ama ekranda gösterilmez
# 3. Tüm geçmiş her API çağrısında gönderilir (token maliyeti artar)
# 4. Uzun konuşmalarda token limiti aşılabilir (bağlam penceresi)
# ============================================================================
