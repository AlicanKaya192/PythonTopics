# ===================================================================================
# 19.9 - UYGULAMA PROJESİ: DATA EXPLORER - VERİ YARDIMCI MODÜLÜ
# ===================================================================================
# Bu dosya, Data Explorer uygulamasının veri işleme ve AI etkileşim fonksiyonlarını içerir.
# 
# MODÜL AMACI:
# ------------
# Ana uygulama (app.py) ile AI modelleri arasında köprü görevi görür.
# LangChain Pandas Agent kullanarak veri üzerinde doğal dil sorguları çalıştırır.
#
# NEDEN AYRI BİR MODÜL?
# ---------------------
# - Separation of Concerns (Endişelerin Ayrılması) prensibi
# - UI kodu (app.py) ile iş mantığı (datahelper.py) ayrı tutulur
# - Kod tekrarı önlenir, bakım kolaylaşır
# - Test edilebilirlik artar
# - Farklı UI'lar aynı helper fonksiyonları kullanabilir
#
# KULLANILAN TEKNOLOJİLER:
# ------------------------
# - Pandas: Veri manipülasyonu için Python'ın güçlü kütüphanesi
# - LangChain: LLM'lerle yapılandırılmış etkileşim framework'ü
# - LangChain Experimental: Pandas DataFrame Agent içerir
# - OpenAI GPT & Anthropic Claude: Büyük dil modelleri
# - python-dotenv: Çevresel değişkenleri .env dosyasından okuma
# ===================================================================================

import pandas as pd  # Veri işleme ve analiz için temel kütüphane

# ===================================================================================
# LANGCHAIN PANDAS AGENT İMPORTU
# ===================================================================================
# LangChain'in deneysel modülünden Pandas DataFrame Agent'ı import ediyoruz.
# 
# NEDEN "EXPERIMENTAL" MODÜLÜNDE?
# -------------------------------
# - Bu özellik henüz tam olarak stabil değil
# - API değişikliklere açık olabilir
# - Ancak işlevselliği çok güçlü ve kullanışlı
# 
# BU AGENT NE YAPAR?
# ------------------
# - LLM'e bir Pandas DataFrame verir
# - LLM, doğal dildeki soruyu anlar
# - Gerekli Python/Pandas kodunu otomatik üretir
# - Kodu çalıştırır ve sonucu döndürür

from langchain_experimental.agents.agent_toolkits.pandas.base import (
    create_pandas_dataframe_agent,
)

# ===================================================================================
# LLM MODEL İMPORTLARI
# ===================================================================================
# Farklı AI sağlayıcılarından model sınıflarını import ediyoruz.
# 
# NEDEN BİRDEN FAZLA MODEL?
# -------------------------
# - Farklı modellerin farklı güçlü yönleri var
# - GPT-4: Genel amaçlı, çok yönlü
# - Claude: Uzun metinlerde başarılı, güvenlik odaklı
# - Maliyet ve performans dengeleme imkanı

from langchain_openai import ChatOpenAI      # OpenAI GPT modelleri için
from langchain_anthropic import ChatAnthropic  # Anthropic Claude modelleri için

import os  # Çevresel değişkenlere erişim için
from dotenv import load_dotenv  # .env dosyasını okumak için

# ===================================================================================
# ÇEVRESEL DEĞİŞKENLERİ YÜKLEME
# ===================================================================================
# API anahtarları gibi hassas bilgileri .env dosyasından okuyoruz.
# 
# NEDEN .ENV DOSYASI KULLANIYORUZ?
# --------------------------------
# - Güvenlik: API anahtarları kod içinde yazılmaz
# - Esneklik: Farklı ortamlarda farklı anahtarlar kullanılabilir
# - Git güvenliği: .env dosyası .gitignore'a eklenerek versiyon kontrolüne dahil edilmez
# - Best Practice: Endüstri standardı bir yaklaşımdır
# 
# BU BİZE NE SAĞLAR?
# ------------------
# - Kod paylaşırken API anahtarları sızma riski yok
# - Geliştirme ve prodüksiyon ortamları kolayca ayrılır
# - Takım çalışmasında herkes kendi anahtarını kullanabilir

