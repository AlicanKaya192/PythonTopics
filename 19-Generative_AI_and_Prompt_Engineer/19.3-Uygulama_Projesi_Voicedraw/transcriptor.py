# =====================================================================================
# VoiceDraw - Ses-Metin Dönüşüm Modülü (Transcriptor)
# =====================================================================================
# Bu modül, OpenAI Whisper API kullanarak ses dosyalarını metne dönüştürür.
# Speech-to-Text (STT) veya Automatic Speech Recognition (ASR) olarak da bilinir.
#
# Whisper Modeli Hakkında:
# - OpenAI tarafından geliştirilen çok dilli konuşma tanıma modeli
# - 680.000 saatlik farklı ses verisiyle eğitilmiştir
# - 99 farklı dili destekler (Türkçe dahil)
# - Gürültülü ortamlarda bile yüksek doğruluk sağlar
# - Aksanları ve lehçeleri anlayabilir
#
# API Kullanımı:
# - Maksimum dosya boyutu: 25 MB
# - Desteklenen formatlar: mp3, mp4, mpeg, mpga, m4a, wav, webm
# - Model: whisper-1 (şu an için tek seçenek)
#
# Çevre Değişkenleri:
# - openai_apikey: OpenAI API anahtarı
# =====================================================================================

# ===================
# KÜTÜPHANE İMPORTLARI
# ===================

# OpenAI Python SDK - Whisper API erişimi için
# Bu SDK, OpenAI'nin tüm API'lerine (GPT, DALL-E, Whisper vb.) erişim sağlar
from openai import OpenAI

# Çevre değişkenlerine erişim için standart Python kütüphanesi
import os

# .env dosyasından çevre değişkenlerini yüklemek için
# Bu sayede API anahtarları güvenli bir şekilde saklanabilir
from dotenv import load_dotenv

# =====================================================================================
# ÇEVRE DEĞİŞKENLERİNİ YÜKLE
# =====================================================================================
# load_dotenv() fonksiyonu şu sırayla .env dosyasını arar:
# 1. Mevcut çalışma dizini
# 2. Üst dizinler (proje köküne kadar)
#
# .env dosyası formatı:
# openai_apikey=sk-XXXXXXXXXXXXXXXXXXXX
#
# GÜVENLİK NOTU:
# - .env dosyasını asla git'e commit etmeyin
# - .gitignore dosyasına .env eklediğinizden emin olun
# =====================================================================================

load_dotenv()

# =====================================================================================
# OPENAI API YAPILANDIRMASI
# =====================================================================================
# API anahtarı çevre değişkeninden alınarak OpenAI istemcisi oluşturulur.
# Bu istemci, Whisper API dahil tüm OpenAI hizmetlerine erişim sağlar.
# =====================================================================================

# OpenAI API anahtarını çevre değişkeninden al
my_key_openai = os.getenv("openai_apikey")

# OpenAI istemci nesnesi oluştur
client = OpenAI(
    api_key=my_key_openai  # API anahtarını ayarla
)


# =====================================================================================
# WHİSPER İLE SES-METİN DÖNÜŞÜMÜ FONKSİYONU
# =====================================================================================

def transcribe_with_whisper(audio_file_name):
    """
    OpenAI Whisper API kullanarak ses dosyasını metne dönüştürür.
    
    Whisper Modeli Özellikleri:
    - Derin öğrenme tabanlı transformer mimarisi kullanır
    - End-to-end eğitilmiştir (ses → metin doğrudan dönüşüm)
    - Gürültü bastırma ve ses normalizasyonu yapar
    - Noktalama işaretlerini otomatik ekler
    - Konuşmacı tespiti yapabilir (diarization - opsiyonel)
    
    API Parametreleri:
    - model: Kullanılacak Whisper modeli ("whisper-1")
    - file: Dönüştürülecek ses dosyası (binary mod)
    - language: Hedef dil kodu (ISO 639-1 formatında)
    
    Dil Kodu Örnekleri:
    - "tr": Türkçe
    - "en": İngilizce
    - "de": Almanca
    - "fr": Fransızca
    - None: Otomatik dil tespiti (biraz daha yavaş)
    
    Args:
        audio_file_name (str): Dönüştürülecek ses dosyasının adı veya yolu
                               Örnek: "voice_prompt.wav"
        
    Returns:
        str: Ses dosyasından çıkarılan metin
             Noktalama işaretleri dahil, düzgün formatlanmış metin
    
    Örnek Kullanım:
        >>> text = transcribe_with_whisper("voice_prompt.wav")
        >>> print(text)
        "Merhaba, bugün hava çok güzel."
    """
    
    # ==========================================================================
    # SES DOSYASINI AÇ
    # ==========================================================================
    # Ses dosyası binary modda ("rb" = read binary) açılmalıdır.
    # Whisper API, dosya içeriğini doğrudan alır ve işler.
    # ==========================================================================
    
    audio_file = open(audio_file_name, "rb")  # Binary modda oku

    # ==========================================================================
    # WHİSPER API ÇAĞRISI
    # ==========================================================================
    # audio.transcriptions.create() metodu şu işlemleri yapar:
    # 1. Ses dosyasını OpenAI sunucularına yükler
    # 2. Whisper modeli ile ses tanıma yapar
    # 3. Tanınan metni döndürür
    #
    # Parametreler:
    # - model: "whisper-1" (şu an için tek model)
    # - file: Açılmış ses dosyası nesnesi
    # - language: Dil kodu (performansı artırır, isteğe bağlı)
    #
    # Not: language parametresi verilmezse, Whisper otomatik dil tespiti yapar.
    # Ancak dil biliniyorsa belirtmek:
    # - Tanıma doğruluğunu artırır
    # - İşlem süresini kısaltır
    # - Yanlış dil tespiti riskini ortadan kaldırır
    # ==========================================================================
    
    AI_generated_transcript = client.audio.transcriptions.create(
        model="whisper-1",  # Whisper modeli
        file=audio_file,  # Ses dosyası
        language="tr"  # Türkçe dil kodu
    )   

    # ==========================================================================
    # SONUCU DÖNDÜR
    # ==========================================================================
    # API yanıtı bir Transcription nesnesidir.
    # .text özelliği, tanınan metni string olarak içerir.
    # ==========================================================================
    
    return AI_generated_transcript.text  # Tanınan metni döndür