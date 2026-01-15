# =======================================================================================
# DOSYA: customtools.py
# AÇIKLAMA: LangChain ajan sistemleri için özel araç (tool) tanımları.
#           DALL-E 3 ve Stable Diffusion XL ile görsel üretimi ve web scraping içerir.
#
# KONU: OTONOM AJANLAR - ReAct Yaklaşımı ve Tool Kullanımı
# 
# LANGCHAIN TOOL SİSTEMİ
# ======================
# LangChain'de "Tool" (Araç), bir ajanın kullanabileceği işlev birimini temsil eder.
# Her araç şunları içerir:
# - name: Aracın benzersiz adı (ajan bu isimle çağırır)
# - func: Çalıştırılacak Python fonksiyonu
# - description: Aracın ne yaptığını açıklayan metin (LLM bu açıklamaya göre karar verir)
#
# Ajan, kullanıcı isteğine göre hangi aracı kullanacağına karar verir.
# Bu karar, her aracın "description" alanına bakarak yapılır.
#
# GÖRSEL ÜRETİM MODELLERİ
# =======================
# 1. DALL-E 3 (OpenAI):
#    - OpenAI'nin en gelişmiş görsel üretim modeli
#    - Yüksek kaliteli, detaylı görseller üretir
#    - Prompt takip yeteneği çok güçlüdür
#
# 2. Stable Diffusion XL (Stability AI):
#    - Açık kaynaklı görsel üretim modeli
#    - API üzerinden erişilebilir
#    - Özelleştirilebilir parametreler sunar
#
# WEB SCRAPING
# ============
# BeautifulSoup kütüphanesi ile web sayfalarından içerik çıkarma işlemi.
# Ajanlar bu araçla web sayfalarını okuyabilir ve analiz edebilir.
# =======================================================================================

from langchain.agents import Tool  # LangChain Tool sınıfı - araç tanımlamak için
from openai import OpenAI  # OpenAI API erişimi - DALL-E 3 için
from bs4 import BeautifulSoup  # HTML parsing kütüphanesi - web scraping için
from io import BytesIO  # Binary veri akışı - görsel verileri işlemek için
import base64  # Base64 encoding/decoding - Stable Diffusion API yanıtı için
import requests  # HTTP istekleri - API çağrıları ve web sayfası indirmek için
from datetime import datetime  # Tarih/saat işlemleri - dosya adlandırma için
import os  # İşletim sistemi işlemleri - dosya/klasör yönetimi
from dotenv import load_dotenv  # Ortam değişkenleri yükleme

# =======================================================================================
# ORTAM DEĞİŞKENLERİ VE API YAPILANDIRMASI
# =======================================================================================
# API anahtarları güvenlik nedeniyle .env dosyasında saklanır.
# Bu dosya versiyon kontrolüne dahil edilmemelidir (.gitignore'a eklenmeli).
# =======================================================================================

load_dotenv()  # .env dosyasını ortam değişkenlerine yükle

# API anahtarlarını ortam değişkenlerinden al
my_key_openai = os.getenv("openai_apikey")  # OpenAI API anahtarı (DALL-E 3 için)
my_key_stabilityai = os.getenv("stabilityai_apikey")  # Stability AI API anahtarı (SDXL için)

# OpenAI client'ı oluştur - DALL-E 3 API çağrıları için kullanılacak
client = OpenAI(
    api_key=my_key_openai
)

# =======================================================================================
# GÖRSEL OLUŞTURMA ARAÇLARI NOTU
# =======================================================================================
# Bu araçların oluşturduğu görseller:
# - "../assets/19.7-Materyaller/img/" klasörüne kaydedilir
# - Benzersiz zaman damgalı dosya adları alır
# - PNG formatında saklanır
#
# Kullanılabilecek modeller:
# - SDXL (Stable Diffusion XL): Stability AI'nin modeli
# - DALLE3: OpenAI'nin modeli
# - Bsoup: BeautifulSoup ile web scraping
#
# Method->Tool: Fonksiyonlar LangChain Tool nesnelerine dönüştürülür
# =======================================================================================


