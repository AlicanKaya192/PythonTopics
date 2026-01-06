# =======================================================================================
# DOSYA: test.py
# AÇIKLAMA: Streamlit tabanlı basit kişilik testi uygulaması.
#           CrewAI ajanları tarafından üretilmiş bir örnek uygulama.
#
# KONU: OTONOM AJANLAR - CrewAI Çıktı Örneği
# 
# Bu dosya, crewai.py dosyasındaki çoklu ajan sistemi tarafından üretilmiş
# bir Python Streamlit uygulamasının örneğidir. Ajanlar şu adımları tamamladı:
# 1. Kişilik Testleri Uzmanı: Test içeriğini ve soruları hazırladı
# 2. Kişilik Testleri Danışmanı: İçeriği inceledi ve onayladı
# 3. Yazılım Mühendisi: Bu Streamlit uygulamasını kodladı
#
# KİŞİLİK TESTİ YAKLAŞIMI
# =======================
# Bu basit kişilik testi, bireyleri şu altı kategoride değerlendirir:
# - Dışa Dönük: Sosyal, enerjik, iletişime açık
# - İçe Dönük: Düşünceli, yalnızlığı seven, sakin
# - Pratik: Gerçekçi, sonuç odaklı, detaycı
# - Yenilikçi: Yaratıcı, değişime açık, vizyoner
# - Risk Alıcı: Maceraperest, cesur, girişken
# - Riskten Kaçınan: Temkinli, güvenlik odaklı, planlı
#
# STREAMLIT BİLEŞENLERİ
# =====================
# Bu uygulamada kullanılan Streamlit bileşenleri:
# - st.title(): Sayfa başlığı
# - st.radio(): Tekli seçim (radyo butonları)
# - st.button(): Tıklanabilir buton
# - st.subheader(): Alt başlık
# - st.write(): Metin çıktısı
#
# NOT: Bu basit bir örnektir. Gerçek kişilik testleri (Big Five, 16 Personalities)
# çok daha karmaşık algoritmalar ve daha fazla soru kullanır.
# =======================================================================================

import streamlit as st  # Streamlit web framework

# =======================================================================================
# SAYFA BAŞLIĞI
# =======================================================================================
# st.title(): Sayfanın ana başlığını oluşturur (H1 etiketine karşılık gelir)
# =======================================================================================

st.title('Kişilik Testi')

# =======================================================================================
# SORULAR VE YANITLAR
# =======================================================================================
# Kişilik testinin temel bileşenleri:
# 1. sorular: Kullanıcıya sorulacak kişilik değerlendirme soruları listesi
# 2. yanit_secenekleri: Likert ölçeği formatında yanıt seçenekleri
#
# Likert Ölçeği Nedir?
# --------------------
# Psikometrik testlerde yaygın kullanılan bir ölçekleme yöntemidir.
# Katılımcılardan bir ifadeye katılım derecelerini belirtmeleri istenir.
# Tipik 5'li ölçek: Kesinlikle Katılıyorum → Kesinlikle Katılmıyorum
# =======================================================================================

# Sorular ve yanıt seçenekleri
sorular = [
    "Yeni insanlarla tanışmayı sever misiniz?",  # Dışa dönüklük ölçer
    "Detaylara önem verir misiniz?",  # Pratiklik ölçer
    "Plan yapmadan seyahate çıkar mısınız?",  # Spontanlık/risk ölçer
    "Risk almayı sever misiniz?",  # Risk toleransı ölçer
    "Sanat eserlerinden etkilenir misiniz?",  # Açıklık ölçer
    "Bir grup içinde liderlik yapmayı sever misiniz?",  # Dışa dönüklük ölçer
    "Bilinmeyene karşı meraklı mısınız?",  # Yenilikçilik ölçer
    "Kuralları sorgular mısınız?",  # Yenilikçilik ölçer
    "Yalnız zaman geçirmekten hoşlanır mısınız?",  # İçe dönüklük ölçer
    "Düzenli bir yaşam tarzını tercih eder misiniz?"  # Pratiklik ölçer
]

# Likert ölçeği yanıt seçenekleri (5'li)
yanit_secenekleri = [
    'Kesinlikle katılıyorum',  # En güçlü olumlu
    'Katılıyorum',  # Olumlu
    'Kararsızım',  # Nötr
    'Katılmıyorum',  # Olumsuz
    'Kesinlikle katılmıyorum'  # En güçlü olumsuz
]

# =======================================================================================
# KULLANICI YANITLARINI TOPLAMA
# =======================================================================================
# Her soru için bir st.radio() widget'ı oluşturulur.
# Kullanıcının yanıtları bir listede toplanır.
#
# st.radio() Parametreleri:
# - Birinci parametre: Soru metni (widget başlığı)
# - İkinci parametre: Seçenekler listesi
# - key: Widget'ın benzersiz tanımlayıcısı (her widget için farklı olmalı)
#
# NOT: key parametresi olmazsa, aynı seçeneklere sahip radio butonları
# birbirine karışabilir. Her soru kendisi key olarak kullanılıyor.
# =======================================================================================

# Kullanıcı yanıtlarını toplama
yanitlar = []  # Tüm yanıtları saklamak için boş liste

