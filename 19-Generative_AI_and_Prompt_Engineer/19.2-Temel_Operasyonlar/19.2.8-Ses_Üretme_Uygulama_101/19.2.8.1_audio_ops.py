# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 8: Ses Üretme Uygulama 101
# 19.2.8.1 - AI ile Ses İşlemleri (TTS, STT, Çeviri)
# ============================================================================
# Bu dosya, farklı AI ses API'leri kullanarak:
# - Metinden ses üretme (Text-to-Speech / TTS)
# - Sesten metin çıkarma (Speech-to-Text / STT / Transkripsiyon)
# - Sesli çeviri (Audio Translation)
# işlemlerini Streamlit arayüzü ile göstermektedir.
#
# SES YAPAY ZEKASI TEKNOLOJİLERİ
# ==============================
# 1. TTS (Text-to-Speech) - Metin Okuma:
#    - Metni doğal insan sesine dönüştürme
#    - Farklı ses karakterleri (erkek, kadın, vs.)
#    - Duygu ve tonlama desteği
#    - Kullanım: Sesli asistan, podcast, erişilebilirlik
#
# 2. STT (Speech-to-Text) - Ses Tanıma:
#    - Konuşmayı metne dönüştürme
#    - Çoklu dil desteği
#    - Gürültü filtreleme
#    - Kullanım: Transkripsiyon, sesli komut, altyazı
#
# 3. Ses Çevirisi (Audio Translation):
#    - Farklı dildeki konuşmayı İngilizce'ye çevirme
#    - Tek adımda transkripsiyon + çeviri
#    - Whisper modeli ile gerçekleştirilir
#
# KULLANILAN MODELLER
# ===================
# 1. OpenAI TTS-1:
#    - Yüksek kaliteli metin okuma
#    - 6 farklı ses karakteri
#    - Düşük gecikme süresi
#
# 2. OpenAI Whisper:
#    - Açık kaynak STT modeli
#    - 99+ dil desteği
#    - Gürültüye dayanıklı
#    - Transkripsiyon + Çeviri
#
# 3. AssemblyAI Conformer:
#    - Yüksek doğruluk oranı
#    - Gerçek zamanlı transkripsiyon
#    - Konuşmacı ayrımı (diarization)
#    - Duygu analizi desteği
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# OpenAI: TTS ve Whisper API erişimi için
# assemblyai: AssemblyAI Conformer modeli için
# streamlit: Web arayüzü oluşturmak için
# os: Ortam değişkenlerine erişim ve dosya işlemleri
# dotenv: .env dosyasından API anahtarlarını okumak için

from openai import OpenAI
import assemblyai as aai
import streamlit as st
import os
from dotenv import load_dotenv


# ============================================================================
# 2. API YAPILANDIRMASI
# ============================================================================
# İki farklı API için anahtar yükleme:
# - OpenAI: TTS-1 ve Whisper modelleri için
# - AssemblyAI: Conformer modeli için
#
# .env dosyası örnek formatı:
# openai_apikey=sk-xxxxxxxxxxxxxxxxxxxxx
# assemblyai_apikey=xxxxxxxxxxxxxxxxxxxxx
#
# API anahtarları almak için:
# - OpenAI: https://platform.openai.com/api-keys
# - AssemblyAI: https://www.assemblyai.com/app/account

load_dotenv()

my_key_openai = os.getenv("openai_apikey")
my_key_assemblyai = os.getenv("assemblyai_apikey")


# ============================================================================
# 3. OPENAI İSTEMCİSİ OLUŞTURMA
# ============================================================================
# TTS ve Whisper API çağrıları için OpenAI istemcisi

client = OpenAI(
    api_key=my_key_openai
)


# ============================================================================
# 4. SES DOSYASI KAYIT YOLU
# ============================================================================
# Üretilen ses dosyaları assets klasörüne kaydedilir
# 19.2.8 klasöründen assets'e relatif yol: ../../assets/

