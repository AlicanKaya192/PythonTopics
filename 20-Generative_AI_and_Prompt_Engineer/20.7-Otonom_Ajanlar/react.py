# =======================================================================================
# DOSYA: react.py
# AÇIKLAMA: LangChain kullanarak ReAct (Reasoning and Acting) ajan örneği.
#           Web araması yapabilen otonom bir ajan oluşturur.
#
# KONU: OTONOM AJANLAR - ReAct Yaklaşımı
# 
# REACT NEDİR?
# ============
# ReAct (Reasoning and Acting), yapay zeka ajanları için bir çerçevedir.
# "Düşün, Hareket Et, Gözlemle" döngüsünü takip eder.
#
# ReAct Döngüsü:
# --------------
# 1. THOUGHT (Düşünce): Ajan mevcut durumu analiz eder ve ne yapacağını düşünür
# 2. ACTION (Eylem): Ajan bir araç kullanarak eylem yapar (örn: web araması)
# 3. OBSERVATION (Gözlem): Eylemin sonucunu gözlemler
# 4. Tekrar 1'e döner veya final yanıtı verir
#
# Örnek ReAct Döngüsü:
# --------------------
# Soru: "Türkiye'nin başkenti neresidir?"
#
# Thought: Bu soruyu yanıtlamak için coğrafi bilgiye ihtiyacım var.
#          Web araması yapmalıyım.
# Action: search("Türkiye başkent")
# Observation: Türkiye'nin başkenti Ankara'dır. Ankara, 1923'te...
# Thought: Yeterli bilgiye sahibim, şimdi yanıt verebilirim.
# Final Answer: Türkiye'nin başkenti Ankara'dır.
#
# NEDEN REACT KULLANILIR?
# =======================
# 1. Şeffaflık: Ajanın düşünce sürecini görebilirsiniz
# 2. Hata Ayıklama: Hangi adımda sorun olduğunu anlayabilirsiniz
# 3. Araç Kullanımı: Ajan harici araçlarla entegre çalışabilir
# 4. Karmaşık Görevler: Çok adımlı problemleri çözebilir
#
# LANGCHAIN ENTEGRASYONU
# ======================
# LangChain, ReAct ajanları oluşturmak için hazır bileşenler sunar:
# - hub.pull(): Önceden tanımlı prompt şablonları
# - create_react_agent(): ReAct ajan oluşturma fonksiyonu
# - AgentExecutor: Ajanı çalıştıran orkestratör
# =======================================================================================

from langchain import hub  # LangChain Hub - paylaşılan prompt şablonları için
from langchain.agents import AgentExecutor, create_react_agent  # Ajan oluşturma araçları
from langchain_community.tools.tavily_search import TavilySearchResults  # Web arama aracı
from langchain_openai import ChatOpenAI  # OpenAI GPT modeli
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini modeli
import os
from dotenv import load_dotenv

# =======================================================================================
# ORTAM DEĞİŞKENLERİ VE API YAPILANDIRMASI
# =======================================================================================
# Farklı API sağlayıcıları için anahtarların yüklenmesi.
# Her API sağlayıcısı kendi ortam değişkenini bekler.
# =======================================================================================

load_dotenv()  # .env dosyasını yükle

# API anahtarlarını yükle
my_key_openai = os.getenv("openai_apikey")  # OpenAI API anahtarı
my_key_google = os.getenv("google_apikey")  # Google Gemini API anahtarı

# Tavily API anahtarını ortam değişkenine ayarla
# Tavily, LangChain ile entegre çalışan bir web arama API'sidir
# Geleneksel web aramalarından daha iyi yapılandırılmış sonuçlar döner
os.environ["TAVILY_API_KEY"] = os.getenv("tavily_apikey")

# =======================================================================================
# DİL MODELLERİNİN TANIMI
# =======================================================================================
# LangChain, farklı LLM sağlayıcılarını aynı arayüzle kullanmamızı sağlar.
# Bu sayede modeli kolayca değiştirebiliriz.
#
# ChatGoogleGenerativeAI:
# - Google'ın Gemini Pro modelini kullanır
# - Gemini, Google'ın en gelişmiş çok modlu AI modelidir
#
# ChatOpenAI:
# - OpenAI'nin GPT-4 modelini kullanır
# - gpt-4-0125-preview: GPT-4 Turbo versiyonu (daha hızlı ve güncel)
# =======================================================================================

# Google Gemini Pro modeli oluştur
llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model="gemini-pro")