for soru in sorular:
    # Her soru için radio buton oluştur
    # key=soru parametresi, her radio button'ın benzersiz olmasını sağlar
    yanit = st.radio(soru, yanit_secenekleri, key=soru)
    # Seçilen yanıtı listeye ekle
    yanitlar.append(yanit)

# =======================================================================================
# KİŞİLİK TİPİ HESAPLAMA ALGORİTMASI
# =======================================================================================
# Bu basit algoritma, yanıtlara göre puan hesaplar ve en yüksek puanlı
# kişilik tiplerini döndürür.
#
# Puanlama Mantığı:
# - Olumlu yanıtlar (Kesinlikle katılıyorum, Katılıyorum):
#   → Dışa Dönük, Yenilikçi, Risk Alıcı puanları artar
# - Kararsız yanıtlar:
#   → Pratik, İçe Dönük puanları artar
# - Olumsuz yanıtlar (Katılmıyorum, Kesinlikle katılmıyorum):
#   → İçe Dönük, Pratik, Riskten Kaçınan puanları artar
#
# NOT: Bu basitleştirilmiş bir algoritmadır. Gerçek kişilik testleri,
# her soru için farklı ağırlıklar ve faktör analizi kullanır.
# =======================================================================================

def kisilik_tipi_hesapla(yanitlar):
    """
    Kullanıcı yanıtlarına göre kişilik tipini hesaplar.
    
    Bu fonksiyon, basit bir puanlama algoritması kullanır:
    - Olumlu yanıtlar → Dışa dönük, yenilikçi, risk alıcı özellikleri güçlendirir
    - Kararsız yanıtlar → Pratik ve içe dönük özellikleri güçlendirir
    - Olumsuz yanıtlar → İçe dönük, pratik ve riskten kaçınan özellikleri güçlendirir
    
    Parametreler:
    -------------
    yanitlar (list): Kullanıcının tüm sorulara verdiği yanıtların listesi
    
    Returns:
        str: Belirlenmiş kişilik tipleri (virgülle ayrılmış string)
    """
    # Kişilik tipi puanları için sözlük
    # Her kişilik tipi 0 puanla başlar
    puanlar = {
        'Dışa Dönük': 0,  # Sosyal, enerjik
        'İçe Dönük': 0,  # Düşünceli, sakin
        'Pratik': 0,  # Gerçekçi, detaycı
        'Yenilikçi': 0,  # Yaratıcı, açık fikirli
        'Riskten Kaçınan': 0,  # Temkinli, güvenlik odaklı
        'Risk Alıcı': 0  # Cesur, maceraperest
    }

    # Her yanıtı değerlendir ve puanları güncelle
    for yanit in yanitlar:
        if yanit == 'Kesinlikle katılıyorum' or yanit == 'Katılıyorum':
            # Olumlu yanıtlar: Dışa dönük, yenilikçi ve risk alıcı özellikler
            puanlar['Dışa Dönük'] += 1
            puanlar['Yenilikçi'] += 1
            puanlar['Risk Alıcı'] += 1
        elif yanit == 'Kararsızım':
            # Nötr yanıtlar: Pratik ve içe dönük özellikler
            puanlar['Pratik'] += 1
            puanlar['İçe Dönük'] += 1
        elif yanit == 'Katılmıyorum' or yanit == 'Kesinlikle katılmıyorum':
            # Olumsuz yanıtlar: İçe dönük, pratik ve riskten kaçınan özellikler
            puanlar['İçe Dönük'] += 1
            puanlar['Pratik'] += 1
            puanlar['Riskten Kaçınan'] += 1

    # En yüksek puanı bul
    # max(puanlar.values()): Puanlar sözlüğündeki en yüksek değer
    max_puan = max(puanlar.values())
    
    # En yüksek puana sahip tüm kişilik tiplerini bul
    # (Birden fazla tip aynı puana sahip olabilir)
    # list comprehension: Her key-value çifti için, value max_puan'a eşitse key'i al
    kisilik_tipleri = [k for k, v in puanlar.items() if v == max_puan]

    # Kişilik tiplerini virgülle ayrılmış string olarak döndür
    # ['Dışa Dönük', 'Yenilikçi'] → 'Dışa Dönük, Yenilikçi'
    return ', '.join(kisilik_tipleri)

# =======================================================================================
# SONUÇLARI GÖRÜNTÜLEME
# =======================================================================================
# Kullanıcı "Kişilik Tipimi Belirle" butonuna tıkladığında:
# 1. Hesaplama fonksiyonu çağrılır
# 2. Sonuç alt başlık olarak gösterilir
# 3. Açıklayıcı not eklenir
#
# st.button(): Tıklandığında True dönen buton
# st.subheader(): Alt başlık (H2'ye karşılık)
# st.write(): Genel amaçlı metin çıktısı
# =======================================================================================

# Sonuçları gösterme
if st.button('Kişilik Tipimi Belirle'):
    # Kişilik tipini hesapla
    sonuc = kisilik_tipi_hesapla(yanitlar)
    
    # Sonuçları göster
    st.subheader('Kişilik Tipiniz:')
    st.write(sonuc)
    
    # Açıklayıcı not
    # Bu not, testin sınırlamalarını belirtir
    st.write('Not: Bu test, genel bir rehber olarak kullanılmalıdır. Kişilik, zaman içinde ve farklı durumlar altında değişebilir.')