SPEECH_OUTPUT_PATH = "../../assets/speech.mp3"


# ============================================================================
# 5. TTS (TEXT-TO-SPEECH) FONKSİYONU
# ============================================================================
# OpenAI TTS-1 modeli ile metinden ses üretme
#
# client.audio.speech.create() PARAMETRELER:
# ------------------------------------------
# model: Kullanılacak TTS modeli
#   - "tts-1": Standart model (daha hızlı, düşük gecikme)
#   - "tts-1-hd": Yüksek kalite (daha yavaş, daha net ses)
#
# voice: Ses karakteri seçimi
#   - "alloy": Nötr, dengeli ses
#   - "echo": Erkek, derin ses
#   - "fable": İngiliz aksanı, hikaye anlatıcı
#   - "onyx": Erkek, otoriteler ses
#   - "nova": Kadın, canlı ses
#   - "shimmer": Kadın, yumuşak ses
#
# response_format: Çıktı ses formatı
#   - "mp3": En yaygın format (varsayılan)
#   - "opus": Düşük gecikme streaming için
#   - "aac": Dijital ses için optimize
#   - "flac": Kayıpsız sıkıştırma
#
# input: Seslendirilecek metin (max 4096 karakter)
#
# ÇIKTI:
# ------
# stream_to_file(): Ses verisini direkt dosyaya yazar
# Alternatif: response.content ile binary veri alınabilir

def create_speech_from_text(prompt, speech_file_name, voice_type="alloy"):
    """
    Metni OpenAI TTS-1 modeli ile sese dönüştürür.
    
    Args:
        prompt (str): Seslendirilecek metin
        speech_file_name (str): Çıktı dosya yolu
        voice_type (str): Ses karakteri (alloy, echo, fable, onyx, nova, shimmer)
        
    Returns:
        str: İşlem durumu mesajı
    """
    # TTS API çağrısı
    AI_Response = client.audio.speech.create(
        model="tts-1",
        voice=voice_type,
        response_format="mp3",
        input=prompt
    )

    # Ses verisini dosyaya kaydet
    # stream_to_file(): Binary veriyi direkt dosyaya yazar
    AI_Response.stream_to_file(speech_file_name)

    return "Seslendirme İşlemi Tamamlandı"


# ============================================================================
# 6. WHISPER TRANSKRİPSİYON FONKSİYONU
# ============================================================================
# OpenAI Whisper modeli ile sesten metin çıkarma (STT)
#
# WHISPER MODEL ÖZELLİKLERİ:
# --------------------------
# - OpenAI tarafından geliştirilen açık kaynak model
# - 680.000 saat veri ile eğitilmiş
# - 99+ dil desteği
# - Gürültüye ve aksanlara dayanıklı
# - Noktalama ve büyük/küçük harf otomatik
#
# client.audio.transcriptions.create() PARAMETRELER:
# --------------------------------------------------
# model: "whisper-1" (şu an tek seçenek)
# file: Ses dosyası (binary modda açılmış)
# language: ISO 639-1 dil kodu (opsiyonel)
#   - "tr": Türkçe
#   - "en": İngilizce
#   - Belirtilmezse otomatik algılar
#
# Desteklenen formatlar: mp3, mp4, mpeg, mpga, m4a, wav, webm
# Maksimum dosya boyutu: 25 MB

def transcribe_with_whisper(audio_file_name):
    """
    Ses dosyasını Whisper modeli ile metne dönüştürür.
    
    Args:
        audio_file_name (str): Ses dosyası yolu
        
    Returns:
        str: Transkripsiyon metni
    """
    # Ses dosyasını binary modda aç
    audio_file = open(audio_file_name, "rb")

    # Transkripsiyon API çağrısı
    AI_generated_transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="tr"  # Türkçe olarak belirtildi
    )

    # Transkripsiyon metnini döndür
    return AI_generated_transcript.text


