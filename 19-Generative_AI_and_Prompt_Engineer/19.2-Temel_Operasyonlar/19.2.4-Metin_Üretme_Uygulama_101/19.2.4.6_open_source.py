# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 5: Metin Üretme Uygulama 101
# 19.5.6 - Açık Kaynak Modeller ile Metin Üretimi (Replicate)
# ============================================================================
# Bu dosya, Replicate platformu üzerinden açık kaynak büyük dil
# modellerini (LLM) kullanarak metin üretmeyi göstermektedir.
#
# REPLICATE NEDİR?
# ----------------
# Replicate, açık kaynak AI modellerini cloud üzerinde çalıştıran
# bir platformdur. Avantajları:
# - GPU kurulumu gerektirmez
# - Binlerce hazır model mevcut
# - Kullandıkça öde modeli
# - Kolay API entegrasyonu
#
# AÇIK KAYNAK LLM'LER NEDEN ÖNEMLİ?
# ---------------------------------
# - Şeffaflık: Model ağırlıkları ve eğitim süreci açık
# - Özelleştirme: Fine-tuning yapılabilir
# - Gizlilik: Kendi sunucunuzda çalıştırabilirsiniz
# - Maliyet: Uzun vadede daha ekonomik olabilir
# - Bağımsızlık: Tek bir sağlayıcıya bağımlılık yok
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# replicate: Replicate API ile iletişim için Python kütüphanesi
# dotenv: .env dosyasından güvenli anahtar okuma
#
# NOT: replicate kütüphanesi, REPLICATE_API_TOKEN ortam değişkenini
# otomatik olarak okur. Bu nedenle os.getenv() kullanmaya gerek yok.

import replicate
from dotenv import load_dotenv


# ============================================================================
# 2. API YAPILANDIRMASI
# ============================================================================
# .env dosyasından Replicate API token'ını yükle
#
# .env dosyası örnek formatı:
# REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxxx
#
# Token almak için: https://replicate.com/account/api-tokens
#
# ÖNEMLİ: Replicate kütüphanesi, ortam değişkenini otomatik okur
# Değişken adı tam olarak "REPLICATE_API_TOKEN" olmalı

load_dotenv()


# ============================================================================
# 3. PROMPT VE SİSTEM PROMPTU TANIMLAMA
# ============================================================================
# prompt: Kullanıcının sorusu/isteği
# system_prompt: Modelin davranışını belirleyen talimat
#
# System prompt örnekleri:
# - "Sen yardımsever bir asistansın."
# - "Sen bir Python uzmanısın. Sadece kod örnekleri ver."
# - "Kısa ve öz cevaplar ver."

prompt = "Mevsimler nasıl oluşur?"
system_prompt = "Sen yardımsever bir asistansın."


# ============================================================================
# 4. LLAMA 2 70B CHAT MODELİ İLE METİN ÜRETİMİ
# ============================================================================
# LLAMA 2 NEDİR?
# --------------
# Meta (Facebook) tarafından geliştirilen açık kaynak LLM ailesi.
# - 7B, 13B, 70B parametre versiyonları mevcut
# - Chat versiyonları diyalog için optimize edilmiş
# - Araştırma ve ticari kullanım için ücretsiz
#
# replicate.run() PARAMETRELERI:
# ------------------------------
# İlk parametre: Model tanımlayıcısı (owner/model:version)
#   - "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"
#   - Format: "sahip/model_adı:versiyon_hash"
#
# input: Model girdileri (dictionary)
#   - temperature: Yaratıcılık seviyesi (0-1)
#   - max_new_tokens: Üretilecek maksimum token
#   - system_prompt: Sistem talimatı
#   - prompt: Kullanıcı mesajı
#   - debug: Hata ayıklama bilgisi

AI_Response = replicate.run(
    "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    input = {
        "temperature":0.5,
        "max_new_tokens": 256,
        "system_prompt": system_prompt,
        "prompt": prompt,
        "debug": False
    }
)


# ============================================================================
# 5. STREAMING YANITINI BİRLEŞTİRME
# ============================================================================
# Replicate API, yanıtı streaming olarak döndürür (parça parça).
# replicate.run() bir generator döndürür, her iterasyonda bir parça gelir.
# "".join() ile tüm parçaları birleştiriyoruz.
#
# Streaming avantajları:
# - Kullanıcıya daha hızlı ilk yanıt
# - Bellek verimliliği (tüm yanıtı beklemek yerine)
# - Gerçek zamanlı görüntüleme imkanı

AI_Response = "".join(AI_Response)

# Llama 2 yanıtını yazdır
print(AI_Response)
print("*"*100)  # Görsel ayırıcı


# ============================================================================
# 6. MIXTRAL 8X7B MODELİ İLE METİN ÜRETİMİ
# ============================================================================
# MIXTRAL NEDİR?
# --------------
# Mistral AI tarafından geliştirilen Mixture of Experts (MoE) modeli.
# Öne çıkan özellikleri:
# - 8 uzman ağı, her seferinde 2'si aktif
# - 46.7B toplam parametre, 12.9B aktif parametre
# - GPT-3.5'e yakın performans, daha düşük maliyet
# - Çok dilli yetenek
#
# MoE (Mixture of Experts) NEDİR?
# -------------------------------
# Farklı "uzman" alt ağları içeren mimari.
# Her girdi için en uygun uzmanlar seçilir.
# Sonuç: Daha az hesaplama ile daha yüksek performans.
#
# NOT: Mixtral'de system_prompt parametresi yok
# Sistem talimatı prompt içine dahil edilebilir

AI_Response = replicate.run(
    "mistralai/mixtral-8x7b-instruct-v0.1:7b3212fbaf88310cfef07a061ce94224e82efc8403c26fc67e8f6c065de51f21",
        input = {
        "temperature":0.5,
        "max_new_tokens": 256,
        "prompt": prompt,
        "debug": False
    }

)

# Streaming yanıtı birleştir
AI_Response = "".join(AI_Response)

# Mixtral yanıtını yazdır
print(AI_Response)


# ============================================================================
# REPLICATE'TE POPÜLER AÇIK KAYNAK MODELLER
# ============================================================================
#
# 1. METIN MODELLERİ:
#    - meta/llama-2-70b-chat: Meta'nın güçlü sohbet modeli
#    - mistralai/mixtral-8x7b-instruct-v0.1: Verimli MoE modeli
#    - mistralai/mistral-7b-instruct-v0.1: Küçük ama güçlü
#    - meta/llama-2-13b-chat: Dengeli performans/maliyet
#
# 2. GÖRSEL MODELLER:
#    - stability-ai/sdxl: Stable Diffusion XL
#    - stability-ai/stable-diffusion: SD 1.5/2.1
#
# 3. SES MODELLERİ:
#    - openai/whisper: Ses transkripsiyonu
#    - suno-ai/bark: Metin okuma (TTS)
#
# REPLICATE VS DİĞER PLATFORMLAR:
# -------------------------------
# | Platform   | Avantaj                  | Dezavantaj            |
# |------------|--------------------------|----------------------|
# | Replicate  | Kolay, çok model         | Sınırlı özelleştirme |
# | HuggingFace| Çok model, topluluk       | Daha teknik          |
# | RunPod     | Ucuz GPU, esneklik       | Kurulum gerekir      |
# | Modal      | Serverless, ölçeklenebilir| Öğrenme eğrisi       |
#
# MALİYET İPUÇLARI:
# -----------------
# - Replicate kullandıkça öder (saniye başına)
# - Küçük modeller (7B, 13B) daha ekonomik
# - Batch işlemler için kendi GPU'nuzu düşünün
# ============================================================================
