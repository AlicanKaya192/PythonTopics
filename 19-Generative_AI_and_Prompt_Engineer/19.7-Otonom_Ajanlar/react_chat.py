# =======================================================================================
# DOSYA: react_chat.py
# AÇIKLAMA: Streamlit tabanlı interaktif ReAct ajan sohbet uygulaması.
#           Kullanıcıların web araması, görsel üretimi ve web scraping yapabilen
#           bir yapay zeka ajanıyla sohbet etmesini sağlar.
#
# KONU: OTONOM AJANLAR - ReAct Yaklaşımı ve Çoklu Araç Entegrasyonu
# 
# Bu uygulama şu özelliklere sahiptir:
# - Farklı LLM sağlayıcıları arasında seçim (GPT-4, Gemini, Claude)
# - Farklı arama motorları (DuckDuckGo, Tavily)
# - Görsel üretim modelleri (DALL-E 3, Stable Diffusion XL)
# - Web scraping (BeautifulSoup)
# - Sohbet geçmişi ve anlık geri bildirim
#
# STREAMLIT CALLBACK HANDLER
# ==========================
# Streamlit uygulamalarında ReAct ajanının düşünce sürecini
# gerçek zamanlı olarak göstermek için StreamlitCallbackHandler kullanılır.
# Bu sayede kullanıcı:
# - Ajanın Thought adımlarını görür
# - Hangi Action'ların yapıldığını izler
# - Observation sonuçlarını anlar
#
# AJAN KONFİGÜRASYONU
# ====================
# Bu uygulama, kullanıcıya farklı bileşenler arasında seçim yapma imkanı sunar:
# 1. Dil Modeli: GPT-4, Gemini Pro, Claude 2.1
# 2. Arama Motoru: DuckDuckGo (ücretsiz), Tavily (yapılandırılmış)
# 3. Görsel Üretici: Stable Diffusion XL, DALL-E 3
# 4. Web Scraper: BeautifulSoup
# =======================================================================================

from langchain.agents import AgentExecutor, create_react_agent, load_tools  # LangChain ajan araçları
from langchain_openai import ChatOpenAI  # OpenAI GPT modeli
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini modeli
from langchain_community.chat_models import ChatAnthropic  # Anthropic Claude modeli
from langchain import hub  # LangChain Hub - prompt şablonları
from langchain_community.callbacks import StreamlitCallbackHandler  # Streamlit entegrasyonu
from langchain_community.tools.tavily_search import TavilySearchResults  # Tavily arama aracı
import streamlit as st  # Streamlit web framework
import os  # İşletim sistemi işlemleri
import customtools  # Özel araç tanımları (görsel üretim, web scraping)
from dotenv import load_dotenv  # Ortam değişkenleri yükleme

# =======================================================================================
# ORTAM DEĞİŞKENLERİ VE API YAPILANDIRMASI
# =======================================================================================
# Farklı LLM sağlayıcıları için API anahtarları .env dosyasından yüklenir.
# Her sağlayıcı kendi anahtarını kullanır.
# =======================================================================================

load_dotenv()  # .env dosyasını ortam değişkenlerine yükle

# API anahtarlarını ortam değişkenlerinden al
my_key_openai = os.getenv("openai_apikey")  # OpenAI API anahtarı (GPT-4 + DALL-E)
my_key_google = os.getenv("google_apikey")  # Google Gemini API anahtarı
my_key_anthropic = os.getenv("anthropic_apikey")  # Anthropic Claude API anahtarı

# Tavily arama API anahtarını ortam değişkenine ayarla
# LangChain bu değişkeni otomatik olarak okur
os.environ["TAVILY_API_KEY"] = os.getenv("tavily_apikey")

# =======================================================================================
# DİL MODELLERİNİN OLUŞTURULMASI
# =======================================================================================
# Üç farklı LLM sağlayıcısını aynı anda hazır tutuyoruz.
# Kullanıcı sidebar'dan seçim yapabilir.
#
# ChatGoogleGenerativeAI (Gemini Pro):
# - Google'ın çok modlu AI modeli
# - Ücretsiz API kullanım kotası mevcut
#
# ChatOpenAI (GPT-4 Turbo):
# - OpenAI'nin en gelişmiş sohbet modeli
# - streaming=True: Yanıtları token token alır (gerçek zamanlı)
# - temperature=0: Deterministik yanıtlar (her seferinde aynı)
#
# ChatAnthropic (Claude 2.1):
# - Anthropic'in güvenlik odaklı AI modeli
# - Daha uzun bağlam penceresi (200k token)
# =======================================================================================

