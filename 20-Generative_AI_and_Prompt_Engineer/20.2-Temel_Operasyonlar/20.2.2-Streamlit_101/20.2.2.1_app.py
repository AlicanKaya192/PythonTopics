# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 1: Streamlit ile Hızlı Prototipleme
# Streamlit 101 - Temel Kavramlar ve Uygulamalar
# ============================================================================
# Bu dosya, Streamlit framework'ü ile web uygulaması geliştirmenin
# temel kavramlarını ve bileşenlerini içermektedir.
# Streamlit, Python ile hızlı ve etkileşimli web uygulamaları
# oluşturmak için kullanılan güçlü bir araçtır.
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# Streamlit: Python ile web uygulaması geliştirmek için kullanılan framework
# json: JSON formatında veri okuma/yazma işlemleri için standart kütüphane

import streamlit as st
import json

# ============================================================================
# 2. SAYFA YAPILANDIRMA AYARLARI
# ============================================================================
# set_page_config(): Streamlit sayfasının temel ayarlarını yapılandırır
# - page_title: Tarayıcı sekmesinde görünecek başlık
# - page_icon: Tarayıcı sekmesinde görünecek ikon (emoji veya resim dosyası)
# Not: Bu fonksiyon, Streamlit uygulamasında ilk çağrılan komut olmalıdır

st.set_page_config(page_title="Steamlit 101", page_icon=":robot_face:")


# ============================================================================
# 3. METİN GÖSTERME YÖNTEMLERİ (Örnekler - Yorum Satırında)
# ============================================================================
# Streamlit'te metin göstermek için çeşitli fonksiyonlar kullanılabilir:
#
# st.write()     : En yaygın metin gösterme yöntemi, çoğu veri tipini destekler
# st.markdown()  : Markdown formatında biçimlendirilmiş metin gösterir
# st.header()    : Büyük başlık oluşturur (H1)
# st.subheader() : Alt başlık oluşturur (H2)
# st.code()      : Kod blokları gösterir (syntax highlighting ile)
# st.latex()     : LaTeX formatında matematiksel formüller gösterir

# st.write("En yaygın metin gösterme yöntemi")
# st.markdown("_Biçimlendirilmiş Metin_")
# st.header("Bu bir header örneği")
# st.subheader("Bu ise bir subheader örneği")
# st.code('for i in range(10): my_function()')
# st.latex(r''' e^{i\pi} + 1 = 0 ''')


# ============================================================================
# 4. MULTIMEDYA GÖSTERME YÖNTEMLERİ (Örnekler - Yorum Satırında)
# ============================================================================
# Streamlit ile resim, video ve ses dosyaları gösterilebilir:
#
# st.image() : PNG, JPG, GIF vb. resim dosyalarını gösterir
# st.video() : MP4, WebM vb. video dosyalarını oynatır
# st.audio() : MP3, WAV vb. ses dosyalarını oynatır
#
# Dosya Yolları:
# - Görsel ve video dosyaları: ../assets/ klasöründe bulunur
# - Relatif yol kullanılarak erişim sağlanır

# st.image(image="../../assets/1-image_sample.png")
# st.video(data="../../assets/2-video_sample.mp4")
# st.audio(data="../../assets/3-audio_sample.mp3")


# ============================================================================
# 5. KULLANICI ETKİLEŞİM BİLEŞENLERİ (Örnekler - Yorum Satırında)
# ============================================================================
# Streamlit, kullanıcıdan veri almak için çeşitli widget'lar sunar:
#
# st.text_input()   : Metin girişi alanı (şifre için type="password")
# st.checkbox()     : İşaretleme kutusu (boolean değer döner)
# st.number_input() : Sayısal değer girişi (min/max değerleri ayarlanabilir)
# st.slider()       : Kaydırıcı ile değer seçimi
# st.radio()        : Radyo butonları ile tek seçim
# st.button()       : Tıklanabilir buton
# st.file_uploader(): Dosya yükleme bileşeni
# st.divider()      : Görsel ayraç çizgisi

