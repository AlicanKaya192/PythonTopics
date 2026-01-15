# ===================================================================================
# 19.9 - UYGULAMA PROJESİ: DATA EXPLORER
# ===================================================================================
# Bu dosya, Data Explorer uygulamasının ana Streamlit arayüzünü içerir.
# 
# PROJE AMACI:
# ------------
# Bu proje, kullanıcıların CSV dosyalarını yükleyerek doğal dilde (Türkçe) 
# sorular sorabilmelerini ve AI destekli veri analizi yapabilmelerini sağlar.
# LangChain ve GPT/Claude modelleri kullanılarak verilerle "konuşma" deneyimi sunar.
#
# NEDEN BU PROJEYİ YAPTIK?
# ------------------------
# - Veri analizi genellikle teknik bilgi gerektirir (SQL, Python, Pandas vb.)
# - Bu proje sayesinde teknik bilgisi olmayan kullanıcılar da veriyle etkileşime geçebilir
# - Doğal dil ile veri keşfi, veri demokratizasyonunun önemli bir adımıdır
# - LangChain'in Pandas agent özelliğini pratik bir senaryoda kullanmayı öğreniyoruz
#
# KULLANILAN TEKNOLOJİLER:
# ------------------------
# - Streamlit: Hızlı ve kolay web arayüzü oluşturma
# - LangChain: LLM'lerle yapılandırılmış etkileşim
# - OpenAI GPT / Anthropic Claude: Doğal dil işleme ve analiz
# - Pandas: Veri manipülasyonu ve analizi
# ===================================================================================

import streamlit as st  # Web arayüzü oluşturmak için Streamlit kütüphanesi
import datahelper       # Veri işleme ve AI etkileşimi için yardımcı modülümüz

# ===================================================================================
# SESSION STATE YÖNETİMİ
# ===================================================================================
# Streamlit'te session_state, uygulama oturumu boyunca verileri korumak için kullanılır.
# 
# NEDEN SESSION STATE KULLANIYORUZ?
# ---------------------------------
# - Streamlit, her kullanıcı etkileşiminde sayfayı yeniden çalıştırır
# - Session state olmadan, yüklenen veriler ve durumlar kaybolur
# - "dataload" değişkeni, veri yüklenip yüklenmediğini takip eder
# - Bu sayede kullanıcı deneyimi kesintisiz devam eder

if "dataload" not in st.session_state:
    # İlk açılışta dataload False olarak ayarlanır
    # Bu, veri henüz yüklenmedi anlamına gelir
    st.session_state.dataload = False


def activate_dataload():
    """
    Veri yükleme durumunu aktif hale getirir.
    
    NEDEN BU FONKSİYON VAR?
    -----------------------
    - Streamlit button'ları on_click callback fonksiyonu alabilir
    - Bu fonksiyon, "Yükle" butonuna tıklandığında çağrılır
    - Session state'i güncelleyerek uygulamanın veri moduna geçmesini sağlar
    
    BU BİZE NE SAĞLAR?
    ------------------
    - Kullanıcı butona tıkladığında anında durum değişikliği
    - Sayfa yenilense bile veri yüklendi bilgisi korunur
    """
    st.session_state.dataload = True


# ===================================================================================
# SAYFA YAPILANDIRMASI
# ===================================================================================
# Streamlit sayfa ayarlarını en başta yapmak önemlidir.
# 
# NEDEN BU AYARLARI YAPIYORUZ?
# ----------------------------
# - page_title: Tarayıcı sekmesinde görünen başlık
# - layout="wide": Sayfa genişliğini kullanarak daha fazla alan sağlar
# - Bu, özellikle veri tabloları ve grafikler için önemlidir

st.set_page_config(page_title="Data Explorer 🤖", layout="wide")

# ===================================================================================
# GÖRSEL BANNER VE BAŞLIK
# ===================================================================================
# Uygulamanın görsel kimliğini oluşturan banner görseli ve başlık.
# 
# NEDEN BANNER KULLANIYORUZ?
# --------------------------
# - Profesyonel ve çekici bir görünüm sağlar
# - Kullanıcıya uygulamanın amacını hemen anlatır
# - Marka kimliği oluşturur
#
# NOT: Görsel dosyası assets klasöründen alınmaktadır.