# ============================================================================
# 7. WHISPER ÇEVİRİ FONKSİYONU
# ============================================================================
# Farklı dildeki sesi İngilizce metne çevirme
#
# TRANSKRİPSİYON VS ÇEVİRİ:
# -------------------------
# - Transkripsiyon: Ses → Aynı dilde metin
# - Çeviri: Ses → İngilizce metin
#
# ÖNEMLİ: Çeviri sadece İngilizce'ye yapılabilir!
# Diğer dillere çeviri için ek bir çeviri API'si gerekir.
#
# client.audio.translations.create() PARAMETRELER:
# ------------------------------------------------
# model: "whisper-1"
# file: Ses dosyası (binary modda)
# 
# Not: language parametresi yok - otomatik algılar ve İngilizce'ye çevirir

def translate_with_whisper(audio_file_name):
    """
    Ses dosyasını Whisper modeli ile İngilizce'ye çevirir.
    
    Args:
        audio_file_name (str): Ses dosyası yolu
        
    Returns:
        str: İngilizce çeviri metni
    """
    # Ses dosyasını binary modda aç
    audio_file = open(audio_file_name, "rb")

    # Çeviri API çağrısı
    AI_generated_translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )

    # Çeviri metnini döndür
    return AI_generated_translation.text


# ============================================================================
# 8. ASSEMBLYAI CONFORMER TRANSKRİPSİYON FONKSİYONU
# ============================================================================
# AssemblyAI'nin Conformer modeli ile transkripsiyon
#
# CONFORMER MODEL ÖZELLİKLERİ:
# ----------------------------
# - Convolution + Transformer hibrit mimarisi
# - Yüksek doğruluk oranı
# - Gerçek zamanlı transkripsiyon desteği
# - Ek özellikler:
#   - Speaker Diarization (konuşmacı ayrımı)
#   - Sentiment Analysis (duygu analizi)
#   - Entity Detection (varlık tespiti)
#   - Auto Chapters (otomatik bölümleme)
#
# ASSEMBLYAI VS WHISPER:
# ----------------------
# | Özellik          | Whisper         | AssemblyAI       |
# |------------------|-----------------|------------------|
# | Maliyet          | Token başına    | Dakika başına    |
# | Gerçek zamanlı   | Hayır           | Evet             |
# | Konuşmacı ayrımı | Hayır           | Evet             |
# | Duygu analizi    | Hayır           | Evet             |
# | Açık kaynak      | Evet            | Hayır            |
#
# aai.Transcriber() KULLANIMI:
# ----------------------------
# 1. API anahtarını ayarla
# 2. Transcriber nesnesi oluştur
# 3. transcribe() metoduyla dosya yolunu gönder

def transcribe_with_conformer(audio_file_name):
    """
    Ses dosyasını AssemblyAI Conformer modeli ile metne dönüştürür.
    
    Args:
        audio_file_name (str): Ses dosyası yolu
        
    Returns:
        str: Transkripsiyon metni
    """
    # AssemblyAI API anahtarını ayarla
    aai.settings.api_key = my_key_assemblyai
    
    # Transcriber nesnesi oluştur
    transcriber = aai.Transcriber()

    # Transkripsiyon işlemi
    # Not: Bu işlem asenkron olarak sunucuda gerçekleşir
    AI_generated_text = transcriber.transcribe(audio_file_name)

    # Transkripsiyon metnini döndür
    return AI_generated_text.text


# ============================================================================
# 9. STREAMLIT ARAYÜZÜ - SEKMELER
# ============================================================================
# Dört farklı işlem için sekmeli arayüz:
# 1. TTS ile Ses Sentezleme: Metin → Ses
# 2. Whisper ile Transkripsiyon: Ses → Metin (aynı dil)
# 3. Whisper ile Tercüme: Ses → İngilizce metin
# 4. Conformer ile Transkripsiyon: Ses → Metin (AssemblyAI)

