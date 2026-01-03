# =====================================================================================
# VoiceDraw - Sesli Çizim Uygulaması (Ana Modül)
# =====================================================================================
# Bu uygulama, kullanıcının sesli komutlarıyla görsel üretebilmesini sağlayan
# bir Streamlit tabanlı web uygulamasıdır. Temel iş akışı şöyledir:
#
# 1. Kullanıcı ses kaydı başlatır ve bir görsel tarifi yapar
# 2. Kayıt durdurulduğunda, ses Whisper AI ile metne dönüştürülür
# 3. Metin DALL-E 3 veya Gemini Vision ile görsel oluşturmak için kullanılır
# 4. Oluşturulan görsel kullanıcıya gösterilir ve indirilebilir
#
# Kullanılan Teknolojiler:
# - Streamlit: Web arayüzü framework'ü
# - OpenAI Whisper: Ses-metin dönüşümü (Speech-to-Text)
# - OpenAI DALL-E 3: Metin-görsel üretimi (Text-to-Image)
# - Google Gemini Vision: Görsel analizi ve prompt iyileştirme
# - PyAudio: Ses kaydı
# - Threading: Eş zamanlı ses kaydı işlemleri
# =====================================================================================

# ===================
# KÜTÜPHANE İMPORTLARI
# ===================

import streamlit as st  # Web uygulaması arayüzü için Streamlit framework'ü
import threading  # Çoklu iş parçacığı (multithread) desteği - ses kaydı için gerekli
import recorder  # Ses kaydı modülü (recorder.py) - mikrofon kayıt işlemleri
import transcriptor  # Ses-metin dönüşüm modülü (transcriptor.py) - Whisper API entegrasyonu
import painter  # Görsel üretim modülü (painter.py) - DALL-E & Gemini entegrasyonu
import time  # Zamanlama işlemleri için standart Python kütüphanesi

# =====================================================================================
# OTURUM DURUMU BAŞLATMA (Session State Initialization)
# =====================================================================================
# Streamlit'te session_state, sayfa yenilenmelerinde bile kullanıcı verilerini
# korumak için kullanılır. Bu özellikle interaktif uygulamalarda kritik öneme sahiptir.
#
# Session state değişkenleri:
# - record_active: Kayıt durumunu kontrol eden Event nesnesi (threading.Event)
# - recording_status: Kullanıcıya gösterilen durum mesajı
# - recording_completed: Kayıt tamamlandı mı kontrolü
# - latest_image: Son oluşturulan görsel dosya yolu (iteratif düzenleme için)
# - messages: Sohbet geçmişi (kullanıcı ve AI mesajları)
# - frames: Ses kaydı çerçeveleri (audio frames)
# =====================================================================================

if "record_active" not in st.session_state:
    # Threading.Event() - thread-safe bir bayrak/sinyal mekanizmasıdır
    # set() ile aktif, clear() ile pasif yapılır, is_set() ile kontrol edilir
    st.session_state.record_active = threading.Event()
    st.session_state.recording_status = "Başlamaya Hazırız!"  # Başlangıç durum mesajı
    st.session_state.recording_completed = False  # Kayıt henüz tamamlanmadı
    st.session_state.latest_image = ""  # Son oluşturulan görsel yolu (başlangıçta boş)
    st.session_state.messages = []  # Boş sohbet geçmişi listesi
    st.session_state.frames = []  # Boş ses kaydı çerçeveleri listesi


# =====================================================================================
# SES KAYDI FONKSİYONLARI
# =====================================================================================


def start_recording():
    """
    Ses kaydını başlatan fonksiyon.
    
    Bu fonksiyon şu işlemleri gerçekleştirir:
    1. record_active Event'ini aktif yapar (set)
    2. Önceki kayıt çerçevelerini temizler
    3. Durum mesajını günceller
    4. Yeni bir thread'de kayıt işlemini başlatır
    
    Threading kullanımı önemlidir çünkü ses kaydı blocking (engelleyici) bir işlemdir.
    Eğer ana thread'de çalıştırılırsa, Streamlit arayüzü donacaktır.
    """
    st.session_state.record_active.set()  # Kayıt bayrağını aktif et
    st.session_state.frames = []  # Önceki kayıt verilerini temizle
    st.session_state.recording_status = "🔴 **Sesiniz Kaydediliyor...**"  # Durum güncelle
    st.session_state.recording_completed = False  # Kayıt henüz tamamlanmadı

    # Yeni bir thread'de kayıt fonksiyonunu başlat
    # target: Çalıştırılacak fonksiyon
    # args: Fonksiyona geçirilecek argümanlar (tuple formatında)
    threading.Thread(
        target=recorder.record, 
        args=(st.session_state.record_active, st.session_state.frames)
    ).start()