def generate_image_with_dalle(prompt):
    """
    DALL-E 3 kullanarak metin promptundan görsel üretir.
    
    DALL-E 3 Özellikleri:
    ---------------------
    - OpenAI'nin en gelişmiş görsel üretim modeli
    - Metin talimatlarını çok iyi anlar ve takip eder
    - 1024x1024, 1024x1792, 1792x1024 boyutlarını destekler
    - HD kalite seçeneği mevcut
    - Her istekte tek veya çoklu görsel üretilebilir
    
    API Parametreleri:
    ------------------
    - model: Kullanılacak model ("dall-e-3" veya "dall-e-2")
    - size: Görsel boyutu (1024x1024 standart kare format)
    - quality: "standard" veya "hd" (yüksek detay)
    - n: Üretilecek görsel sayısı (DALL-E 3 için max 1)
    - response_format: "url" veya "b64_json"
    - prompt: Görsel açıklama metni
    
    Parametreler:
    -------------
    prompt (str): Üretilecek görseli tanımlayan metin
    
    Returns:
        str: HTML formatında görsel linki (ajan yanıtına eklenir)
    """
    # -------------------------------------------------------------------------
    # DALL-E 3 API ÇAĞRISI
    # -------------------------------------------------------------------------
    # client.images.generate(): OpenAI'nin görsel üretim endpoint'i
    # Yanıt olarak URL veya base64 encoded görsel döner
    # -------------------------------------------------------------------------
    
    AI_Response = client.images.generate(
        model = "dall-e-3",  # Kullanılacak model
        size = "1024x1024",  # Kare format, yüksek çözünürlük
        quality = "hd",  # Yüksek detay kalitesi (daha yavaş ama daha iyi)
        n = 1,  # Tek görsel üret (DALL-E 3 limiti)
        response_format = "url",  # URL olarak döndür (base64 yerine)
        prompt = prompt  # Kullanıcının görsel açıklaması
    )
    
    # API yanıtından görsel URL'sini al
    # data[0]: İlk (ve tek) görsel
    # .url: Geçici görsel URL'si (1 saat geçerli)
    image_url = AI_Response.data[0].url

    # -------------------------------------------------------------------------
    # GÖRSELİ İNDİR VE KAYDET
    # -------------------------------------------------------------------------
    # DALL-E 3 geçici URL'ler döndürür (1 saat sonra silinir)
    # Bu nedenle görseli hemen indirip yerel olarak kaydetmeliyiz
    # -------------------------------------------------------------------------
    
    # HTTP GET isteği ile görseli indir
    response = requests.get(image_url)
    # Binary veriyi BytesIO nesnesine yükle
    image_bytes = BytesIO(response.content)

    # Benzersiz dosya adı oluştur (tarih-saat damgası ile)
    # Format: YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Görselin kaydedileceği yol - assets klasörüne kaydet
    filepath = f"../assets/19.7-Materyaller/img/generated_image_{timestamp}.png"

    # img klasörü yoksa oluştur
    # os.path.dirname(): Dosya yolundan dizin yolunu al
    output_dir = os.path.dirname(filepath)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Görseli dosyaya yaz
    # "wb": Write Binary modu (görsel binary veridir)
    with open(filepath, "wb") as file:
        file.write(image_bytes.getbuffer())

    # HTML link formatında döndür
    # Ajan bu linki kullanıcıya gösterir
    return f'<a href="{filepath}">Resminiz Burada</a>'