# st.write("Lütfen Bilgilerinizi Girin")
# st.text_input(label="Lütfen e-posta adresinizi giriniz:")
# st.text_input(label="Lütfen şifrenizi giriniz:", type="password")
# st.checkbox(label="Şifremi Unuttum")
# st.divider()
# st.number_input(label="Lütfen yaşınızı giriniz:", min_value=18, max_value=40, value=22)
# st.slider(label="Lütfen yaşınızı giriniz:", min_value=18, max_value=40, value=22)
# st.divider()
# st.radio(label="Statünüz Nedir?", options=["Öğrenci", "Mezun"])
# st.button(label="Giriş Yap")
# st.divider()
# st.file_uploader(label="Dosya Yüklemek İçin Tıklayınız")


# ============================================================================
# 6. ARAYÜZ YERLEŞİM BİLEŞENLERİ (Örnekler - Yorum Satırında)
# ============================================================================
# Streamlit ile sayfa düzeni oluşturmak için kullanılan bileşenler:
#
# st.sidebar    : Yan menü alanı (sol tarafta sabit panel)
# st.tabs()     : Sekmeli içerik alanları
# st.columns()  : Yan yana sütunlar (burada kullanılmamış)
# st.container(): İçerik gruplandırma alanı (burada kullanılmamış)
# st.expander() : Açılır/kapanır bölümler (burada kullanılmamış)

# st.sidebar.markdown("<h4>Uygulamamıza Hoşgeldin!</h4>", unsafe_allow_html=True)
# st.sidebar.image("../../assets/1-image_sample.png")
# tab1, tab2 = st.tabs(["Kullanıcı Bilgileri", "Kullanım Tercihleri"])
# with tab1:
#     st.text_input(label="E-Posta Adresinizi Giriniz:")
#     st.text_input(label="Şifrenizi Giriniz", type="password")
#     st.checkbox(label="Şifremi Unuttum")
#     st.divider()
#     st.button(label="Kaydet")
# with tab2:
#     st.radio(label="Hesap Türü", options=["Öğrenci", "Mezun"])
#     st.slider(label="Zaman Aşımı Süresi (saniye)", min_value=3, max_value=30, value=5)
#     st.file_uploader(label="Güncel Özgeçmişinizi Yükleyiniz")


# ============================================================================
# 7. PROGRAM AKIŞI İLE BİLEŞEN ENTEGRASYONU - AKTİF KOD BÖLÜMÜ
# ============================================================================
# Bu bölüm, Streamlit bileşenlerinin birlikte nasıl çalıştığını gösterir.
# Kullanıcı girdilerini alıp, işleyip, dosyaya kaydeden tam bir uygulama örneği.

# ----------------------------------------------------------------------------
# 7.1 SIDEBAR (YAN MENÜ) OLUŞTURMA
# ----------------------------------------------------------------------------
# st.sidebar: Sol tarafta sabit kalan panel alanı
# - Genellikle navigasyon, logo veya genel bilgiler için kullanılır
# - unsafe_allow_html=True: HTML etiketlerinin yorumlanmasını sağlar

st.sidebar.markdown("<h4>Uygulamamıza Hoşgeldin!</h4>", unsafe_allow_html=True)

# Sidebar'a görsel ekleme
# Not: Görsel dosyası ../assets/ klasöründen yüklenir
st.sidebar.image("../../assets/1-image_sample.png")


# ----------------------------------------------------------------------------
# 7.2 SEKMELER (TABS) OLUŞTURMA
# ----------------------------------------------------------------------------
# st.tabs(): Sayfa içinde sekmeli içerik alanları oluşturur
# - Her sekme bağımsız bir içerik alanı sunar
# - with bloğu kullanılarak sekme içerikleri tanımlanır

tab1, tab2 = st.tabs(["Kullanıcı Bilgileri", "Kullanım Tercihleri"])


# ----------------------------------------------------------------------------
# 7.3 TAB1: KULLANICI BİLGİLERİ SEKMESİ
# ----------------------------------------------------------------------------
# Bu sekmede kullanıcının temel bilgileri alınır:
# - E-posta adresi (text_input)
# - Şifre (text_input, type="password" ile maskelenmiş)
# - Şifremi unuttum seçeneği (checkbox)
# - Kaydet butonu