load_dotenv()  # .env dosyasını oku ve çevresel değişkenlere yükle

# API anahtarlarını çevresel değişkenlerden al
my_key_openai = os.getenv("openai_apikey")      # OpenAI API anahtarı
my_key_anthropic = os.getenv("anthropic_apikey")  # Anthropic API anahtarı

# ===================================================================================
# LLM MODEL YAPILANDIRMASI
# ===================================================================================
# Kullanılacak AI modellerini yapılandırıyoruz.
# 
# PARAMETRE AÇIKLAMALARI:
# -----------------------
# - api_key: Kimlik doğrulama için API anahtarı
# - model: Kullanılacak model versiyonu
# - temperature: Yaratıcılık seviyesi (0 = deterministik, 1 = yaratıcı)
# 
# NEDEN TEMPERATURE=0?
# --------------------
# - Veri analizi determinizm gerektirir
# - Aynı soru aynı cevabı vermelidir
# - Yaratıcılık değil, doğruluk önceliklidir
# - Finansal/istatistiksel sorularda tutarlılık kritik

# OpenAI GPT-4 Turbo modeli - En güncel ve güçlü GPT modeli
llm_gpt = ChatOpenAI(
    api_key=my_key_openai, 
    model="gpt-4-turbo-preview",  # GPT-4 Turbo: Hızlı ve maliyet-etkin
    temperature=0  # Deterministik çıktı için
)

# Anthropic Claude 3 Opus - En güçlü Claude modeli
# Karmaşık akıl yürütme ve uzun bağlam için ideal
llm_claude_opus = ChatAnthropic(
    anthropic_api_key=my_key_anthropic, 
    model_name="claude-3-opus-20240229", 
    temperature=0
)

# Anthropic Claude 3 Haiku - Hızlı ve ekonomik Claude modeli
# Basit sorular için maliyet-etkin seçenek
llm_claude_haiku = ChatAnthropic(
    anthropic_api_key=my_key_anthropic, 
    model_name="claude-3-haiku-20240307", 
    temperature=0
)

# ===================================================================================
# AKTİF MODEL SEÇİMİ
# ===================================================================================
# Uygulamada kullanılacak modeli seçiyoruz.
# 
# NEDEN GPT SEÇİLDİ?
# ------------------
# - GPT-4's Pandas kod üretiminde çok başarılı
# - Türkçe dil desteği iyi
# - API güvenilirliği yüksek
# 
# NOT: İhtiyaca göre diğer modellere geçiş yapılabilir

selected_llm = llm_gpt  # Varsayılan olarak GPT-4 kullanıyoruz


# ===================================================================================
# VERİ ÖZETİ OLUŞTURMA FONKSİYONU
# ===================================================================================

