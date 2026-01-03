# =====================================================================================
# VoiceDraw - Ses Kayıt Modülü (Recorder)
# =====================================================================================
# Bu modül, kullanıcının mikrofonundan ses kaydı yapar ve WAV formatında kaydeder.
# Kayıt işlemi ayrı bir thread'de çalışır, böylece Streamlit arayüzü donmaz.
#
# Teknik Detaylar:
# - Format: 16-bit PCM (Pulse Code Modulation)
# - Kanal Sayısı: 1 (Mono - tek kanal)
# - Örnekleme Hızı: 44100 Hz (CD kalitesi)
# - Buffer Boyutu: 1024 frame (düşük gecikme için optimize edilmiş)
#
# Çıktı Dosyası: voice_prompt.wav
#
# Kullanılan Kütüphane:
# - PyAudio: PortAudio kütüphanesinin Python bağlayıcısı
#   Mikrofon ve hoparlör erişimi için düşük seviyeli API sağlar
# =====================================================================================

# ===================
# KÜTÜPHANE İMPORTLARI
# ===================

# PyAudio - Ses giriş/çıkış işlemleri için ana kütüphane
# PortAudio C kütüphanesinin Python wrapper'ı olarak çalışır
# Kurulum: pip install pyaudio
# Not: Windows'ta pyaudio kurulumu için Microsoft Visual C++ Build Tools gerekebilir
import pyaudio

# Wave - WAV ses dosyası okuma/yazma için standart Python kütüphanesi
# WAV dosyaları sıkıştırmasız PCM verisi içerir (yüksek kalite, büyük boyut)
import wave


# =====================================================================================
# SES KAYIT FONKSİYONU
# =====================================================================================