def stop_recording():
    """
    Ses kaydını durduran fonksiyon.
    
    Bu fonksiyon şu işlemleri gerçekleştirir:
    1. record_active Event'ini pasif yapar (clear)
    2. Durum mesajını "Kayıt Tamamlandı" olarak günceller
    3. recording_completed bayrağını True yapar
    
    Not: clear() çağrıldığında, recorder.py'deki while döngüsü otomatik olarak durur
    ve kayıt dosyası (voice_prompt.wav) oluşturulur.
    """
    st.session_state.record_active.clear()  # Kayıt bayrağını pasif et
    st.session_state.recording_status = "✅ **Kayıt Tamamlandı!**"  # Durum güncelle
    st.session_state.recording_completed = True  # Kayıt tamamlandı bayrağı


# =====================================================================================
# STREAMLIT SAYFA YAPILANDIRMASI VE ARAYÜZ
# =====================================================================================
# set_page_config(): Sayfa başlığı, düzeni ve ikonu ayarlanır
# layout="wide": Tam genişlik düzeni kullanılır (daha geniş görüntü alanı)
# page_icon: Tarayıcı sekmesinde görünecek ikon
# =====================================================================================

st.set_page_config(
    page_title="VoiceDraw",  # Tarayıcı sekmesi başlığı
    layout="wide",  # Geniş sayfa düzeni
    page_icon="../assets/19.3-Materyaller/app_icon.png"  # Uygulama ikonu
)

# Üst banner görseli - uygulamanın tanıtım görseli
st.image(
    image="../assets/19.3-Materyaller/top_banner.png",  # Banner görsel yolu
    use_column_width=True  # Sütun genişliğine otomatik ölçekle
)

# Uygulama başlığı ve ayırıcı çizgi
st.title("VoiceDraw: Sesli Çizim")
st.divider()  # Yatay ayırıcı çizgi

# =====================================================================================
# KOLON DÜZENİ (Column Layout)
# =====================================================================================
# Streamlit'te st.columns() ile yan yana yerleşim oluşturulur.
# [1,4] oranı: Sol sütun 1 birim, sağ sütun 4 birim genişliğinde
# Bu düzen, ses kontrolleri (sol) ve görsel çıktıları (sağ) ayırır.
# =====================================================================================

col_audio, col_image = st.columns([1, 4])

# =====================================================================================
# SOL SÜTUN: SES KAYIT KONTROLLERİ
# =====================================================================================

with col_audio:
    st.subheader("Ses Kayıt")  # Alt başlık
    st.divider()
    
    # Kayıt durumunu gösteren bilgi kutusu
    status_message = st.info(st.session_state.recording_status)
    st.divider()

    # Alt kolonlar: Butonlar (sol) ve ses çalar (sağ)
    subcol_left, subcol_right = st.columns([1, 2])

    with subcol_left:
        # Başlat butonu - kayıt aktifken devre dışı
        start_btn = st.button(
            label="Başlat", 
            on_click=start_recording,  # Tıklandığında çağrılacak fonksiyon
            disabled=st.session_state.record_active.is_set()  # Kayıt aktifse devre dışı
        )
        # Durdur butonu - kayıt pasifken devre dışı
        stop_btn = st.button(
            label="Durdur", 
            on_click=stop_recording, 
            disabled=not st.session_state.record_active.is_set()  # Kayıt pasifse devre dışı
        )
    
    with subcol_right:
        # Ses çalar widget'ı için placeholder (dinamik güncelleme için)
        recorded_audio = st.empty()

        # Kayıt tamamlandıysa ses dosyasını oynat
        if st.session_state.recording_completed:
            with st.spinner("Dosya Hazırlanıyor..."):
                time.sleep(1)  # Dosya yazımı için kısa bekleme
                recorded_audio.audio(data="voice_prompt.wav")  # Ses dosyasını çal

    st.divider()
    
    # Son resmi kullan checkbox'ı - iteratif görsel düzenleme için
    # Bu seçenek etkinleştirilirse, önceki görsel üzerinde değişiklik yapılır
    latest_image_use = st.checkbox(label="Son Resmi Kullan")