tab_TTS, tab_whisper, tab_translation, tab_conformer = st.tabs(
    [
     "TTS ile Ses Sentezleme", 
     "Whisper ile Transkripsiyon", 
     "Whisper ile Tercüme", 
     "Conformer ile Transkripsiyon"
     ]
)


# ============================================================================
# 9.1 TAB 1: TTS İLE SES SENTEZLEME
# ============================================================================
# Kullanıcıdan metin ve ses tercihi alır, TTS ile sese dönüştürür

with tab_TTS:
    st.subheader("TTS-1 Modeli ile Konuşma Sentezleme")
    st.divider()

    # Metin giriş alanı
    prompt = st.text_input("Seslendirmek istediğiniz metni giriniz", key="prompt_tts")
    
    # Ses karakteri seçimi
    # OpenAI'nin sunduğu 6 farklı ses karakteri
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    voice_type = st.selectbox(label="Ses tercihiniz:", options=voices, key="voice_tts")
    
    # Sentezle butonu
    generate_btn = st.button("Ses Sentezle", key="button_tts")

    # Butona tıklandığında ses üret
    if generate_btn:
        # TTS işlemini gerçekleştir ve dosyaya kaydet
        status = create_speech_from_text(
            prompt=prompt, 
            speech_file_name=SPEECH_OUTPUT_PATH,  # assets klasörüne kaydet
            voice_type=voice_type
        )
        st.success(status)

        # Üretilen ses dosyasını oku ve oynat
        audio_file = open(SPEECH_OUTPUT_PATH, "rb")
        audio_bytes = audio_file.read()

        # Ses oynatıcı bileşeni
        st.audio(data=audio_bytes, format="audio/mp3")
        
        # Başarı animasyonu
        st.balloons()


# ============================================================================
# 9.2 TAB 2: WHISPER İLE TRANSKRİPSİYON
# ============================================================================
# Kullanıcının yüklediği ses dosyasını metne dönüştürür

with tab_whisper:
    st.subheader("Whisper Modeli ile Transkripsiyon")
    st.divider()

    # Dosya yükleme bileşeni
    selected_file = st.file_uploader("Bir ses dosyası seçiniz", type=["mp3"], key="file_whisper")

    # Dosya yüklendiyse önizleme göster
    if selected_file:
        # Yüklenen dosyayı geçici olarak kaydet
        temp_path = f"../../assets/temp_{selected_file.name}"
        with open(temp_path, "wb") as f:
            f.write(selected_file.getbuffer())
        
        # Ses dosyasını oynat
        audio_file = open(temp_path, "rb")
        audio_bytes = audio_file.read()
        st.audio(data=audio_bytes, format="audio/mp3")

    # Metne dönüştür butonu
    transcribe_btn = st.button("Metne Dönüştür", key="button_whisper")

    # Butona tıklandığında transkripsiyon yap
    if transcribe_btn:
        if selected_file:
            temp_path = f"../../assets/temp_{selected_file.name}"
            generated_text = transcribe_with_whisper(audio_file_name=temp_path)

            st.divider()
            # st.info(): Mavi arka planlı bilgi kutusu
            st.info(f"TRANSKRİPSİYON: {generated_text}")
            st.balloons()
        else:
            st.warning("Lütfen önce bir ses dosyası yükleyiniz!")


# ============================================================================
# 9.3 TAB 3: WHISPER İLE TERCÜME
# ============================================================================
# Kullanıcının yüklediği ses dosyasını İngilizce'ye çevirir