st.image(image="../assets/19.9-Materyaller/img/app_banner.jpg", use_column_width=True)
st.title("Data Explorer: Doğal Dilde Veri Keşfi 🤖")
st.divider()  # Görsel ayırıcı çizgi, bölümleri ayırt etmeyi kolaylaştırır

# ===================================================================================
# SIDEBAR - VERİ YÜKLEME ALANI
# ===================================================================================
# Sidebar, ana içerikten bağımsız bir kontrol paneli sağlar.
# 
# NEDEN SIDEBAR KULLANIYORUZ?
# ---------------------------
# - Ana içerik alanını temiz tutar
# - Kontroller her zaman erişilebilir durumda kalır
# - Kullanıcı deneyimini iyileştirir

st.sidebar.subheader("Veriye Dosyanızı Yükleyin")
st.sidebar.divider()

# ===================================================================================
# DOSYA YÜKLEME KOMPONENTİ
# ===================================================================================
# CSV dosyası yükleme alanı.
# 
# NEDEN SADECE CSV?
# -----------------
# - CSV, en yaygın veri formatlarından biridir
# - Pandas ile kolay işlenebilir
# - Çoğu veri kaynağından CSV export alınabilir
# - type="csv" ile sadece CSV dosyalarının yüklenmesine izin veriyoruz

loaded_file = st.sidebar.file_uploader(
    "Yüklemek istediğiniz CSV dosyasını seçiniz", 
    type="csv"
)

# Yükleme butonu - on_click ile activate_dataload fonksiyonunu tetikler
load_data_btn = st.sidebar.button(
    label="Yükle", 
    on_click=activate_dataload, 
    use_container_width=True  # Buton sidebar genişliğini kaplar
)

# ===================================================================================
# ANA SAYFA DÜZENI - KOLONLAR
# ===================================================================================
# Sayfayı üç kolona bölerek düzenli bir görünüm oluşturuyoruz.
# 
# KOLON ORANLARI [4, 1, 7]:
# -------------------------
# - col_prework (4): Veri özeti bölümü - orta genişlikte
# - col_dummy (1): Boş alan - kolonlar arasında görsel ayırıcı
# - col_interaction (7): Etkileşim bölümü - en geniş alan
# 
# NEDEN BU DÜZEN?
# ---------------
# - Kullanıcı hem veri özetini hem de etkileşim alanını aynı anda görebilir
# - Profesyonel dashboard görünümü sağlar
# - Responsive tasarım için Streamlit kolonları idealdir

col_prework, col_dummy, col_interaction = st.columns([4, 1, 7])


# ===================================================================================
# VERİ YÜKLEME SONRASI İŞLEMLER
# ===================================================================================
# Veri yüklendiğinde (dataload=True) aşağıdaki bölümler aktif olur.

