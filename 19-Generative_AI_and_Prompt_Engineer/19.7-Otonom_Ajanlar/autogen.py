# =======================================================================================
# DOSYA: autogen.py
# AÇIKLAMA: Microsoft AutoGen Studio için yapılandırma ve başlatma komutları
#
# KONU: OTONOM AJANLAR - Çoklu Ajan Sistemleri (Multi-Agent Systems)
# 
# Bu dosya, Microsoft'un AutoGen kütüphanesi ile çalışmak için gerekli
# terminal komutlarını ve yapılandırma talimatlarını içerir.
#
# AUTOGEN NEDİR?
# ==============
# AutoGen, Microsoft tarafından geliştirilen açık kaynaklı bir çerçevedir (framework).
# LLM (Large Language Model) tabanlı çoklu ajan sistemleri oluşturmak için kullanılır.
#
# AutoGen'in Temel Özellikleri:
# -----------------------------
# 1. ÇOKLU AJAN KONUŞMALARI:
#    - Birden fazla ajan birbirleriyle konuşabilir
#    - Her ajanın farklı rolleri ve yetenekleri olabilir
#    - Ajanlar birlikte karmaşık görevleri çözebilir
#
# 2. AJAN TİPLERİ:
#    - AssistantAgent: LLM tabanlı asistan ajan
#    - UserProxyAgent: Kullanıcıyı temsil eden ajan (kod çalıştırabilir)
#    - GroupChatManager: Çoklu ajan sohbetlerini yöneten ajan
#
# 3. KOD ÇALIŞTIRMA:
#    - Ajanlar Python kodu yazabilir ve çalıştırabilir
#    - Sandbox ortamında güvenli kod yürütme
#    - Hata ayıklama ve düzeltme yapabilir
#
# 4. İNSAN-DÖNGÜDE (HUMAN-IN-THE-LOOP):
#    - Kritik kararlarda insan onayı alınabilir
#    - İnsan müdahalesi ile yönlendirme yapılabilir
#
# AUTOGEN STUDIO NEDİR?
# =====================
# AutoGen Studio, AutoGen için görsel bir kullanıcı arayüzüdür (Web UI).
# Kod yazmadan:
# - Ajan oluşturabilirsiniz
# - Ajan yeteneklerini tanımlayabilirsiniz
# - Çoklu ajan senaryoları tasarlayabilirsiniz
# - Konuşmaları görselleştirebilirsiniz
#
# Kurulum:
# --------
# pip install autogenstudio
#
# Kullanım Senaryoları:
# ---------------------
# 1. Kod Geliştirme: Birden fazla ajan birlikte kod yazabilir
# 2. Araştırma: Araştırma asistanları veri toplayıp analiz edebilir
# 3. Problem Çözme: Farklı uzmanlık alanlarına sahip ajanlar birlikte çalışabilir
#
# =======================================================================================

# =======================================================================================
# AUTOGEN STUDIO BAŞLATMA KOMUTU
# =======================================================================================
# Bu komut, AutoGen Studio web arayüzünü başlatır.
# 
# Parametreler:
# - port 8081: Web arayüzünün çalışacağı port numarası
#   (Varsayılan olarak 8080'i kullanır, 8081 çakışmaları önlemek için)
#
# Terminalde çalıştırılacak komut:
# >>> autogenstudio ui --port 8081
#
# Başlatıldıktan sonra tarayıcınızda http://localhost:8081 adresine gidin
# =======================================================================================

#autogenstudio ui --port 8081

# =======================================================================================
# OPENAI API ANAHTARI AYARLAMA
# =======================================================================================
# AutoGen, OpenAI modellerini kullanmak için bir API anahtarına ihtiyaç duyar.
# Bu ortam değişkeni, terminalde AutoGen Studio başlatmadan önce ayarlanmalıdır.
#
# Windows (PowerShell) için:
# >>> $env:OPENAI_API_KEY="sk-your-api-key-here"
#
# Windows (CMD) için:
# >>> set OPENAI_API_KEY=sk-your-api-key-here
#
# Linux/MacOS için:
# >>> export OPENAI_API_KEY=sk-your-api-key-here
#
# GÜVENLİK NOTU:
# API anahtarlarınızı asla kodunuzda veya versiyon kontrolünde saklamayın!
# Bunun yerine .env dosyası veya ortam değişkenleri kullanın.
# =======================================================================================

#set OPENAI_API_KEY=

# =======================================================================================
# AUTOGEN TEMEL KULLANIM ÖRNEĞİ (Referans)
# =======================================================================================
# Aşağıda, AutoGen'in kod ile nasıl kullanılacağına dair bir örnek verilmiştir.
# Bu kod çalıştırılmak üzere değil, referans amaçlıdır.
#
# from autogen import AssistantAgent, UserProxyAgent
#
# # LLM yapılandırması
# llm_config = {
#     "model": "gpt-4",
#     "api_key": os.getenv("OPENAI_API_KEY")
# }
#
# # Asistan ajan oluştur
# assistant = AssistantAgent(
#     name="asistan",
#     llm_config=llm_config,
#     system_message="Sen yardımcı bir asistansın."
# )
#
# # Kullanıcı proxy ajan oluştur (kod çalıştırabilir)
# user_proxy = UserProxyAgent(
#     name="kullanici",
#     human_input_mode="TERMINATE",  # Sadece sonlandırmak için insan girişi al
#     code_execution_config={"work_dir": "coding"}  # Kod çalıştırma dizini
# )
#
# # Ajanları konuştur
# user_proxy.initiate_chat(
#     assistant,
#     message="Python ile Fibonacci sayılarını hesaplayan bir fonksiyon yaz."
# )
# =======================================================================================