def summarize_csv(data_file):
    """
    Yüklenen CSV dosyasının kapsamlı bir özetini oluşturur.
    
    NEDEN BU FONKSİYON ÖNEMLİ?
    --------------------------
    - Kullanıcıya verinin genel görünümünü sunar
    - Veri kalitesi hakkında bilgi verir (eksik/mükerrer değerler)
    - AI destekli sütun açıklamaları sağlar
    - Teknik olmayan kullanıcıların veriyi anlamasını kolaylaştırır
    
    BU BİZE NE SAĞLAR?
    ------------------
    - Hızlı veri keşfi
    - Veri kalitesi değerlendirmesi
    - Anlaşılır sütun açıklamaları
    - İstatistiksel özet
    
    Args:
        data_file: Streamlit tarafından yüklenen CSV dosya objesi
        
    Returns:
        dict: Aşağıdaki anahtarları içeren sözlük:
            - initial_data_sample: İlk 5 satır (df.head())
            - column_descriptions: AI tarafından üretilen sütun açıklamaları
            - missing_values: Eksik veri bilgisi
            - duplicate_values: Mükerrer veri bilgisi
            - essential_metrics: Temel istatistikler (df.describe())
    """
    
    # CSV dosyasını Pandas DataFrame'e dönüştür
    # low_memory=False: Büyük dosyalarda tip çıkarımını iyileştirir
    # NEDEN LOW_MEMORY=FALSE?
    # - Pandas varsayılan olarak bellek tasarrufu için chunk'lar halinde okur
    # - Bu, sütun tiplerinin tutarsız çıkarılmasına neden olabilir
    # - False ayarı, tüm veriyi okuyarak doğru tip çıkarımı sağlar
    df = pd.read_csv(data_file, low_memory=False)

    # ===================================================================================
    # PANDAS DATAFRAME AGENT OLUŞTURMA
    # ===================================================================================
    # LangChain'in Pandas Agent'ını oluşturuyoruz.
    # 
    # NEDEN BU AGENT?
    # ---------------
    # - DataFrame üzerinde doğal dilde sorgular çalıştırabilir
    # - Python/Pandas kodu otomatik üretir
    # - Sonuçları anlaşılır formatta döndürür
    # 
    # PARAMETRE AÇIKLAMALARI:
    # -----------------------
    # - selected_llm: Kullanılacak AI modeli
    # - df: Analiz edilecek DataFrame
    # - verbose=True: İşlem adımlarını konsola yazdırır (debug için)
    # - handle_parsing_errors: Hatalı LLM çıktılarını yönetir
    
    pandas_agent = create_pandas_dataframe_agent(
        selected_llm, 
        df, 
        verbose=True,  # Debug için işlem adımlarını göster
        agent_executor_kwargs={"handle_parsing_errors": "True"}  # Hata yönetimi
    )

    # Sonuçları saklamak için boş sözlük
    data_summary = {}

    # ---------------------------------------------------------------------------
    # ÖRNEK VERİ KESİTİ
    # ---------------------------------------------------------------------------
    # İlk 5 satırı alarak kullanıcıya verinin yapısını gösteriyoruz
    # NEDEN HEAD()? Kullanıcı verinin nasıl göründüğünü anlar
    data_summary["initial_data_sample"] = df.head()

    # ---------------------------------------------------------------------------
    # SÜTUN AÇIKLAMALARI (AI DESTEKLİ)
    # ---------------------------------------------------------------------------
    # AI'dan her sütun için Türkçe açıklama istiyoruz
    # NEDEN AI? Sütun isimlerinden içeriği otomatik çıkarabilir
    # PROMPT ÖNEMİ: Türkçe ve tablo formatı istiyoruz
    data_summary["column_descriptions"] = pandas_agent.run(
        "Verideki sütunları içeren bir tablo yap. "
        "Tabloda sütunların adları ve yanlarında kısaca içerdikleri bilgiye dair "
        "Türkçe bir açıklama yer alsın. Bunu bir tablo olarak ver."
    )

    # ---------------------------------------------------------------------------
    # EKSİK VERİ ANALİZİ (AI DESTEKLİ)
    # ---------------------------------------------------------------------------
    # AI'dan eksik veri sayısını istiyoruz
    # NEDEN ÖNEMLİ? Eksik veriler analiz sonuçlarını etkiler
    # VERİ KALİTESİ: İlk adım eksik verileri tespit etmektir
    data_summary["missing_values"] = pandas_agent.run(
        "Bu veri kümesinde eksik veri var mı? Varsa kaç adet var? "
        "Yanıtını 'Bu veri kümesinde X adet hücrede eksik veri var' şeklinde ver."
    )

    # ---------------------------------------------------------------------------
    # MÜKERRER VERİ ANALİZİ (AI DESTEKLİ)
    # ---------------------------------------------------------------------------
    # AI'dan tekrarlanan kayıtları tespit etmesini istiyoruz
    # NEDEN ÖNEMLİ? Mükerrer kayıtlar istatistikleri çarpıtır
    # VERİ BÜTÜNLÜĞÜ: Temiz veri için mükerrerler kontrol edilmeli
    data_summary["duplicate_values"] = pandas_agent.run(
        "Bu veri kümesinde mükerrer veri var mı? Varsa kaç adet var? "
        "Yanıtını 'Bu veri kümesinde X adet hücrede mükerrer veri var' şeklinde ver."
    )

    # ---------------------------------------------------------------------------
    # TEMEL İSTATİSTİKLER
    # ---------------------------------------------------------------------------
    # Pandas describe() ile temel metrikleri hesaplıyoruz
    # BU NE İÇERİR?
    # - count: Değer sayısı
    # - mean: Ortalama
    # - std: Standart sapma
    # - min/max: Minimum ve maksimum değerler
    # - 25%, 50%, 75%: Çeyrekler (quartiles)
    data_summary["essential_metrics"] = df.describe()

    return data_summary