# OpenAI GPT-4 Turbo modeli oluştur
llm_gpt = ChatOpenAI(api_key=my_key_openai, model="gpt-4-0125-preview")

# =======================================================================================
# ARAÇLARIN (TOOLS) TANIMLANMASI
# =======================================================================================
# ReAct ajanları, görevleri yerine getirmek için araçlara ihtiyaç duyar.
# Bu araçlar, ajanın "Action" adımında kullandığı işlevlerdir.
#
# TavilySearchResults:
# - Gelişmiş web arama aracı
# - Yapılandırılmış arama sonuçları döner
# - max_results: Döndürülecek maksimum sonuç sayısı
#
# Tavily'nin Avantajları:
# - Google/Bing'e göre daha LLM-dostu çıktı
# - Kaynak URL'leri ve snippet'ler içerir
# - Daha az "gürültü" içeren sonuçlar
# =======================================================================================

tools = [TavilySearchResults(max_results=1)]  # Max 1 arama sonucu döndür

# =======================================================================================
# REACT PROMPT ŞABLONU
# =======================================================================================
# LangChain Hub, topluluk tarafından paylaşılan prompt şablonlarını sunar.
# hub.pull() ile bu şablonları çekebilirsiniz.
#
# "hwchase17/react": Harrison Chase (LangChain kurucusu) tarafından
# tanımlanmış standart ReAct promptu.
#
# ReAct Prompt Yapısı:
# --------------------
# Answer the following questions as best you can. You have access to the following tools:
# {tools}
# 
# Use the following format:
# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question
#
# NOT: Türkçe yanıtlar için özelleştirilmiş "emreyz/react-turkce" promptu da kullanılabilir
# =======================================================================================

# İngilizce standart ReAct promptu
prompt = hub.pull("hwchase17/react")

# Alternatif: Türkçe özelleştirilmiş prompt
#prompt = hub.pull("emreyz/react-turkce")

# =======================================================================================
# AJAN OLUŞTURMA
# =======================================================================================
# ReAct ajanı, LLM ve araçları birleştirerek oluşturulur.
#
# create_react_agent():
# - llm: Kullanılacak dil modeli
# - tools: Ajanın kullanabileceği araçlar listesi
# - prompt: ReAct formatındaki prompt şablonu
##
# AgentExecutor:
# - Ajanı çalıştıran ve yöneten sınıf
# - verbose=True: Düşünce sürecini konsola yazdırır (debugging için)
# - handle_parsing_errors: Parse hatalarında varsayılan davranış
# =======================================================================================

# Kullanılacak LLM'i seç
# Gemini veya GPT-4 kullanılabilir
llm = llm_gpt  # GPT-4 Turbo kullanıyoruz

# ReAct ajanı oluştur
# Agent, LLM'in "beynini" ve araçları birleştirir
agent = create_react_agent(llm, tools, prompt)

# AgentExecutor oluştur - ajanı çalıştıran orkestratör
# verbose=True: Tüm düşünce sürecini ve eylemleri göster
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# =======================================================================================
# AJANI ÇALIŞTIRMA
# =======================================================================================
# invoke() metodu, ajana bir soru/görev gönderir ve sonucu alır.
#
# Çalışma Akışı:
# 1. Soru ajana iletilir
# 2. Ajan ReAct döngüsünü başlatır
# 3. Thought/Action/Observation adımları tekrarlanır
# 4. Final yanıt oluşturulur
#
# handle_parsing_errors=True:
# - LLM çıktısı beklenmedik formatta olursa hata yerine düzeltme dener
# - Daha sağlam bir çalışma sağlar
# =======================================================================================

# Örnek soru - Türkçe yanıt isteniyor
# Ajan web araması yaparak yanıt bulacak
result = agent_executor.invoke(
    {"input": "Türkiye'de bir sonraki yerel seçimler hangi tarihte gerçekleştirilecek? Cevabı bulduktan sonra yanıtını Türkçe yaz."}, 
    handle_parsing_errors=True
)

# =======================================================================================
# SONUÇLARIN GÖRÜNTÜLENMESİ
# =======================================================================================
# invoke() bir dict döndürür:
# - result['input']: Orijinal soru
# - result['output']: Ajanın final yanıtı
# =======================================================================================

print("*"*100)  # Görsel ayırıcı
print(f"Sorunuz Şuydu: {result['input']}")  # Sorulan soru
print("*"*100)
print(f"Yanıt şu: {result['output']}")  # Ajanın yanıtı