with tab_translation:
    st.subheader("Whisper Modeli ile Tercüme")
    st.divider()

    # Dosya yükleme bileşeni
    selected_file = st.file_uploader("Bir ses dosyası seçiniz", type=["mp3"], key="file_translation")

    # Dosya yüklendiyse önizleme göster
    if selected_file:
        # Yüklenen dosyayı geçici olarak kaydet
        temp_path = f"../../assets/temp_{selected_file.name}"
        with open(temp_path, "wb") as f:
            f.write(selected_file.getbuffer())
        
        # Ses dosyasını oynat
        audio_file = open(temp_path, "rb")
        audio_bytes = audio_file.read()
        st.audio(data=audio_bytes, format="audio/mp3")

    # Tercüme et butonu
    translate_btn = st.button("Tercüme Et", key="button_translation")

    # Butona tıklandığında çeviri yap
    if translate_btn:
        if selected_file:
            temp_path = f"../../assets/temp_{selected_file.name}"
            translated_text = translate_with_whisper(audio_file_name=temp_path)

            st.divider()
            st.info(f"TERCÜME (İngilizce): {translated_text}")
            st.balloons()
        else:
            st.warning("Lütfen önce bir ses dosyası yükleyiniz!")


# ============================================================================
# 9.4 TAB 4: CONFORMER İLE TRANSKRİPSİYON
# ============================================================================
# AssemblyAI Conformer modeli ile transkripsiyon

with tab_conformer:
    st.subheader("Conformer Modeli ile Transkripsiyon")
    st.divider()

    # Dosya yükleme bileşeni
    selected_file = st.file_uploader("Bir ses dosyası seçiniz", type=["mp3"], key="file_conformer")

    # Dosya yüklendiyse önizleme göster
    if selected_file:
        # Yüklenen dosyayı geçici olarak kaydet
        temp_path = f"../../assets/temp_{selected_file.name}"
        with open(temp_path, "wb") as f:
            f.write(selected_file.getbuffer())
        
        # Ses dosyasını oynat
        audio_file = open(temp_path, "rb")
        audio_bytes = audio_file.read()
        st.audio(data=audio_bytes, format="audio/mp3")

    # Metne dönüştür butonu
    transcribe_btn = st.button("Metne Dönüştür", key="button_conformer")

    # Butona tıklandığında transkripsiyon yap
    if transcribe_btn:
        if selected_file:
            temp_path = f"../../assets/temp_{selected_file.name}"
            generated_text = transcribe_with_conformer(audio_file_name=temp_path)

            st.divider()
            st.info(f"TRANSKRİPSİYON: {generated_text}")
            st.balloons()
        else:
            st.warning("Lütfen önce bir ses dosyası yükleyiniz!")


# ============================================================================
# ÖZET: SES AI API'LERİ KARŞILAŞTIRMASI
# ============================================================================
#
# TTS (Metin → Ses):
# ------------------
# | Model         | Kalite  | Hız    | Maliyet        |
# |---------------|---------|--------|----------------|
# | OpenAI TTS-1  | Yüksek  | Hızlı  | $0.015/1K char |
# | OpenAI TTS-HD | Çok Yük.| Orta   | $0.030/1K char |
# | ElevenLabs    | Premium | Hızlı  | $0.30/1K char  |
# | Google TTS    | İyi     | Hızlı  | $0.004/1K char |
#
# STT (Ses → Metin):
# ------------------
# | Model         | Doğruluk | Özellikler         | Maliyet        |
# |---------------|----------|-------------------|----------------|
# | Whisper       | %95+     | 99+ dil           | $0.006/dakika  |
# | AssemblyAI    | %97+     | Diarization, NER  | $0.00025/saniye|
# | Google STT    | %95+     | Gerçek zamanlı    | $0.006/15 san  |
# | AWS Transcribe| %93+     | Medikal, Hukuk    | $0.024/dakika  |
#
# SES KALITESI İÇIN İPUÇLARI:
# ---------------------------
# 1. TTS için net ve düzgün cümleler kullanın
# 2. STT için gürültüsüz ses kayıtları tercih edin
# 3. Uzun dosyaları parçalara bölerek işleyin
# 4. Dil parametresini her zaman belirtin (varsa)
# ============================================================================