# Google Gemini Pro modeli
llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro")

# OpenAI GPT-4 Turbo modeli (streaming etkin)
llm_gpt = ChatOpenAI(api_key=my_key_openai, model="gpt-4-0125-preview", temperature=0, streaming=True)

# Anthropic Claude 2.1 modeli
llm_claude = ChatAnthropic(anthropic_api_key=my_key_anthropic, model_name="claude-2.1")

# =======================================================================================
# REACT PROMPT ŞABLONU
# =======================================================================================
# LangChain Hub'dan standart ReAct promptunu çek.
# Bu prompt, ajanın Thought/Action/Observation formatını takip etmesini sağlar.
# =======================================================================================

agent_prompt = hub.pull("hwchase17/react")  # Harrison Chase'in standart ReAct promptu


def configure_agent(selected_llm, selected_search_engine, selected_image_generator):
    """
    Kullanıcı seçimlerine göre ReAct ajanını yapılandırır.
    
    Bu fonksiyon:
    1. Seçilen LLM'i belirler
    2. Arama aracını ayarlar
    3. Görsel üretim aracını ekler
    4. Web scraping aracını ekler
    5. Tüm araçları içeren bir ajan oluşturur
    
    Parametreler:
    -------------
    selected_llm (str): Seçilen dil modeli ("GPT-4", "Gemini Pro", "Claude 2.1")
    selected_search_engine (str): Seçilen arama motoru ("DuckDuckGo", "Tavily")
    selected_image_generator (str): Seçilen görsel üretici ("Stable Diffusion XL", "DALL-E 3")
    
    Returns:
        AgentExecutor: Yapılandırılmış ve çalışmaya hazır ajan
    """
    # -------------------------------------------------------------------------
    # DİL MODELİ SEÇİMİ
    # -------------------------------------------------------------------------
    # Kullanıcının sidebar'dan seçtiği modele göre LLM belirlenir.
    # Her model farklı avantajlar sunar:
    # - GPT-4: En yüksek doğruluk, iyi araç kullanımı
    # - Gemini Pro: Hızlı, çok modlu yetenekler
    # - Claude 2.1: Uzun bağlam, güvenlik odaklı
    # -------------------------------------------------------------------------
    
    if selected_llm == "GPT-4":
        llm = llm_gpt
    elif selected_llm == "Gemini Pro":
        llm = llm_gemini
    elif selected_llm == "Claude 2.1":
        llm = llm_claude

    # -------------------------------------------------------------------------
    # ÖZEL ARAÇLARIN OLUŞTURULMASI
    # -------------------------------------------------------------------------
    # customtools modülünden görsel üretim ve web scraping araçları alınır.
    # Bu araçlar, ajanın kullanabileceği "yetenekler"dir.
    # -------------------------------------------------------------------------
    
    # Görsel üretim aracı (DALL-E 3 veya Stable Diffusion XL)
    image_generator_tool = customtools.get_tool(selected_image_generator=selected_image_generator)
    
    # Web scraping aracı (BeautifulSoup tabanlı)
    web_scraping_tool = customtools.get_web_tool()
    
    # -------------------------------------------------------------------------
    # ARAMA MOTORU SEÇİMİ VE ARAÇ LİSTESİ
    # -------------------------------------------------------------------------
    # İki arama motoru seçeneği:
    # 
    # DuckDuckGo:
    # - Ücretsiz
    # - API anahtarı gerektirmez
    # - Gizlilik odaklı
    # - load_tools() ile yüklenir
    #
    # Tavily:
    # - LLM için optimize edilmiş sonuçlar
    # - Daha yapılandırılmış çıktı
    # - API anahtarı gerektirir
    # -------------------------------------------------------------------------
    
    if selected_search_engine == "DuckDuckGo":
        # DuckDuckGo aramayı yükle ve diğer araçları ekle
        tools = load_tools(["ddg-search"])  # DuckDuckGo Search aracı
        tools.extend([image_generator_tool, web_scraping_tool])  # Özel araçları ekle
        
    elif selected_search_engine == "Tavily":
        # Tavily ve diğer araçları tek listede oluştur
        tools = [TavilySearchResults(max_results=1), image_generator_tool, web_scraping_tool]

    # -------------------------------------------------------------------------
    # AJAN VE EXECUTOR OLUŞTURMA
    # -------------------------------------------------------------------------
    # create_react_agent: LLM, araçlar ve promptu birleştirerek ajan oluşturur
    # AgentExecutor: Ajanı çalıştıran ve yöneten orkestratör
    # -------------------------------------------------------------------------
    
    # ReAct ajanını oluştur
    agent = create_react_agent(llm=llm, tools=tools, prompt=agent_prompt)
    
    # AgentExecutor oluştur - ajanı çalıştıracak
    # verbose=True: Tüm Thought/Action/Observation adımlarını logla
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


