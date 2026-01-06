"""
===================================================================================
ORHAN VELİ ŞİİRLERİ ETİKETLEME UYGULAMASI (Poem Labeling Application)
===================================================================================

Bu modül, Orhan Veli şiirlerini Google Gemini AI kullanarak otomatik olarak 
etiketleyen bir Streamlit web uygulamasını içerir.

AMAÇ:
-----
- Şiirlerin konu, tema, duygu ve motiflerini yapay zeka ile otomatik belirlemek
- Fine-tuning (ince ayar) için eğitim verisi hazırlamak
- Şiir analizi sürecini otomasyona kavuşturmak

ÇALIŞMA PRENSİBİ:
-----------------
1. Excel dosyasından şiirler okunur
2. Her şiir için Gemini AI'a istek gönderilir
3. AI, şiirin konu/tema/duygu/motiflerini tespit eder
4. Sonuçlar aynı Excel dosyasına 'response' sütununa yazılır

KULLANIM:
---------
Terminal'de çalıştırmak için:
    streamlit run assign_labels.py

NOT: Bu uygulama, Fine-Tuning veri seti hazırlığının ilk adımıdır.
Etiketlenen şiirler daha sonra prepare_ft_file.py ile JSONL formatına dönüştürülür.

GEREKSINIMLER:
--------------
- streamlit: Web arayüzü için
- pandas: Excel dosya işlemleri için
- langchain_google_genai: Google Gemini AI entegrasyonu için
- python-dotenv: Çevre değişkenleri yönetimi için
- openpyxl: Excel dosya okuma/yazma motoru

Yazar: [Proje Sahibi]
Tarih: 2024
===================================================================================
"""

# ===================================================================================
# KÜTÜPHANE İMPORTLARI (Library Imports)
# ===================================================================================

import os                                    # İşletim sistemi işlemleri (environment variables)
import pandas as pd                          # Veri manipülasyonu ve Excel işlemleri
import streamlit as st                       # Web arayüzü oluşturma framework'ü
from dotenv import load_dotenv               # .env dosyasından çevre değişkenlerini yükleme
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini AI entegrasyonu

# ===================================================================================
# ÇEVRE DEĞİŞKENLERİ VE AI MODEL YAPILANDIRMASI
# (Environment Variables and AI Model Configuration)
# ===================================================================================

# .env dosyasındaki çevre değişkenlerini sisteme yükle
# Bu dosyada API anahtarları gibi hassas bilgiler güvenli şekilde saklanır
load_dotenv()

# Google Gemini API anahtarını çevre değişkenlerinden al
# NOT: Güvenlik için API anahtarları asla kod içinde açık yazılmamalıdır
my_key_google = os.getenv("google_apikey")

# Google Gemini Pro modelini başlat
# gemini-pro: Google'ın güçlü dil modeli, metin analizi ve üretimi için optimize edilmiş
llm_gemini = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=my_key_google)

# ===================================================================================
# PROMPT TANIMLAMALARI (Prompt Definitions)
# ===================================================================================

# Sistem promptu: AI'ın nasıl davranacağını ve yanıt formatını belirler
# Bu prompt, modelin bir Türk edebiyatı uzmanı gibi davranmasını sağlar
system_prompt = """Sen bir Türk edebiyatı uzmanısın. Türk şiir literatürünü çok iyi biliyorsun.
Özellikle de Orhan Veli şiirlerini çok iyi biliyorsun.
Sana verilen Orhan Veli şiirlerinde ele alınan konuyu, temayı, duyguyu, şiirdeki başlıca motifleri tespit edebiliyorsun.
Yanıtını verirken bu tespit ettiğin konu, tema, duygu veya motifleri aralarında birer virgül olacak şekilde yazıyorsun.
Yanıtında sadece bunları yazıyorsun. Başka hiçbir açıklama ya da ek bilgi vermiyorsun.
"""

# Kullanıcı promptu: Her şiir için gönderilecek temel istek
# Bu prompt, sistem promptu ile birleştirilerek tam sorgu oluşturulur
prompt = "Orhan Veli'nin aşağıdaki şiirinde ele alınan konu, tema, duygu veya motifleri yaz."

# ===================================================================================
# DOSYA YOLLARI (File Paths)
# ===================================================================================

