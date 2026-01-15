# =======================================================================================
# DOSYA: crewai.py
# AÇIKLAMA: CrewAI çerçevesi kullanarak çoklu ajan sistemleri oluşturma örneği.
#           Bu dosya, kişilik testi geliştirmek için üç ajanı bir araya getirir.
#
# KONU: OTONOM AJANLAR - Çoklu Ajan Yaklaşımı (Multi-Agent Approach)
# 
# CrewAI NEDİR?
# ==============
# CrewAI, yapay zeka ajanlarını bir "ekip" olarak organize etmenizi sağlayan
# bir Python çerçevesidir. Her ajan farklı bir role ve uzmanlık alanına sahiptir.
#
# CrewAI'nin Temel Bileşenleri:
# -----------------------------
# 1. AGENT (Ajan):
#    - Belirli bir role sahip yapay zeka varlığı
#    - Kendi hedefleri ve arka hikayesi olan
#    - LLM (Büyük Dil Modeli) ile güçlendirilmiş
#
# 2. TASK (Görev):
#    - Bir ajanın yerine getirmesi gereken iş
#    - Belirli talimatlar ve beklenen çıktılar içerir
#
# 3. CREW (Ekip):
#    - Birden fazla ajanın ve görevin bir araya geldiği yapı
#    - Ajanlar arasındaki iş akışını yönetir
#
# 4. PROCESS (Süreç):
#    - Sequential: Görevler sırayla yürütülür
#    - Hierarchical: Bir yönetici ajan görevleri dağıtır
#
# Bu Dosyadaki Senaryo:
# ----------------------
# Bir kişilik testi geliştirmek için üç farklı uzman ajan kullanılır:
# 1. Kişilik Testleri Uzmanı: Test içeriğini hazırlar
# 2. Yazılım Mühendisi: Streamlit uygulamasını kodlar
# 3. Kişilik Testleri Danışmanı: İnceleme ve öneriler yapar
#
# Ajanlar sıralı (sequential) bir süreçte çalışarak birbirlerinin
# çıktılarını kullanır ve final olarak çalışan bir uygulama üretir.
# =======================================================================================

from crewai import Crew, Process  # CrewAI çerçevesinin temel sınıfları
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini modeli
from langchain_openai import ChatOpenAI  # OpenAI GPT modeli
import crewhelper  # Ajan ve görev tanımlarını içeren yardımcı modül
import os  # İşletim sistemi işlemleri ve ortam değişkenleri

# =======================================================================================
# ORTAM DEĞİŞKENLERİ YAPILANDIRMASI
# =======================================================================================
# CrewAI ve LangChain, API anahtarlarını ortam değişkenlerinden okur.
# Bu değişkenler .env dosyasından veya doğrudan ortamdan alınır.
# =======================================================================================

os.environ["OPENAI_API_KEY"] = os.getenv("openai_apikey")  # OpenAI API anahtarı
os.environ["GOOGLE_API_KEY"] = os.getenv("google_apikey")  # Google Gemini API anahtarı


# =======================================================================================
# DİL MODELLERİNİN TANIMI
# =======================================================================================
# LangChain entegrasyonu sayesinde farklı LLM sağlayıcıları kullanılabilir.
# Her model, ajanlar tarafından farklı görevlerde kullanılabilir.
#
# ChatGoogleGenerativeAI:
# - Google'ın Gemini Pro modelini kullanır
# - Hızlı yanıt süreleri ve iyi genel performans
# - temperature=0: Deterministik çıktı, yaratıcılık düşük
#
# ChatOpenAI:
# - OpenAI'nin GPT-4 modelini kullanır
# - Daha yüksek doğruluk ve karmaşık muhakeme
# - gpt-4-0125-preview: GPT-4 Turbo versiyonu
# =======================================================================================

llm_gemini = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
llm_gpt = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)

# =======================================================================================
# PROJE TALİMATLARI (INSTRUCTIONS)
# =======================================================================================
# Bu talimatlar, tüm ajanların ortak hedefini ve projenin gereksinimlerini tanımlar.
# Her ajan bu talimatlara uygun şekilde çalışır.
#
# Bu senaryoda talep edilen:
# - Big Five, 16 Personalities veya 4 Renk yaklaşımına uygun kişilik testi
# - Kişilik tipleri ve karakter özellikleri
# - Her tip için test soruları
# - Sonuç hesaplama algoritması
# - Kullanıcıya gösterilecek özet metinler
# - Tüm bunları içeren bir Python Streamlit uygulaması
# =======================================================================================

instructions=f"""Profesyonel hayatta kişilerin karakteristik özelliklerini belirlemekte kullanmak üzere bir kişilik testi geliştir.
Bu testi geliştirirken Big Five, 16 Personalities veya 4 Renk yaklaşımı bilinen ve geniş kabul görmüş yaklaşımlara uyumlu olarak hareket et.
Geliştirdiğin kişilik testi, kişilik tiplerini ve bunların her birinin karakter özelliklerini barındırıyor olmalı.
Her bir kişilik tipini ve karakteri test etmek için sorular yazmalısın. 
Bu soruların yanıtına göre nasıl kullanıcıyı bir tiple ve karakter özellikleriyle bağlantılandıracağına dair bir yönteme karar vermelisin. 
Bu testi yapan kişilere göstermek için her bir kişilik tipinin kısa özet metinleri de olmalı. 
Bu kriterlere uygun olarak kişilik testinin içeriklerini hazırladıktan sonra tüm bu içerikleri içerecek şekilde bir Python Streamlit uygulaması yazmalısın. 
Böylece kullanıcılar bu uygulamayı kullanarak kişilik tiplerini öğrenebilirler. 
Derin bir nefes al ve bu görevleri birer birer yerine getir.
"""