def generate_with_SD(prompt):
    """
    Stable Diffusion XL kullanarak metin promptundan görsel üretir.
    
    Stable Diffusion XL (SDXL) Özellikleri:
    ---------------------------------------
    - Stability AI tarafından geliştirilen açık kaynaklı model
    - 1024x1024 piksel yüksek çözünürlüklü çıktı
    - Negatif prompt desteği (istenmeyen öğeleri filtreleme)
    - Steps, CFG Scale gibi ayarlanabilir parametreler
    - Seed ile tekrarlanabilir sonuçlar
    
    API Parametreleri Açıklaması:
    -----------------------------
    - steps: Diffusion adım sayısı (yüksek = daha kaliteli ama yavaş)
    - width/height: Görsel boyutları (SDXL için 1024x1024 optimal)
    - seed: Rastgelelik tohumu (0 = her seferinde farklı)
    - cfg_scale: CFG (Classifier-Free Guidance) - prompt uyumu kontrolü
      * Düşük değer (1-5): Daha yaratıcı sonuçlar
      * Yüksek değer (10-20): Prompta daha sadık sonuçlar
    - samples: Üretilecek görsel sayısı
    - text_prompts: Pozitif ve negatif promptlar
      * weight > 0: İstenen özellikler
      * weight < 0: İstenmeyen özellikler
    
    Parametreler:
    -------------
    prompt (str): Üretilecek görseli tanımlayan metin
    
    Returns:
        str: HTML formatında görsel linki
    """
    # -------------------------------------------------------------------------
    # STABILITY AI API YAPILANDIRMASI
    # -------------------------------------------------------------------------
    # Stability AI, REST API üzerinden SDXL modeline erişim sağlar.
    # API dokümantasyonu: https://platform.stability.ai/docs/api-reference
    # -------------------------------------------------------------------------
    
    # API endpoint URL'si - SDXL 1.0 text-to-image
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    # HTTP başlıkları - API anahtarı ve içerik tipi
    headers = {
        "Accept": "application/json",  # JSON formatında yanıt iste
        "Content-Type": "application/json",  # JSON formatında istek gönder
        "Authorization": f"Bearer {my_key_stabilityai}",  # API anahtarı (Bearer token)
    }

    # İstek gövdesi - görsel üretim parametreleri
    body = {
        "steps": 40,  # Diffusion adım sayısı (20-50 arası önerilir)
        "width": 1024,  # Görsel genişliği (SDXL optimum)
        "height": 1024,  # Görsel yüksekliği (SDXL optimum)
        "seed": 0,  # Rastgelelik tohumu (0 = random, belirli sayı = tekrarlanabilir)
        "cfg_scale": 5,  # CFG ölçeği - prompta sadakat (5-10 önerilir)
        "samples": 1,  # Üretilecek görsel sayısı
        "text_prompts": [
            {
                # POZİTİF PROMPT: İstenen özellikler
                "text": prompt,  # Kullanıcının açıklaması
                "weight": 1  # Pozitif ağırlık
            },
            {
                # NEGATİF PROMPT: İstenmeyen özellikler
                # Bu özellikler görsellerden çıkarılır
                "text": "blurry, bad",  # Bulanık ve kötü kalite istemiyoruz
                "weight": -1  # Negatif ağırlık
            }
        ],
    }

    # -------------------------------------------------------------------------
    # API ÇAĞRISI VE YANIT İŞLEME
    # -------------------------------------------------------------------------
    # POST isteği gönder ve JSON yanıtını al
    # -------------------------------------------------------------------------
    
    response = requests.post(
        url,
        headers=headers,
        json=body  # Python dict otomatik olarak JSON'a dönüştürülür
    )

    # JSON yanıtını Python dict'e dönüştür
    data = response.json()

    # -------------------------------------------------------------------------
    # GÖRSELLERİ İŞLE VE KAYDET
    # -------------------------------------------------------------------------
    # Stability AI, görselleri base64 encoded string olarak döndürür.
    # Her görsel için decode edip yerel dosyaya kaydediyoruz.
    # -------------------------------------------------------------------------
    
    # artifacts: Üretilen görsellerin listesi
    for image in data["artifacts"]:
        # Base64 string'i binary veriye dönüştür
        image_bytes = base64.b64decode(image["base64"])

        # Benzersiz dosya adı oluştur (tarih-saat damgası ile)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Görselin kaydedileceği yol - assets klasörüne kaydet
        filepath = f"../assets/19.7-Materyaller/img/generated_image_{timestamp}.png"

        # Klasör yoksa oluştur
        output_dir = os.path.dirname(filepath)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Görseli dosyaya yaz
        with open(filepath, "wb") as file:
            file.write(image_bytes)

    # HTML link formatında döndür
    return f'<a href="{filepath}">Resminiz Burada</a>'


