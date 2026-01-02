# ============================================================================
# Üretken Yapay Zeka ile Uygulama Geliştirme Eğitimi
# Modül 1: Streamlit ile Hızlı Prototipleme
# Streamlit Session State Mekanizması - Pratik Kullanım
# ============================================================================
# Bu dosya, Streamlit'in en önemli kavramlarından biri olan Session State
# mekanizmasının pratik kullanımını göstermektedir.
#
# SESSION STATE NEDİR?
# ---------------------
# Streamlit, varsayılan olarak her kullanıcı etkileşiminde (buton tıklaması,
# input değişikliği vb.) tüm scripti baştan çalıştırır. Bu durum, değişkenlerin
# her seferinde sıfırlanmasına neden olur.
#
# Session State, bu sorunu çözmek için tasarlanmıştır:
# - Kullanıcı oturumu boyunca değişkenleri bellekte tutar
# - Sayfa yenilendiğinde veya widget etkileşiminde değerler korunur
# - Farklı bileşenler arasında veri paylaşımını mümkün kılar
# ============================================================================

# ============================================================================
# 1. KÜTÜPHANE İMPORTLARI
# ============================================================================
# streamlit: Web uygulaması framework'ü
# pandas: Veri analizi ve işleme kütüphanesi (CSV okuma için)

import streamlit as st
import pandas as pd


# ============================================================================
# 2. SAYFA BAŞLIĞI
# ============================================================================
# st.header(): Sayfaya büyük bir başlık ekler
# Bu, kullanıcıya uygulamanın amacını açıkça gösterir

st.header("Session State Mekanizması: Pratik Kullanım")


# ============================================================================
# 3. SESSION STATE DEĞİŞKENİ BAŞLATMA
# ============================================================================
# Session State kullanımının ÖNEMLİ KURALI:
# Değişkeni kullanmadan önce, var olup olmadığını kontrol etmeliyiz!
#
# Neden? Streamlit her etkileşimde scripti yeniden çalıştırır:
# - İlk çalıştırmada değişken henüz oluşturulmamıştır
# - Sonraki çalıştırmalarda değişken zaten vardır ve değeri korunmuştur
#
# "not in" kontrolü:
# - Değişken yoksa: Başlangıç değeri atanır (bu örnekte 10)
# - Değişken varsa: Mevcut değer korunur, bu blok atlanır

if "satir_sayisi" not in st.session_state:
    st.session_state.satir_sayisi = 10


# ============================================================================
# 4. VERİ OKUMA İŞLEMİ
# ============================================================================
# pandas.read_csv(): CSV dosyasını DataFrame olarak okur
# - Dosya yolu: ../datasets/data.csv (datasets klasöründen)
# - sep=",": Sütun ayırıcı olarak virgül kullanılır (varsayılan değer)
#
# Not: Dataset dosyası 19-Generative klasörünün altındaki datasets
# klasöründe bulunmaktadır.

dataframe = pd.read_csv("../datasets_19/data.csv", sep=",")


# ============================================================================
# 5. VERİ TABLOSU GÖSTERME
# ============================================================================
# st.table(): DataFrame'i statik tablo olarak gösterir
# - Kaydırma veya sıralama özellikleri yoktur
# - Küçük veri setleri için idealdir
#
# dataframe.head(n): DataFrame'in ilk n satırını döndürür
# - n değeri session_state'ten alınır
# - Bu sayede satır sayısı dinamik olarak değiştirilebilir
#
# Alternatif: st.dataframe() - Etkileşimli tablo (sıralama, filtreleme)

st.table(dataframe.head(st.session_state.satir_sayisi))


# ============================================================================
# 6. CALLBACK FONKSİYONLARI
# ============================================================================
# Callback fonksiyonları, widget etkileşimlerinde çağrılan fonksiyonlardır.
# Bu örnekte, butonlara tıklandığında satır sayısını artıran/azaltan
# fonksiyonlar tanımlanmıştır.
#
# ÖNEMLİ: Callback fonksiyonları, session_state değişkenlerini doğrudan
# değiştirebilir. Bu değişiklikler, sayfa yeniden render edildiğinde
# hemen yansıtılır.

def artir():
    """
    Satır sayısını 1 artırır.
    Session State'teki 'satir_sayisi' değişkenine doğrudan erişir ve günceller.
    """
    st.session_state.satir_sayisi += 1

def dusur():
    """
    Satır sayısını 1 azaltır.
    Session State'teki 'satir_sayisi' değişkenine doğrudan erişir ve günceller.
    Dikkat: Negatif değerlere düşmemesi için kontrol eklenebilir.
    """
    st.session_state.satir_sayisi -= 1


# ============================================================================
# 7. KONTROL BUTONLARI
# ============================================================================
# st.button(): Tıklanabilir buton oluşturur
# - label: Buton üzerinde görünecek metin
# - on_click: Butona tıklandığında çağrılacak fonksiyon (callback)
#
# on_click parametresi sayesinde:
# - Buton tıklandığında otomatik olarak ilgili fonksiyon çağrılır
# - Fonksiyon, session_state'i güncelledikten sonra sayfa yeniden render edilir
# - Güncel değerler hemen ekranda görünür

artir_btn = st.button(label="Artır 👆", on_click=artir)
dusur_btn = st.button(label="Düşür 👇", on_click=dusur)


# ============================================================================
# 8. MEVCUT DEĞER GÖSTERME
# ============================================================================
# st.divider(): Görsel ayraç çizgisi ekler (içerik bölümlendirmesi için)
# st.header(): Mevcut satır sayısını büyük fontla gösterir
#
# Bu bölüm, session_state mekanizmasının çalıştığını doğrulamak için
# kullanılır. Artır/Düşür butonlarına tıklandığında değerin değiştiğini
# gözlemleyebilirsiniz.

st.divider()
st.header(st.session_state.satir_sayisi)


# ============================================================================
# ÖZET: SESSION STATE KULLANIM ADIMLARI
# ============================================================================
# 1. Değişkeni kontrol et: if "degisken_adi" not in st.session_state
# 2. Yoksa başlangıç değeri ata: st.session_state.degisken_adi = deger
# 3. Değişkeni kullan: st.session_state.degisken_adi
# 4. Callback ile güncelle: on_click parametresi ile fonksiyon bağla
#
# BU YAPININ AVANTAJLARI:
# - Kullanıcı etkileşimleri arasında veri korunur
# - Sayfa yenilenmelerinde değerler kaybolmaz
# - Karmaşık uygulama durumları yönetilebilir
# - Birden fazla bileşen arasında veri paylaşımı mümkün olur
# ============================================================================