# ===================================================================================
# DATAFRAME ALMA FONKSİYONU
# ===================================================================================

def get_dataframe(data_file):
    """
    CSV dosyasını Pandas DataFrame'e dönüştürür.
    
    NEDEN AYRI BİR FONKSİYON?
    -------------------------
    - Tek Sorumluluk Prensibi: Her fonksiyon bir iş yapar
    - Yeniden kullanılabilirlik: Birden fazla yerde çağrılabilir
    - Bakım kolaylığı: Okuma mantığı tek yerde
    
    BU BİZE NE SAĞLAR?
    ------------------
    - Tutarlı veri okuma
    - Merkezi hata yönetimi imkanı
    - Kolay test edilebilirlik
    
    Args:
        data_file: Streamlit tarafından yüklenen dosya objesi
        
    Returns:
        pd.DataFrame: CSV verisini içeren DataFrame
    """
    
    # low_memory=False: Tip çıkarımını iyileştirir
    df = pd.read_csv(data_file, low_memory=False)

    return df


# ===================================================================================
# TREND ANALİZİ FONKSİYONU
# ===================================================================================

def analyze_trend(data_file, variable_of_interest):
    """
    Belirtilen değişkenin zaman içindeki değişim trendini analiz eder.
    
    NEDEN BU FONKSİYON ÖNEMLİ?
    --------------------------
    - Zaman serisi verilerinde trend analizi kritiktir
    - Manuel analiz zaman alır ve uzmanlık gerektirir
    - AI, verideki kalıpları otomatik tespit edebilir
    
    BU BİZE NE SAĞLAR?
    ------------------
    - Otomatik trend yorumlama
    - Türkçe, anlaşılır açıklamalar
    - Teknik bilgi gerektirmeden analiz
    
    ÖRNEK KULLANIM:
    ---------------
    >>> analyze_trend(data_file, "Fiyat")
    "Fiyat değişkeni son 6 ayda %15 artış göstermiştir..."
    
    Args:
        data_file: Streamlit tarafından yüklenen dosya objesi
        variable_of_interest: Analiz edilecek sütun adı (string)
        
    Returns:
        str: AI tarafından üretilen Türkçe trend yorumu
    """
    
    # CSV'yi DataFrame'e dönüştür
    df = pd.read_csv(data_file, low_memory=False)

    # Pandas Agent oluştur
    pandas_agent = create_pandas_dataframe_agent(
        selected_llm, 
        df, 
        verbose=True, 
        agent_executor_kwargs={"handle_parsing_errors": "True"}
    )

    # ===================================================================================
    # TREND ANALİZİ PROMPTU
    # ===================================================================================
    # Bu prompt, AI'ın doğru bir trend analizi yapmasını sağlar.
    # 
    # PROMPT TASARIMI:
    # ----------------
    # 1. Değişken adı dinamik olarak ekleniyor
    # 2. "Yorumlamayı reddetme" - AI'ın kaçınmasını engelliyor
    # 3. "Satırlar geçmişten günümüze" - Veri yapısını açıklıyor
    # 4. "Türkçe" - Çıktı dilini belirliyor
    
    trend_response = pandas_agent.run(
        f"Veri kümesi içindeki şu değişkenin değişim trendini kısaca yorumla: {variable_of_interest} "
        "Yorumlamayı reddetme. "
        "Verideki satırlar geçmişten günümüze tarih bazlı olduğu için, "
        "verideki satırlara bakarak yorumda bulunabilirsin. "
        "Yanıtın Türkçe olarak ver."
    )

    return trend_response