# =======================================================================================
# STREAMLIT SAYFA YAPILANDIRMASI
# =======================================================================================
# Streamlit, Python ile hızlı web uygulamaları geliştirmek için kullanılır.
# UI bileşenleri Python kodu ile tanımlanır.
# =======================================================================================

# Sayfa ayarları - tarayıcı sekmesinde görünen başlık
st.set_page_config(page_title="ReAct Ajan ile Sohbet Etkileşimi")

# Banner görseli - assets klasöründen yüklenir
st.image(image="../assets/19.7-Materyaller/img/ai_agent_banner.png")

# Ana başlık
st.title("ReAct Ajan ile Sohbet Etkileşimi")

# Görsel ayırıcı çizgi
st.divider()


# =======================================================================================
# SIDEBAR KONFİGÜRASYONU
# =======================================================================================
# Sidebar, kullanıcının ajan ayarlarını yapmasını sağlar.
# Radio butonları ile tek seçim yapılır.
#
# Streamlit Radio Widget:
# - label: Widget başlığı
# - options: Seçenekler listesi
# - index: Varsayılan seçilen öğe (0-indexed)
# =======================================================================================

st.sidebar.header("Ajan Konfigürasyonu")  # Sidebar başlığı
st.sidebar.divider()

# Dil modeli seçimi
# GPT-4: En güçlü, ücretli
# Gemini Pro: Dengeli, ücretsiz kota
# Claude 2.1: Uzun bağlam, güvenlik
selected_llm = st.sidebar.radio(label="Dil Modeli Seçiniz", options=["GPT-4", "Gemini Pro", "Claude 2.1"])
st.sidebar.divider()

# Arama motoru seçimi
# DuckDuckGo: Ücretsiz, gizlilik odaklı
# Tavily: LLM optimize, ücretli
selected_search_engine = st.sidebar.radio(label="Arama Motoru Seçiniz", options=["DuckDuckGo", "Tavily"], index=1)
st.sidebar.divider()

# Görsel üretim modeli seçimi
# Stable Diffusion XL: Açık kaynak, esnek
# DALL-E 3: OpenAI, yüksek kalite
selected_image_generator = st.sidebar.radio(label="Resim Üretim Modelini Seçiniz", options=["Stable Diffusion XL","DALL-E 3"])
st.sidebar.divider()

# Web scraping aracı seçimi (şimdilik sadece BeautifulSoup)
selected_web_scraper = st.sidebar.radio(label="Web Kazıma Aracı Seçiniz", options=["BeautifulSoup"])
st.sidebar.divider()

# Türkçe yanıt zorlama seçeneği
# Aktif ise her soruya "Bu soruyu Türkçe yanıtla" eklenir
turkish_sensitivity = st.sidebar.checkbox(label="Türkçe Yanıta Zorla", value=True)
st.sidebar.divider()

# Sohbet geçmişini sıfırlama butonu
reset_chat_btn = st.sidebar.button(label="Sohbeti Geçmişini Sıfırla")


# =======================================================================================
# SESSION STATE YÖNETİMİ
# =======================================================================================
# Streamlit, her etkileşimde scripti yeniden çalıştırır.
# session_state, veriler sayfa yenilemeleri arasında korunmasını sağlar.
# =======================================================================================