with tab1:
    # E-posta girişi - dönen değer eposta değişkeninde saklanır
    eposta = st.text_input(label="E-Posta Adresinizi Giriniz:")
    
    # Şifre girişi - type="password" ile karakterler maskelenir
    sifre = st.text_input(label="Şifrenizi Giriniz", type="password")
    
    # Şifremi unuttum checkbox'ı
    st.checkbox(label="Şifremi Unuttum")
    
    # Görsel ayraç çizgisi
    st.divider()
    
    # Kaydet butonu - tıklandığında True döner, aksi halde False
    kaydet_btn = st.button(label="Kaydet")


# ----------------------------------------------------------------------------
# 7.4 TAB2: KULLANIM TERCİHLERİ SEKMESİ
# ----------------------------------------------------------------------------
# Bu sekmede kullanıcının tercih bilgileri alınır:
# - Hesap türü seçimi (radio button)
# - Zaman aşımı süresi ayarı (slider)
# - Özgeçmiş dosyası yükleme (file uploader)

with tab2:
    # Hesap türü seçimi - radio button
    # Seçilen değer hesap_turu değişkeninde saklanır
    hesap_turu = st.radio(label="Hesap Türü", options=["Öğrenci", "Mezun"])
    
    # Zaman aşımı süresi - slider ile değer seçimi
    # min_value: minimum değer, max_value: maksimum değer, value: başlangıç değeri
    st.slider(label="Zaman Aşımı Süresi (saniye)", min_value=3, max_value=30, value=5)
    
    # Dosya yükleme bileşeni
    st.file_uploader(label="Güncel Özgeçmişinizi Yükleyiniz")


# ----------------------------------------------------------------------------
# 7.5 VERİ KAYDETME İŞLEMİ
# ----------------------------------------------------------------------------
# Kaydet butonuna tıklandığında çalışan kod bloğu
# - Kullanıcı bilgileri JSON formatında dosyaya yazılır
# - Hesap türüne göre geçerlilik süresi belirlenir

if kaydet_btn:
    # Kullanıcı verilerini tutacak liste oluşturuluyor
    data = []
    
    # E-posta bilgisi listeye ekleniyor (dictionary olarak)
    data.append({"eposta": eposta})
    
    # Şifre bilgisi listeye ekleniyor
    data.append({"sifre": sifre})
    
    # Hesap türüne göre geçerlilik süresi belirleme
    # Öğrenciler için 1 yıl (365 gün), mezunlar için 1 ay (30 gün)
    if hesap_turu == "Öğrenci":
        gecerlilik_suresi = 365
    elif hesap_turu == "Mezun":
        gecerlilik_suresi = 30
    
    # Geçerlilik süresi listeye ekleniyor
    data.append({"geçerlilik süresi": gecerlilik_suresi})
    
    # JSON formatında dosyaya yazma işlemi
    # with bloğu: Dosya otomatik olarak kapanır (file handling best practice)
    # json.dumps(): Python listesini JSON string'ine dönüştürür
    with open("kullanici.txt", "w") as file:
        file.write(json.dumps(data))
    
    # Başarı animasyonu gösterme (balonlar)
    st.balloons()
    
    # Başarı mesajı gösterme (yeşil arka planlı bildirim)
    st.success("Dosyanız kaydedildi")
    
    # Belirlenen geçerlilik süresini kullanıcıya gösterme
    # f-string: Python 3.6+ ile gelen string formatlama yöntemi
    st.write(f"Belirlenen geçerlilik süresi: {gecerlilik_suresi}")


# ============================================================================
# 8. SESSION STATE MEKANİZMASI
# ============================================================================
# Session State, Streamlit'te kullanıcı oturumu boyunca veri saklamak için
# kullanılan bir mekanizmadır. Detaylı kullanım için 19.3.1.1_session.py
# dosyasına bakınız.
# 
# Temel Kavramlar:
# - st.session_state: Oturum boyunca kalıcı değişkenler saklar
# - Sayfa yenilense bile değerler korunur
# - Farklı bileşenler arasında veri paylaşımı sağlar
# ============================================================================