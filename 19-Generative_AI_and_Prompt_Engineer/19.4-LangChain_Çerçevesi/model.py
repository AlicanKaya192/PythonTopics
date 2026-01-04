# ==============================================================================
# LangChain ile Farklı LLM Model Karşılaştırma Uygulaması
# ==============================================================================
# Bu Streamlit uygulaması, aynı soruyu farklı büyük dil modellerine (LLM) sorarak
# yanıtlarını yan yana karşılaştırmanızı sağlar.
#
# Neden model karşılaştırması önemli?
# -----------------------------------
# Her LLM'in kendine özgü güçlü ve zayıf yönleri vardır:
# - GPT-4: Genel zeka ve kod yazma konusunda çok başarılı
# - Gemini: Google'ın modeli, güncel bilgiler konusunda avantajlı
# - Claude: Uzun metinleri işleme ve detaylı analiz konusunda güçlü
# - Command: Cohere'nin modeli, arama ve özet çıkarma için optimize
#
# Bu uygulama sayesinde:
# 1. Aynı soruya farklı modellerin nasıl yaklaştığını görebilirsiniz
# 2. Yanıt sürelerini karşılaştırabilirsiniz
# 3. Temperature ve token ayarlarının etkisini gözlemleyebilirsiniz
# 4. Projeleriniz için en uygun modeli seçebilirsiniz
#
# Temperature nedir?
# ------------------
# 0.0 = Deterministik, tutarlı yanıtlar (tekrarlanabilir)
# 0.5 = Dengeli yaratıcılık
# 1.0 = Maksimum yaratıcılık (her seferinde farklı yanıt)
#
# Max tokens nedir?
# -----------------
# Modelin üretebileceği maksimum kelime/token sayısı
# Kısa yanıtlar: 100-200
# Orta yanıtlar: 300-500
# Uzun yanıtlar: 500+
# ==============================================================================

import streamlit as st
import modelhelper  # API çağrılarını yapan yardımcı modülümüz
import time  # Yanıt sürelerini ölçmek için

# Streamlit sayfa ayarları
# layout="wide": Geniş ekran düzeni, 4 modeli yan yana göstermek için ideal
st.set_page_config(page_title="LangChain: Model Karşılaştırma", layout="wide")
st.title("LangChain: Model Karşılaştırma")
st.divider()

# Ana düzeni iki sütuna böl: Sol taraf giriş, sağ taraf ayarlar
col_prompt, col_settings = st.columns([2, 3])

# Sol sütun: Soru girişi ve gönder butonu
with col_prompt:
    # Kullanıcının sorusunu al
    # Bu soru tüm modellere aynı şekilde gönderilecek
    prompt = st.text_input(label="Sorunuzu giriniz:")
    st.divider()
    submit_btn = st.button("Sor")

# Sağ sütun: Model parametreleri
with col_settings:
    # Temperature: Yanıtların yaratıcılık/rastgelelik seviyesi
    # Düşük değer = daha öngörülebilir, tutarlı yanıtlar
    # Yüksek değer = daha yaratıcı ama bazen tutarsız yanıtlar
    temperature = st.slider(
        label="Temperature", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7  # Varsayılan: hafif yaratıcı
    )
    
    # Maximum Tokens: Yanıtın maksimum uzunluğu
    # Dikkat: Her model farklı token hesabı kullanır
    # Genel kural: 1 token ≈ 0.75 kelime (İngilizce için)
    max_tokens = st.slider(
        label="Maximum Tokens", 
        min_value=100, 
        max_value=500, 
        value=200, 
        step=100
    )

st.divider()

# Dört sütun oluştur - her model için bir sütun
# Bu sayede yanıtları yan yana görebilir ve kolayca karşılaştırabilirsiniz
col_gpt, col_gemini, col_claude, col_command = st.columns(4)

# GPT-4 Turbo sütunu
with col_gpt:
    if submit_btn:
        # st.spinner: İşlem sürerken kullanıcıya görsel geri bildirim
        with st.spinner("GPT Yanıtlıyor..."):
            st.success("GPT-4 Turbo")  # Yeşil başlık kutusu
            
            # Performans ölçümü başlat
            start_time = time.perf_counter()
            
            # modelhelper modülü üzerinden GPT API çağrısı yap
            # Bu ayrı bir modülde tutulur çünkü:
            # 1. Kodun okunabilirliği artar
            # 2. API mantığı UI mantığından ayrılır (separation of concerns)
            # 3. Birden fazla yerden aynı fonksiyonu kullanabiliriz
            st.write(modelhelper.ask_gpt(prompt=prompt, temperature=temperature, max_tokens=max_tokens))
            
            # Performans ölçümü bitir
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            
            # Yanıt süresini göster - kum saati emojisi ile
            st.caption(f"| :hourglass: {round(elapsed_time)} saniye")


# Gemini Pro sütunu
with col_gemini:
    if submit_btn:
        with st.spinner("Gemini Yanıtlıyor..."):
            st.info("Gemini Pro")  # Mavi başlık kutusu
            
            start_time = time.perf_counter()
            
            # Not: Gemini için max_tokens parametresi bu wrapper'da desteklenmiyor
            # Eğer ihtiyaç varsa modelhelper.py'de ayarlanabilir
            st.write(modelhelper.ask_gemini(prompt=prompt, temperature=temperature))
            
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            st.caption(f"| :hourglass: {round(elapsed_time)} saniye")


# Claude 2.1 sütunu
with col_claude:
    if submit_btn:
        with st.spinner("Claude Yanıtlıyor..."):
            st.error("Claude 2.1")  # Kırmızı başlık kutusu (Anthropic rengi)
            
            start_time = time.perf_counter()
            
            # Claude, uzun ve detaylı yanıtlar verme konusunda başarılı
            # Özellikle karmaşık analiz ve açıklama gerektiren sorularda
            st.write(modelhelper.ask_claude(prompt=prompt, temperature=temperature, max_tokens=max_tokens))
            
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            st.caption(f"| :hourglass: {round(elapsed_time)} saniye")


# Command (Cohere) sütunu
with col_command:
    if submit_btn:
        with st.spinner("Command Yanıtlıyor..."):
            st.warning("Command")  # Sarı başlık kutusu
            
            start_time = time.perf_counter()
            
            # Cohere Command, özellikle iş uygulamaları için optimize edilmiş
            # Özet çıkarma, arama ve sınıflandırma konularında güçlü
            st.write(modelhelper.ask_command(prompt=prompt, temperature=temperature, max_tokens=max_tokens))
            
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            st.caption(f"| :hourglass: {round(elapsed_time)} saniye")