# Kaynak ve hedef Excel dosyasının yolu
# NOT: Dosya yolu assets klasöründen çekilmektedir
source_file_path = "../assets/19.8-Materyaller/data/siir.xlsx"
target_file_path = source_file_path  # Aynı dosyaya yazılacak (güncelleme modu)

# ===================================================================================
# STREAMLIT SAYFA YAPILANDIRMASI (Streamlit Page Configuration)
# ===================================================================================

# Tarayıcı sekmesinde görünecek sayfa başlığını ayarla
st.set_page_config(page_title="Şiir Etiketleme Uygulaması")

# Uygulama ana başlığı
st.title("Şiir Etiketleme Uygulaması")

# Görsel ayırıcı çizgi
st.divider()

# ===================================================================================
# KULLANICI GİRİŞ KONTROLLER (User Input Controls)
# ===================================================================================

# Başlangıç satırı seçici
# min_value=1: Excel'de satırlar 1'den başlar (0 değil)
# value=1: Varsayılan başlangıç değeri
start_row = st.number_input("Başlangıç Satırı", min_value=1, value=1)

# Bitiş satırı seçici
# Kullanıcı hangi satıra kadar işlem yapılacağını belirler
end_row = st.number_input("Bitiş Satırı", min_value=1, value=10)

# Etiketleme işlemini başlatacak buton
submit_btn = st.button(label='Etiketle')

# ===================================================================================
# ANA İŞLEM DÖNGÜSÜ (Main Processing Loop)
# ===================================================================================

# Kullanıcı "Etiketle" butonuna bastığında işlem başlar
if submit_btn:

    # Excel dosyasını pandas DataFrame olarak oku
    # engine="openpyxl": .xlsx formatı için gerekli okuma motoru
    df = pd.read_excel(source_file_path, engine="openpyxl")

    # İlerleme çubuğunu başlat (kullanıcıya görsel geri bildirim)
    progress_bar = st.progress(0)
    
    # Toplam işlenecek satır sayısını hesapla
    total_rows = end_row - start_row + 1

    # Belirtilen satır aralığındaki her şiir için döngü
    # iloc[start_row-1:end_row]: Python 0-indexed, kullanıcı 1-indexed
    for index, row in df.iloc[start_row-1:end_row].iterrows():

        try:
            # Mevcut satırdaki şiir metnini al
            siir = row['siir']

            # Sistem promptu, kullanıcı promptu ve şiiri birleştirerek tam prompt oluştur
            # Bu format, AI'ın hem rolünü hem de görevi anlamasını sağlar
            full_prompt = f"{system_prompt} {prompt} {siir}"

            # Google Gemini AI'a istek gönder ve yanıt al
            # invoke(): LangChain'in standart model çağrı metodu
            AI_response = llm_gemini.invoke(input=full_prompt)
            
            # AI yanıtını DataFrame'in 'response' sütununa yaz
            # .content: AI yanıtının metin içeriğini alır
            df.at[index, 'response'] = AI_response.content

        except Exception as e:
            # Hata durumunda kullanıcıyı bilgilendir ve sonraki satıra geç
            # Bu yaklaşım, tek bir hatanın tüm işlemi durdurmasını önler
            st.error(f"Şu satırı işlerken hata oluştu: {index + 1}: {e}. Sonraki satıra geçiliyor...")
            continue
        
        # İlerleme çubuğunu güncelle
        # progress_percentage: 0.0 ile 1.0 arasında bir değer
        progress_percentage = (index + 1 - (start_row-1)) / total_rows
        progress_bar.progress(progress_percentage)
    
    # Güncellenmiş DataFrame'i Excel dosyasına kaydet
    # index=False: DataFrame index'ini dosyaya yazma
    df.to_excel(target_file_path, index=False, engine="openpyxl")
    
    # İlerleme çubuğunu temizle (işlem tamamlandı)
    progress_bar.empty()
    
    # Başarı mesajı göster
    st.success("Etiketleme İşlemi Tamamlandı")

# ===================================================================================
# VERİ GÖRÜNTÜLEME (Data Display)
# ===================================================================================

# Excel dosyasının güncel halini tablo olarak göster
# Bu, kullanıcının hem işlem öncesi hem sonrası veriyi görmesini sağlar
st.dataframe(pd.read_excel(target_file_path, engine="openpyxl"))