# messages listesi yoksa oluştur
# Her mesaj {"role": "user/assistant", "content": "..."} formatında
if "messages" not in st.session_state:
    st.session_state.messages = []


# =======================================================================================
# SOHBET GEÇMİŞİNİ GÖRÜNTÜLEME
# =======================================================================================
# Daha önce gönderilen tüm mesajları ekrana yazdır.
# st.chat_message(): Mesajı uygun baloncukta gösterir
# st.markdown(): Mesaj içeriğini Markdown formatında render eder
# =======================================================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =======================================================================================
# KULLANICI GİRİŞİ VE AJAN YANITI
# =======================================================================================
# Ana sohbet döngüsü:
# 1. Kullanıcı mesaj yazar
# 2. Mesaj session_state'e eklenir
# 3. Ajan yapılandırılır ve çalıştırılır
# 4. Yanıt görüntülenir ve kaydedilir
# =======================================================================================

if prompt := st.chat_input(placeholder="Mesajınızı yazınız"):
    # Kullanıcı mesajını hemen göster
    st.chat_message("user").write(prompt)

    # Türkçe zorlama aktifse, mesaja Türkçe talimatı ekle
    if turkish_sensitivity:
        st.session_state.messages.append({"role":"user", "content": prompt + "Bu soruyu Türkçe yanıtla"})
    else:
        st.session_state.messages.append({"role":"user", "content": prompt})
    
    # Asistan yanıtı için chat baloncuğu
    with st.chat_message("assistant"):
        # Bilgi mesajı - ajan çalışıyor
        st.info("🧠 Düşünce Zinciri İşletiliyor...")

        # ---------------------------------------------------------------------
        # STREAMLIT CALLBACK HANDLER
        # ---------------------------------------------------------------------
        # StreamlitCallbackHandler, ajanın düşünce sürecini gerçek zamanlı
        # olarak Streamlit arayüzünde gösterir.
        # 
        # st.container(): Callback'lerin yazılacağı alan
        # Handler, her Thought/Action/Observation için UI günceller
        # ---------------------------------------------------------------------
        
        st_callback = StreamlitCallbackHandler(st.container())

        # ---------------------------------------------------------------------
        # AJANI YAPILANDIR VE ÇALIŞTIR
        # ---------------------------------------------------------------------
        # configure_agent(): Kullanıcı seçimlerine göre ajan oluştur
        # executor.invoke(): Ajanı çalıştır ve yanıt al
        # 
        # callbacks: StreamlitCallbackHandler'ı ekleyerek gerçek zamanlı
        #            görünüm sağla
        # handle_parsing_errors: Parse hatalarında otomatik düzeltme
        # ---------------------------------------------------------------------
        
        # Seçilen ayarlara göre ajanı yapılandır
        executor = configure_agent(
            selected_llm=selected_llm, 
            selected_search_engine=selected_search_engine, 
            selected_image_generator=selected_image_generator
        )

        # Ajanı çalıştır
        # input: Tüm sohbet geçmişi (bağlam için)
        # callbacks: Gerçek zamanlı UI güncellemesi için
        AI_Response = executor.invoke(
            {"input": st.session_state.messages}, 
            {"callbacks": [st_callback]},
            handle_parsing_errors=True
        )

        # Final yanıtı görüntüle
        # unsafe_allow_html=True: HTML taglerini (görsel linkleri) render et
        st.markdown(AI_Response["output"], unsafe_allow_html=True)

        # Asistan yanıtını session_state'e kaydet
        st.session_state.messages.append({"role":"assistant", "content": AI_Response["output"]})


# =======================================================================================
# SOHBET GEÇMİŞİNİ SIFIRLAMA
# =======================================================================================
# Kullanıcı "Sohbeti Geçmişini Sıfırla" butonuna tıklarsa:
# - Tüm mesajlar temizlenir
# - Toast bildirimi gösterilir
# =======================================================================================

if reset_chat_btn:
    st.session_state.messages = []  # Mesaj listesini boşalt
    st.toast("Sohbet geçmişi sıfırlandı!")  # Kısa bildirim göster