def get_tool(selected_image_generator):
    """
    Seçilen görsel üretim modeline göre uygun LangChain Tool nesnesini döndürür.
    
    LangChain Tool Yapısı:
    ----------------------
    Tool, bir ajanın kullanabileceği işlevi temsil eder:
    - name: Aracın benzersiz adı (ajan bu isimle çağırır)
    - func: Çağrılacak Python fonksiyonu
    - description: Aracın ne yaptığını açıklar (ÇOOK ÖNEMLİ!)
    
    Description Önemi:
    ------------------
    LLM, hangi aracı kullanacağına SADECE description okuyarak karar verir.
    Bu nedenle description:
    - Aracın ne yaptığını net açıklamalı
    - Ne zaman kullanılacağını belirtmeli
    - Girdinin ne olduğunu söylemeli
    - Çıktının ne olduğunu söylemeli
    
    Parametreler:
    -------------
    selected_image_generator (str): Seçilen model ("DALL-E 3" veya "Stable Diffusion XL")
    
    Returns:
        Tool: Yapılandırılmış LangChain Tool nesnesi
    """
    if selected_image_generator == "DALL-E 3":
        return Tool (
            name="Generate Image",  # Aracın adı
            func= generate_image_with_dalle,  # Çağrılacak fonksiyon
            description="""Useful for when you need to generate an image based on given textual instructions or prompts. 
            It returns the filepath where the image saved. This filepath must be given back to the user.
            The filepath is given between HTML tags for turning the address of the image into a link.
            The user must be provided with this HTML style statement that includes the filepath for the saved image.
            """  # Aracın ne yaptığını anlatan detaylı açıklama
        )

    elif selected_image_generator == "Stable Diffusion XL":
            return Tool (
            name="Generate Image",
            func= generate_with_SD,
            description="""Useful for when you need to generate an image based on given textual instructions or prompts. 
            It returns the filepath where the image saved. This filepath must be given back to the user.
            The filepath is given between HTML tags for turning the address of the image into a link.
            The user must be provided with this HTML style statement that includes the filepath for the saved image.
            """
        )


def analyze_webpage(target_url):
    """
    Verilen URL'deki web sayfasının metin içeriğini çıkarır.
    
    Web Scraping Nedir?
    -------------------
    Web scraping, web sitelerinden otomatik olarak veri toplama işlemidir.
    Bu fonksiyon BeautifulSoup kütüphanesini kullanarak:
    1. Sayfayı indirir
    2. HTML'i parse eder
    3. Sadece metin içeriğini çıkarır (etiketleri atar)
    4. Çok uzun içerikleri kırpar
    
    BeautifulSoup:
    --------------
    Python için popüler HTML/XML parsing kütüphanesi.
    HTML yapısını ağaç olarak temsil eder ve gezinmeyi kolaylaştırır.
    
    Parametreler:
    -------------
    target_url (str): Analiz edilecek web sayfasının URL'si
    
    Returns:
        str: Sayfanın metin içeriği (max 4000 karakter)
    
    Sınırlamalar:
    -------------
    - JavaScript ile yüklenen içerikler alınamaz
    - Giriş gerektiren sayfalar çalışmaz
    - Çok büyük sayfalar 4000 karaktere kırpılır (LLM token limiti için)
    """
    # HTTP GET isteği ile sayfayı indir
    response = requests.get(target_url)
    # Yanıt metnini al (HTML içeriği)
    html_content = response.text

    # BeautifulSoup ile HTML'i parse et
    # "html.parser": Python'un dahili HTML parser'ı
    # Alternatifler: "lxml" (daha hızlı), "html5lib" (daha toleranslı)
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Tüm metin içeriğini çıkar
    # get_text(): Tüm HTML etiketlerini kaldırıp sadece metni döndürür
    stripped_content = soup.get_text()

    # İçerik çok uzunsa kırp
    # LLM'ler genellikle sınırlı bağlam penceresine sahiptir
    # 4000 karakter, çoğu model için güvenli bir limit
    if len(stripped_content) > 4000:
        stripped_content = stripped_content[:4000]

    return stripped_content


def get_web_tool():
    """
    Web scraping aracını LangChain Tool olarak döndürür.
    
    Bu araç, ReAct ajanının web sayfalarını okumasını sağlar.
    Örnek kullanım senaryoları:
    - Web sayfasındaki bilgileri analiz etme
    - Haber içeriklerini özetleme
    - Belirli bilgileri web'den çıkarma
    
    Returns:
        Tool: Yapılandırılmış web scraping aracı
    """
    return Tool(
        name="Get Webpage",  # Aracın adı - ajan bu isimle çağırır
        func=analyze_webpage,  # Çağrılacak fonksiyon
        description="Useful for when you need to get the http from a specific webpage"  # Açıklama
    )