# ===================================================================================
# SERBEST SORU CEVAPLAMA FONKSİYONU
# ===================================================================================

def ask_question(data_file, question):
    """
    Kullanıcının veri kümesiyle ilgili serbest sorusunu AI ile yanıtlar.
    
    NEDEN BU FONKSİYON EN GÜÇLÜ ÖZELLİK?
    ------------------------------------
    - Doğal dilde soru sorma imkanı
    - SQL veya Python bilgisi gerektirmez
    - Karmaşık analizler basit sorularla yapılabilir
    - Veri demokratizasyonunun özü budur
    
    BU BİZE NE SAĞLAR?
    ------------------
    - Herkesin veri analizi yapabilmesi
    - Hızlı insight elde etme
    - Teknik bariyerlerin kaldırılması
    
    ÖRNEK SORULAR:
    --------------
    - "En yüksek satış hangi günde gerçekleşti?"
    - "Ortalama müşteri yaşı kaç?"
    - "Hangi ürün kategorisi en çok satıyor?"
    - "Son 3 ayın toplam geliri ne kadar?"
    
    ARKA PLANDA NE OLUYOR?
    ----------------------
    1. AI soruyu analiz eder
    2. Gerekli Pandas kodu üretilir (örn: df.groupby().sum())
    3. Kod DataFrame üzerinde çalıştırılır
    4. Sonuç Türkçe olarak formatlanır
    
    Args:
        data_file: Streamlit tarafından yüklenen dosya objesi
        question: Kullanıcının sorduğu Türkçe soru (string)
        
    Returns:
        str: AI tarafından üretilen Türkçe yanıt
    """
    
    # CSV'yi DataFrame'e dönüştür
    df = pd.read_csv(data_file, low_memory=False)

    # Pandas Agent oluştur
    pandas_agent = create_pandas_dataframe_agent(
        selected_llm, 
        df, 
        verbose=True, 
        agent_executor_kwargs={"handle_parsing_errors": "True"}
    )

    # ===================================================================================
    # SORU CEVAPLAMA PROMPTU
    # ===================================================================================
    # Kullanıcının sorusunu AI'a iletiyoruz.
    # 
    # PROMPT TASARIMI:
    # ----------------
    # - Kullanıcının sorusu olduğu gibi ekleniyor
    # - "Bu soruyu Türkçe yanıtla" - Çıktı dilini garantiliyor
    # 
    # ÖNEMLİ NOT:
    # -----------
    # AI, soruyu anlamak için bağlam olarak DataFrame'i kullanır.
    # Soru açık ve net olmalı, belirsiz sorular hatalı sonuç verebilir.
    
    AI_Response = pandas_agent.run(f"{question} Bu soruyu Türkçe yanıtla.")

    return AI_Response


# ===================================================================================
# MODÜL SONU
# ===================================================================================
# Bu modül, Data Explorer uygulamasının kalbi niteliğindedir.
# LangChain'in gücünü kullanarak veri analizi süreçlerini demokratikleştirir.
# 
# GELİŞTİRME ÖNERİLERİ:
# ---------------------
# 1. Model seçimi için UI ekleme
# 2. Hata yönetimi geliştirme
# 3. Önbellek mekanizması ekleme
# 4. Loglama sistemi kurma
# 5. Prompt optimizasyonu
# 6. Çoklu dil desteği
# ===================================================================================