# =======================================================================================
# AJANLARIN OLUŞTURULMASI
# =======================================================================================
# crewhelper modülünden ajan fonksiyonları çağrılarak ajanlar oluşturulur.
# Her ajan, belirlenen LLM modelini kullanır.
#
# Ajanların Rolleri:
# ------------------
# 1. test_expert (Kişilik Testleri Uzmanı):
#    - Kişilik testi içeriğini oluşturur
#    - Soruları, kişilik tiplerini ve değerlendirme kriterlerini hazırlar
#
# 2. software_engineer (Yazılım Mühendisi):
#    - Python Streamlit kodunu yazar
#    - Testi çalışır bir web uygulamasına dönüştürür
#
# 3. test_consultant (Kişilik Testleri Danışmanı):
#    - Hazırlanan testi inceler
#    - Hatalar ve iyileştirme önerileri sunar
# =======================================================================================

test_expert = crewhelper.test_expert(llm=llm_gpt)  # Kişilik testleri uzmanı
sotware_engineer = crewhelper.software_engineer(llm=llm_gpt)  # Yazılım mühendisi (typo: software)
test_consultant = crewhelper.test_consultant(llm=llm_gpt)  # Kişilik testleri danışmanı

# =======================================================================================
# GÖREVLERİN OLUŞTURULMASI
# =======================================================================================
# Her görev, belirli bir ajana atanır ve o ajanın yapması gerekeni tanımlar.
# Görevler, instructions parametresiyle ortak proje hedeflerini alır.
#
# Görev Sıralaması:
# -----------------
# 1. test_development_task: Test içeriğini geliştir
# 2. test_review_task: Testi incele ve geri bildirim ver
# 3. code_task: Streamlit uygulamasını kodla
# =======================================================================================

# Kişilik testi geliştirme görevi - Test uzmanına atanır
test_development_task = crewhelper.create_test_task(instructions=instructions, agent=test_expert)

# Python Streamlit kodu yazma görevi - Yazılım mühendisine atanır
code_task = crewhelper.create_code_task(instructions=instructions, agent=sotware_engineer)

# Test inceleme görevi - Danışmana atanır
test_review_task = crewhelper.create_review_task(instructions=instructions, agent=test_consultant)


# =======================================================================================
# CREW (EKİP) OLUŞTURMA
# =======================================================================================
# Crew sınıfı, ajanları ve görevleri bir araya getirir ve yürütme planını belirler.
#
# Parametreler:
# -------------
# agents: Ekipteki tüm ajanların listesi
# tasks: Yürütülecek görevlerin listesi (sıralama önemli!)
# verbose: True ise detaylı log çıktısı verir (debugging için kullanışlı)
# process: Görev yürütme stratejisi
#   - Process.sequential: Görevler sırayla yürütülür (Task 1 → Task 2 → Task 3)
#   - Process.hierarchical: Bir yönetici ajan işleri dağıtır
#
# NOT: tasks listesindeki sıra, görevlerin yürütme sırasını belirler!
# =======================================================================================

crew = Crew(
    agents = [
        test_expert,      # Önce kişilik testi uzmanı
        sotware_engineer, # Sonra yazılım mühendisi
        test_consultant   # Son olarak danışman
        ],
    tasks = [
        test_development_task,  # 1. Görev: Test içeriğini oluştur
        test_review_task,       # 2. Görev: Testi incele
        code_task,              # 3. Görev: Kodu yaz
        ],
    verbose = True,  # Detaylı çıktı - ajanların düşünce süreçlerini gösterir
    process=Process.sequential  # Görevler sırayla yürütülür
)

# =======================================================================================
# CREW'İ ÇALIŞTIRMA
# =======================================================================================
# kickoff() metodu, crew'i başlatır ve tüm görevleri yürütür.
# 
# Yürütme Akışı:
# 1. test_expert, kişilik testi içeriğini oluşturur
# 2. test_consultant, oluşturulan testi inceler ve geri bildirim verir
# 3. software_engineer, geri bildirimleri dikkate alarak Streamlit kodunu yazar
#
# Her ajanın çıktısı, sonraki ajana bağlam olarak iletilir.
# Final çıktısı, son görevin (code_task) sonucudur.
# =======================================================================================

result = crew.kickoff()  # Ekibi başlat ve tüm görevleri yürüt

# =======================================================================================
# SONUÇLARIN GÖRÜNTÜLENMESİ
# =======================================================================================
# Crew'in yürütme sonucu, genellikle son görevin çıktısını içerir.
# Bu senaryoda, oluşturulan Python Streamlit kodu döndürülür.
# =======================================================================================

print("*"*100)  # Görsel ayırıcı
print("İşte Sonuçlar:")
print("*"*100)
print("*"*100)
print(result)  # Final çıktıyı yazdır (genellikle Streamlit kodu)