if st.session_state.dataload:
    
    # ===============================================================================
    # VERİ ÖZETİ OLUŞTURMA FONKSİYONU
    # ===============================================================================
    # @st.cache_data dekoratörü çok önemli bir performans optimizasyonudur.
    # 
    # NEDEN CACHE KULLANIYORUZ?
    # -------------------------
    # - AI API çağrıları maliyetli ve zaman alıcıdır
    # - Aynı veri için tekrar tekrar özet çıkarmak gereksizdir
    # - Cache, sonuçları bellekte saklar ve tekrar kullanır
    # - Bu sayede hem maliyet hem de zaman tasarrufu sağlanır
    # 
    # BU BİZE NE SAĞLAR?
    # ------------------
    # - Hızlı sayfa yenileme
    # - Düşük API maliyeti
    # - Daha iyi kullanıcı deneyimi
    
    @st.cache_data
    def summarize():
        """
        Yüklenen CSV dosyasını özetler.
        
        NEDEN seek(0)?
        --------------
        - Dosya daha önce okunduysa, okuma imleci dosyanın sonundadır
        - seek(0) imleci başa döndürür
        - Bu olmadan dosya tekrar okunamaz
        
        Returns:
            dict: Veri özeti içeren sözlük (örnek veri, sütun açıklamaları, 
                  eksik değerler, mükerrer değerler, temel metrikler)
        """
        loaded_file.seek(0)  # Dosya imlecini başa al
        data_summary = datahelper.summarize_csv(data_file=loaded_file)
        return data_summary
    
    # Özeti bir kere hesapla ve sonucu sakla
    data_summary = summarize()

    # ===============================================================================
    # SOL KOLON - VERİ ÖZETİ BÖLÜMÜ
    # ===============================================================================
    # Verinin genel görünümünü ve temel istatistiklerini gösterir.
    
    with col_prework:
        st.info("VERİ ÖZETİ")  # Bilgi kutusu - mavi arka plan
        
        # ---------------------------------------------------------------------------
        # ÖRNEK VERİ KESİTİ
        # ---------------------------------------------------------------------------
        # İlk 5 satırı göstererek kullanıcının veriyi anlamasını sağlıyoruz.
        # NEDEN ÖNEMLİ: Kullanıcı verinin yapısını hemen görebilir
        st.subheader("Verinizden Örnek Bir Kesit:")
        st.write(data_summary["initial_data_sample"])
        st.divider()
        
        # ---------------------------------------------------------------------------
        # SÜTUN AÇIKLAMALARI
        # ---------------------------------------------------------------------------
        # AI tarafından oluşturulan sütun açıklamaları
        # NEDEN ÖNEMLİ: Her sütunun ne içerdiği Türkçe olarak açıklanır
        st.subheader("Veri Kümesinde Yer Alan Değişkenler:")
        st.write(data_summary["column_descriptions"])
        st.divider()
        
        # ---------------------------------------------------------------------------
        # EKSİK VERİ DURUMU
        # ---------------------------------------------------------------------------
        # Veri kalitesi için kritik bilgi
        # NEDEN ÖNEMLİ: Eksik veriler analiz sonuçlarını etkileyebilir
        st.subheader("Eksik/Kayıp Veri Durumu:")
        st.write(data_summary["missing_values"])
        st.divider()
        
        # ---------------------------------------------------------------------------
        # MÜKERRER VERİ DURUMU
        # ---------------------------------------------------------------------------
        # Tekrarlanan kayıtların tespiti
        # NEDEN ÖNEMLİ: Mükerrer veriler istatistikleri çarpıtabilir
        st.subheader("Mükerrer Veri Durumu:")
        st.write(data_summary["duplicate_values"])
        st.divider()
        
        # ---------------------------------------------------------------------------
        # TEMEL METRİKLER
        # ---------------------------------------------------------------------------
        # Pandas describe() ile temel istatistikler
        # NEDEN ÖNEMLİ: Ortalama, standart sapma, min, max gibi değerler
        st.subheader("Temel Metrikler")
        st.write(data_summary["essential_metrics"])
    
    # ===============================================================================
    # ORTA KOLON - BOŞ ALAN
    # ===============================================================================
    # Görsel ayırıcı olarak kullanılır
    
    with col_dummy:
        st.empty()  # Boş bir Streamlit elementi
    
    # ===============================================================================
    # SAĞ KOLON - VERİYLE ETKİLEŞİM BÖLÜMÜ
    # ===============================================================================
    # Kullanıcının veriyle AI destekli etkileşime geçtiği alan
    
    with col_interaction:

        st.info("VERİYLE ETKİLEŞİM")
        
        # ---------------------------------------------------------------------------
        # DEĞİŞKEN İNCELEME ALANI
        # ---------------------------------------------------------------------------
        # Kullanıcı belirli bir sütunu (değişkeni) inceleyebilir
        # NEDEN ÖNEMLİ: Spesifik bir değişkenin trend analizi yapılabilir
        
        variable_of_interest = st.text_input(
            label="İncelemek İstediğiniz Değişken Hangisi?"
        )
        examine_btn = st.button(label="İncele")
        st.divider()

        @st.cache_data
        def explore_variable(data_file, variable_of_interest):
            """
            Belirtilen değişkeni görselleştirir ve trend analizi yapar.
            
            NEDEN BU FONKSİYON ÖNEMLİ?
            --------------------------
            - Kullanıcı herhangi bir sütunu seçip görselleştirebilir
            - AI, trendle ilgili yorum yapar
            - Teknik bilgi gerektirmeden veri analizi mümkün olur
            
            NEDEN seek(0)?
            --------------
            - Dosya birden fazla kez okunuyor
            - Her okuma öncesi imleç sıfırlanmalı
            
            Args:
                data_file: Yüklenen CSV dosyası
                variable_of_interest: İncelenecek sütun adı
            """
            data_file.seek(0)
            dataframe = datahelper.get_dataframe(data_file=data_file)
            
            # Bar chart görselleştirme
            # NEDEN BAR CHART: Zaman serisi verileri için uygun
            st.bar_chart(data=dataframe, y=[variable_of_interest])
            st.divider()
            
            data_file.seek(0)
            # AI destekli trend analizi
            trend_response = datahelper.analyze_trend(
                data_file=loaded_file, 
                variable_of_interest=variable_of_interest
            )
            st.success(trend_response)  # Yeşil başarı kutusu içinde göster
            return
        
        # Değişken adı girilmişse veya İncele butonuna tıklanmışsa
        if variable_of_interest or examine_btn:
            explore_variable(data_file=loaded_file, variable_of_interest=variable_of_interest)
        
        # ---------------------------------------------------------------------------
        # SERBEST SORU SORMA ALANI
        # ---------------------------------------------------------------------------
        # Kullanıcı veriyle ilgili herhangi bir soru sorabilir
        # Bu, projenin en güçlü özelliğidir!
        # 
        # NEDEN ÖNEMLİ?
        # -------------
        # - Doğal dilde soru sorma imkanı
        # - SQL veya Python bilmeye gerek yok
        # - AI, soruyu anlayıp veri üzerinde analiz yapar
        # - Türkçe soru sorulabilir ve Türkçe cevap alınır

        free_question = st.text_input(
            label="Veri Kümesiyle İlgili Ne Bilmek İstersiniz?"
        )
        ask_btn = st.button(label="Sor")
        st.divider()

        @st.cache_data
        def answer_question(data_file, question):
            """
            Kullanıcının serbest sorusunu AI ile yanıtlar.
            
            NEDEN BU FONKSİYON ÖNEMLİ?
            --------------------------
            - LangChain Pandas Agent kullanarak veri üzerinde sorgu çalıştırır
            - Kullanıcı "En yüksek satış hangi günde?" gibi sorular sorabilir
            - AI, gereken Python/Pandas kodunu otomatik üretir ve çalıştırır
            
            Args:
                data_file: Yüklenen CSV dosyası
                question: Kullanıcının sorduğu soru
            """
            data_file.seek(0)
            AI_Response = datahelper.ask_question(
                data_file=loaded_file, 
                question=free_question
            )
            st.success(AI_Response)
            return
        
        # Soru girilmişse veya Sor butonuna tıklanmışsa
        if free_question or ask_btn:
            answer_question(data_file=loaded_file, question=free_question)


# ===================================================================================
# UYGULAMA SONU
# ===================================================================================
# Bu uygulama, LangChain ve Streamlit'in gücünü birleştirerek
# herkesin veri analizi yapabilmesini sağlayan bir araç sunar.
# 
# GELİŞTİRME ÖNERİLERİ:
# ---------------------
# 1. Farklı dosya formatları desteği (Excel, JSON)
# 2. Grafik türü seçimi (line, bar, pie)
# 3. Veri dışa aktarma özelliği
# 4. Çoklu dosya karşılaştırma
# 5. Otomatik rapor oluşturma
# ===================================================================================