# =====================================================================================
# SAĞ SÜTUN: GÖRSEL ÇIKTILAR VE SOHBET GEÇMİŞİ
# =====================================================================================

with col_image:
    st.subheader("Görsel Çıktılar")  # Alt başlık
    st.divider()

    # =========================================================================
    # SOHBET GEÇMİŞİ GÖSTERİMİ
    # =========================================================================
    # Daha önce oluşturulan tüm mesajları göster (sayfa yenilendiğinde bile)
    # Her mesaj için uygun avatar ve içerik formatı kullanılır
    # =========================================================================
    
    for message in st.session_state.messages:

        if message["role"] == "assistant":
            # AI (asistan) mesajı - oluşturulan görseli göster
            with st.chat_message(
                name=message["role"], 
                avatar="../assets/19.3-Materyaller/ai_avatar.png"  # AI avatarı
            ):
                st.warning("İşte Sizin İçin Oluşturduğum Görsel:")
                st.image(image=message["content"], width=300)  # Görsel 300px genişlikte
        
        elif message["role"] == "user":
            # Kullanıcı mesajı - sesli komutu göster
            with st.chat_message(
                name=message["role"], 
                avatar="../assets/19.3-Materyaller/user_avatar.png"  # Kullanıcı avatarı
            ):
                st.success(message["content"])  # Yeşil başarı kutusu

    # =========================================================================
    # YENİ GÖRSEL OLUŞTURMA AKIŞI
    # =========================================================================
    # Durdur butonuna tıklandığında:
    # 1. Ses dosyası Whisper ile metne dönüştürülür
    # 2. Metin DALL-E veya Gemini+DALL-E ile görsele dönüştürülür
    # 3. Görsel gösterilir ve indirme butonu sunulur
    # =========================================================================
    
    if stop_btn:
        # Kullanıcı mesajı bubbles'ı oluştur
        with st.chat_message(
            name="user", 
            avatar="../assets/19.3-Materyaller/user_avatar.png"
        ):
            # Ses-metin dönüşümü (Speech-to-Text)
            with st.spinner("Sesiniz Çözümleniyor..."):
                voice_prompt = transcriptor.transcribe_with_whisper(
                    audio_file_name="voice_prompt.wav"
                )
            st.success(voice_prompt)  # Dönüştürülen metni göster

        # Kullanıcı mesajını sohbet geçmişine ekle
        st.session_state.messages.append({"role": "user", "content": voice_prompt})

        # AI yanıt bubble'ı oluştur
        with st.chat_message(
            name="assistant", 
            avatar="../assets/19.3-Materyaller/ai_avatar.png"
        ):
            st.warning("İşte Sizin İçin Oluşturduğum Görsel:")
            
            # Görsel oluşturma işlemi
            with st.spinner("Görseliniz Oluşturuluyor..."):
                if latest_image_use:
                    # ===========================================================
                    # İTERATİF DÜZENLEME MODU
                    # ===========================================================
                    # Son oluşturulan görsel üzerinde değişiklik yapar.
                    # Bu mod şu şekilde çalışır:
                    # 1. Gemini Vision ile mevcut görsel analiz edilir
                    # 2. Kullanıcının sesli komutu ile birleştirilir
                    # 3. DALL-E ile yeni görsel oluşturulur
                    # ===========================================================
                    image_file_name = painter.generate_image(
                        image_path=st.session_state.latest_image, 
                        prompt=voice_prompt
                    )
                else:
                    # ===========================================================
                    # SIFIRDAN OLUŞTURMA MODU
                    # ===========================================================
                    # Doğrudan DALL-E 3 ile yeni görsel oluşturur.
                    # Sadece kullanıcının sesli komutu kullanılır.
                    # ===========================================================
                    image_file_name = painter.generate_image_with_dalle(
                        prompt=voice_prompt
                    )

            # Oluşturulan görseli göster
            st.image(image=image_file_name, width=300)

            # Görsel indirme butonu
            with open(image_file_name, "rb") as file:
                st.download_button(
                    label="Resmi İndir",
                    data=file,
                    file_name=image_file_name,  # İndirilecek dosya adı
                    mime="image/png"  # MIME tipi
                )

        # AI mesajını sohbet geçmişine ekle
        st.session_state.messages.append({"role": "assistant", "content": image_file_name})
        
        # Son görseli kaydet (iteratif düzenleme için)
        st.session_state.latest_image = image_file_name