def record(record_active, frames):
    """
    Mikrofondan ses kaydı yapan ana fonksiyon.
    
    Bu fonksiyon threading.Thread ile ayrı bir iş parçacığında çalışır,
    böylece Streamlit ana akışını engellemez (non-blocking).
    
    Kayıt Akışı:
    1. PyAudio nesnesi ve ses akışı (stream) oluşturulur
    2. record_active event'i aktif olduğu sürece ses verisi toplanır
    3. Event temizlendiğinde kayıt durur
    4. Toplanan veriler WAV dosyasına yazılır
    
    Args:
        record_active (threading.Event): Kayıt durumunu kontrol eden olay nesnesi
            - set() ile kayıt başlatılır
            - clear() ile kayıt durdurulur
            - is_set() ile durum kontrol edilir
            
        frames (list): Ses kaydı çerçevelerinin depolandığı liste
            - Her frame 1024 byte'lık ses verisi içerir
            - Ana uygulama ile paylaşılan mutable nesne
    """
    
    # ==========================================================================
    # PYAUDIO BAŞLATMA
    # ==========================================================================
    # PyAudio() nesnesi, PortAudio kütüphanesini başlatır ve
    # ses cihazlarına erişim sağlar. Bu nesne, stream'lerin yönetimi
    # ve ses formatlarının dönüştürülmesi için kullanılır.
    # ==========================================================================
    
    audio = pyaudio.PyAudio()

    # ==========================================================================
    # SES AKIŞI (STREAM) OLUŞTURMA
    # ==========================================================================
    # Stream, mikrofon ile uygulama arasındaki gerçek zamanlı ses bağlantısıdır.
    #
    # Parametreler:
    # - format: Ses verisi formatı
    #     paInt16: 16-bit signed integer (-32768 ile 32767 arası)
    #     CD kalitesi için yaygın kullanılan format
    #
    # - channels: Kanal sayısı
    #     1 = Mono (tek kanal)
    #     2 = Stereo (sol ve sağ kanal)
    #     Ses tanıma için mono yeterlidir ve dosya boyutunu yarıya indirir
    #
    # - rate: Örnekleme hızı (sample rate) - saniyede alınan örnek sayısı
    #     44100 Hz = CD kalitesi
    #     İnsan kulağı 20Hz-20kHz frekans aralığını duyar
    #     Nyquist teoremine göre 44100 Hz, 22050 Hz'e kadar sesi yakalayabilir
    #
    # - input: Giriş akışı mı?
    #     True = Mikrofon girişi (kayıt)
    #     False = Hoparlör çıkışı (oynatma)
    #
    # - frames_per_buffer: Buffer boyutu
    #     1024 frame = Her okumada işlenecek örnek sayısı
    #     Düşük değer: Daha az gecikme, daha fazla CPU kullanımı
    #     Yüksek değer: Daha fazla gecikme, daha az CPU kullanımı
    # ==========================================================================
    
    stream = audio.open(
        format=pyaudio.paInt16,  # 16-bit ses formatı
        channels=1,  # Mono kanal
        rate=44100,  # 44.1 kHz örnekleme
        input=True,  # Mikrofon girişi etkin
        frames_per_buffer=1024  # Buffer boyutu
    )

    # ==========================================================================
    # SES KAYIT DÖNGÜSÜ
    # ==========================================================================
    # record_active.is_set() True olduğu sürece ses verisi toplanır.
    # Bu döngü, ana uygulama stop butonuna basıp clear() çağırana kadar çalışır.
    #
    # stream.read():
    # - Belirtilen sayıda frame okur
    # - exception_on_overflow=False: Buffer taşması olursa hata fırlatma
    #   (Bu, kayıt sırasında küçük atlama olursa programın çökmesini önler)
    # ==========================================================================
    
    while record_active.is_set():
        # Mikrofondan 1024 frame ses verisi oku
        data = stream.read(1024, exception_on_overflow=False)
        # Okunan veriyi frames listesine ekle
        frames.append(data)

    # ==========================================================================
    # KAYNAK TEMİZLİĞİ (Resource Cleanup)
    # ==========================================================================
    # Kayıt döngüsü sona erdiğinde, kullanılan kaynakları düzgün şekilde
    # serbest bırakmak önemlidir. Bu işlem yapılmazsa:
    # - Mikrofon meşgul kalabilir
    # - Bellek sızıntısı oluşabilir
    # - Sistem kaynakları tükenir
    # ==========================================================================
    
    stream.stop_stream()  # Ses akışını durdur
    stream.close()  # Stream kaynaklarını serbest bırak
    audio.terminate()  # PyAudio'yu sonlandır ve PortAudio'yu kapat

    # ==========================================================================
    # WAV DOSYASI OLUŞTURMA
    # ==========================================================================
    # Toplanan ses verisini standart WAV formatında dosyaya yazıyoruz.
    # WAV formatı:
    # - Sıkıştırmasız PCM verisi (lossless)
    # - Evrensel uyumluluk (tüm ses yazılımları destekler)
    # - Whisper AI için ideal format
    #
    # Dosya yapısı:
    # - RIFF header: Dosya formatı bilgisi
    # - fmt chunk: Format bilgileri (kanal, örnekleme hızı, bit derinliği)
    # - data chunk: Ham ses verisi
    # ==========================================================================
    
    # WAV dosyasını yazma modunda (wb = write binary) aç
    sound_file = wave.open("voice_prompt.wav", "wb")
    
    # Kanal sayısını ayarla (1 = Mono)
    sound_file.setnchannels(1)
    
    # Örnek genişliğini ayarla (16-bit = 2 byte)
    # audio.get_sample_size(pyaudio.paInt16) = 2 byte döndürür
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    
    # Örnekleme hızını ayarla (44100 Hz)
    sound_file.setframerate(44100)
    
    # Tüm frame'leri birleştirip dosyaya yaz
    # b''.join(frames): Tüm binary parçaları tek bir bytes nesnesine birleştirir
    sound_file.writeframes(b''.join(frames))
    
    # Dosyayı kapat (değişiklikleri diske yaz)
    sound_file.close()