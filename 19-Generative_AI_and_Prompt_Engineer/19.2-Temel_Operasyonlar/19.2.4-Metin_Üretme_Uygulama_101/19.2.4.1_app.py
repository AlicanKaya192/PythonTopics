# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 5: Metin Üretme Uygulama 101
# 19.5.1 - OpenAI GPT API Temel Kullanımı
# ============================================================================
# Bu dosya, OpenAI'nin GPT modellerini kullanarak metin üretmenin
# en temel örneğini içermektedir. Chat Completions API ile basit
# bir soru-cevap uygulaması geliştirilmiştir.
#
# OPENAI API NEDİR?
# -----------------
# OpenAI API, GPT serisi dil modellerine programatik erişim sağlar.
# - GPT-4, GPT-3.5 gibi güçlü dil modellerini kullanabilirsiniz
# - Chat Completions: Sohbet tarzı metin üretimi için kullanılır
# - Text Completions: Metin tamamlama için kullanılır (eski yöntem)
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# OpenAI: OpenAI API ile iletişim kurmak için resmi Python kütüphanesi
# os: İşletim sistemi ortam değişkenlerine erişim için
# dotenv: .env dosyasından API anahtarlarını güvenli şekilde okumak için

from openai import OpenAI
import os
from dotenv import load_dotenv


# ============================================================================
# 2. ORTAM DEĞİŞKENLERİNİ YÜKLEME
# ============================================================================
# load_dotenv(): Proje kök dizinindeki .env dosyasını okur
# .env dosyası API anahtarları gibi hassas bilgileri içerir
# Bu dosya ASLA git'e yüklenmemeli (.gitignore'a eklenmeli)
#
# .env dosyası örnek formatı:
# openai_apikey=sk-xxxxxxxxxxxxxxxxxxxxx

load_dotenv()


# ============================================================================
# 3. API ANAHTARI OKUMA
# ============================================================================
# os.getenv(): Ortam değişkeninden API anahtarını okur
# Güvenlik: API anahtarları kod içinde yazılmamalı, ortam değişkenlerinden okunmalı
# Bu sayede kod paylaşıldığında anahtarlar açığa çıkmaz

my_key = os.getenv("openai_apikey")


# ============================================================================
# 4. OPENAI İSTEMCİSİ (CLIENT) OLUŞTURMA
# ============================================================================
# OpenAI(): API ile iletişim kuracak istemci nesnesi oluşturur
# api_key: Kimlik doğrulama için kullanılan API anahtarı
# Bu nesne üzerinden tüm API çağrıları yapılır

client = OpenAI(api_key=my_key)


# ============================================================================
# 5. CHAT COMPLETIONS API ÇAĞRISI
# ============================================================================
# client.chat.completions.create(): Sohbet tarzı metin üretimi için ana fonksiyon
#
# PARAMETRELER:
# -------------
# model: Kullanılacak GPT modeli
#   - "gpt-4-1106-preview": GPT-4 Turbo (daha hızlı ve ucuz)
#   - "gpt-4": Standart GPT-4
#   - "gpt-3.5-turbo": Daha hızlı ve ekonomik seçenek
#
# temperature: Yaratıcılık seviyesi (0-2 arası)
#   - 0: Deterministik, tutarlı cevaplar (her zaman aynı sonuç)
#   - 1: Dengeli yaratıcılık
#   - 2: Maksimum yaratıcılık (daha rastgele)
#
# max_tokens: Üretilecek maksimum token sayısı
#   - Token ≈ kelime parçası (Türkçe'de ~0.5 kelime)
#   - 256 token ≈ 100-150 kelime
#
# messages: Sohbet geçmişi listesi (rol-içerik çiftleri)
#   - "system": Asistanın davranışını belirler (sistem promptu)
#   - "user": Kullanıcının mesajı
#   - "assistant": Önceki AI cevapları (çok turlu sohbetlerde)

AI_Response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    temperature=0,
    max_tokens=256,
    messages=[
        {"role": "system", "content":"Sen yardımsever bir asistansın."},
        {"role": "user", "content": "Mevsimler neden oluşur? Dünya kendi etrafında döndüğü için mi?"}
    ]
)


# ============================================================================
# 6. YANITI EKRANA YAZDIRMA
# ============================================================================
# API Yanıt Yapısı:
# -----------------
# AI_Response: Tüm yanıt nesnesi
# AI_Response.choices: Üretilen yanıt seçenekleri listesi (genellikle 1 eleman)
# AI_Response.choices[0]: İlk (ve genellikle tek) yanıt
# AI_Response.choices[0].message: Mesaj nesnesi
# AI_Response.choices[0].message.content: Asistanın metin yanıtı
#
# Diğer faydalı bilgiler:
# - AI_Response.usage.prompt_tokens: Gönderilen prompt'un token sayısı
# - AI_Response.usage.completion_tokens: Üretilen yanıtın token sayısı
# - AI_Response.usage.total_tokens: Toplam kullanılan token

print(AI_Response.choices[0].message.content)


# ============================================================================
# ÖZET: OPENAI API KULLANIM ADIMLARI
# ============================================================================
# 1. Kütüphaneleri import et (openai, os, dotenv)
# 2. .env dosyasından API anahtarını yükle
# 3. OpenAI istemcisi oluştur
# 4. chat.completions.create() ile istek gönder
# 5. Yanıtı choices[0].message.content ile al
#
# MALIYET BİLGİSİ:
# ----------------
# - GPT-4 Turbo: ~$0.01 / 1K input token, ~$0.03 / 1K output token
# - GPT-3.5 Turbo: ~$0.0005 / 1K input token, ~$0.0015 / 1K output token
# - Güncel fiyatlar için: https://openai.com/pricing
# ============================================================================