# =====================================================================================
# VoiceDraw - Görsel Üretim Modülü (Painter)
# =====================================================================================
# Bu modül, metin tabanlı görsel üretimi için DALL-E 3 ve Gemini Vision API'lerini
# kullanır. İki temel kullanım senaryosu desteklenir:
#
# 1. Sıfırdan Görsel Üretimi (DALL-E 3):
#    - Kullanıcının metin prompt'u doğrudan DALL-E 3'e gönderilir
#    - 1024x1024 boyutunda HD kalitede görsel üretilir
#
# 2. İteratif Görsel Düzenleme (Gemini + DALL-E):
#    - Mevcut bir görsel Gemini Vision ile analiz edilir
#    - Kullanıcının değişiklik talebi ile birleştirilir
#    - Yeni prompt DALL-E 3'e gönderilerek güncellenmiş görsel üretilir
#
# Kullanılan API'ler:
# - OpenAI DALL-E 3: Metin-görsel üretimi (Text-to-Image generation)
# - Google Gemini Vision: Çoklu-modal görsel analizi (Multimodal understanding)
#
# Çevre Değişkenleri:
# - openai_apikey: OpenAI API anahtarı
# - google_apikey: Google AI API anahtarı
# =====================================================================================

# ===================
# KÜTÜPHANE İMPORTLARI
# ===================

# Google Generative AI SDK - Gemini Vision modeli için
import google.generativeai as genai

# PIL (Pillow) - Görsel işleme kütüphanesi
# Görselleri yüklemek ve Gemini'ye göndermek için kullanılır
import PIL.Image

# HTTP istekleri için - DALL-E'nin ürettiği görseli URL'den indirmek için
import requests

# Çevre değişkenlerine erişim için
import os

# .env dosyasından API anahtarlarını yüklemek için
from dotenv import load_dotenv

# OpenAI Python SDK - DALL-E 3 API için
from openai import OpenAI

# BytesIO - Görsel verisini bellek içinde işlemek için
# URL'den indirilen görsel verisini dosyaya yazmadan önce buffer olarak kullanılır
from io import BytesIO

# Dosya adlarına zaman damgası eklemek için
from datetime import datetime

# =====================================================================================
# ÇEVRE DEĞİŞKENLERİNİ YÜKLE
# =====================================================================================
# load_dotenv() fonksiyonu, proje kök dizinindeki .env dosyasından
# API anahtarları gibi hassas bilgileri yükler.
# Bu yöntem, anahtarları kod içinde sabit kodlamaktan daha güvenlidir.
# =====================================================================================

load_dotenv()

# =====================================================================================
# OPENAI API YAPILANDIRMASI
# =====================================================================================
# OpenAI client nesnesi, DALL-E 3 API'sine erişim sağlar.
# API anahtarı çevre değişkeninden alınır (openai_apikey).
# =====================================================================================

my_key_openai = os.getenv("openai_apikey")  # OpenAI API anahtarını çevre değişkeninden al

# OpenAI istemci nesnesi oluştur
client = OpenAI(
    api_key=my_key_openai  # API anahtarını ayarla
)


# =====================================================================================
# DALL-E 3 İLE GÖRSEL ÜRETME FONKSİYONU
# =====================================================================================

def generate_image_with_dalle(prompt):
    """
    DALL-E 3 kullanarak metin prompt'undan görsel üretir.
    
    Bu fonksiyon şu adımları gerçekleştirir:
    1. Prompt'u DALL-E 3 API'sine gönderir
    2. Üretilen görselin URL'sini alır
    3. URL'den görseli indirir
    4. Görseli benzersiz bir dosya adıyla kaydeder
    
    DALL-E 3 Özellikleri:
    - Yüksek kaliteli, fotorealistik görseller üretir
    - 1024x1024, 1024x1792 veya 1792x1024 boyutlarını destekler
    - "hd" kalitesi daha detaylı ve tutarlı görseller üretir
    - Prompt'u otomatik olarak iyileştirir (prompt engineering)
    
    Args:
        prompt (str): Görsel üretimi için metin açıklaması
        
    Returns:
        str: Kaydedilen görsel dosyasının yolu
    """
    
    # ==========================================================================
    # DALL-E 3 API ÇAĞRISI
    # ==========================================================================
    # images.generate() metodu görsel üretim isteği gönderir
    # 
    # Parametreler:
    # - model: Kullanılacak model (dall-e-2 veya dall-e-3)
    # - size: Görsel boyutu (1024x1024 kare format)
    # - quality: Kalite seviyesi ("standard" veya "hd")
    # - n: Üretilecek görsel sayısı (DALL-E 3'te maksimum 1)
    # - response_format: Yanıt formatı ("url" veya "b64_json")
    # - prompt: Görsel açıklaması
    # ==========================================================================
    
    AI_Response = client.images.generate(
        model="dall-e-3",  # En gelişmiş DALL-E modeli
        size="1024x1024",  # Kare format - 1 megapiksel
        quality="hd",  # Yüksek detay kalitesi
        n=1,  # Tek görsel üret (DALL-E 3 limiti)
        response_format="url",  # Görsel URL olarak dönsün (indirmek için)
        prompt=prompt  # Kullanıcının metin prompt'u
    )
    
    # Üretilen görselin URL'sini al
    # data[0]: İlk (ve tek) görsel
    # url: Görselin erişim URL'si (geçici, birkaç saat geçerli)
    image_url = AI_Response.data[0].url

    # ==========================================================================
    # GÖRSELİ URL'DEN İNDİR
    # ==========================================================================
    # OpenAI'nin döndürdüğü URL geçicii olduğundan, görseli hemen indiriyoruz.
    # requests.get() ile HTTP GET isteği gönderilir.
    # BytesIO ile veriyi bellek içinde tutuyoruz.
    # ==========================================================================
    
    response = requests.get(image_url)  # HTTP GET isteği
    image_bytes = BytesIO(response.content)  # Yanıt içeriğini buffer'a al

    # ==========================================================================
    # BENZERSİZ DOSYA ADI OLUŞTUR
    # ==========================================================================
    # Her görsel için benzersiz bir dosya adı oluşturmak adına
    # zaman damgası (timestamp) kullanıyoruz.
    # Format: generated_image_YYYYMMDD_HHMMSS.png
    # ==========================================================================
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Zaman damgası
    filename = f"./img/generated_image_{timestamp}.png"  # Dosya yolu

    # ==========================================================================
    # GÖRSELİ DOSYAYA KAYDET
    # ==========================================================================
    # Önce img klasörünün var olduğundan emin oluyoruz (yoksa oluştur).
    # Sonra binary yazma modunda ("wb") dosyayı kaydediyoruz.
    # ==========================================================================
    
    if not os.path.exists("./img"):
        os.makedirs("./img")  # img klasörü yoksa oluştur
    
    with open(filename, "wb") as file:
        file.write(image_bytes.getbuffer())  # Buffer'daki veriyi dosyaya yaz

    return filename  # Dosya yolunu döndür


# =====================================================================================
# GOOGLE GEMINI API YAPILANDIRMASI
# =====================================================================================
# Gemini, Google'ın çoklu-modal (multimodal) yapay zeka modelidir.
# Hem metin hem de görsel girdi işleyebilir.
# Bu projede görsel analizi ve prompt iyileştirme için kullanılır.
# =====================================================================================

my_key_google = os.getenv("google_apikey")  # Google API anahtarını çevre değişkeninden al

# Gemini API'yi yapılandır
genai.configure(
    api_key=my_key_google  # API anahtarını ayarla
)


# =====================================================================================
# GEMİNİ VİSİON İLE GÖRSEL ANALİZİ FONKSİYONU
# =====================================================================================

def gemini_vision_with_local_file(image_path, prompt):
    """
    Gemini Vision kullanarak yerel bir görseli analiz eder ve 
    DALL-E için optimize edilmiş bir prompt oluşturur.
    
    Bu fonksiyon, iteratif görsel düzenleme için kritik öneme sahiptir:
    1. Mevcut görseli yükler ve Gemini'ye gönderir
    2. Gemini görseli ayrıntılı olarak tanımlar
    3. Kullanıcının değişiklik talebini bu tanıma ekler
    4. DALL-E için optimize edilmiş yeni bir prompt döndürür
    
    Gemini Vision Özellikleri:
    - Görselleri detaylı şekilde anlayabilir ve tanımlayabilir
    - Metin ve görsel girdiyi birlikte işleyebilir (multimodal)
    - Bağlam farkındalığı ile akıllı yanıtlar üretir
    
    Args:
        image_path (str): Analiz edilecek görselin dosya yolu
        prompt (str): Kullanıcının değişiklik talebi
        
    Returns:
        str: DALL-E için optimize edilmiş prompt metni
    """
    
    # ==========================================================================
    # ÇOKLU-MODAL PROMPT OLUŞTUR
    # ==========================================================================
    # Bu prompt, Gemini'ye görseli nasıl analiz edeceğini ve yanıtı
    # nasıl formatlaması gerektiğini açıklar.
    #
    # Prompt stratejisi:
    # 1. Görseli ayrıntılı olarak betimle
    # 2. Betimlemeyi DALL-E için uygun formata dönüştür
    # 3. Kullanıcının ek yönergesini dahil et
    # ==========================================================================
    
    multimodality_prompt = f"""Bu gönderdiğim resmi, bazı ek yönergelerle birlikte yeniden oluşturmanı istiyorum.
    Bunun için ilk olarak resmi son derece ayrıntılı biçimde betimle. Daha sonra sonucunda bana vereceğin metni, bir yapay zeka
    modelini kullanarak görsel oluşturmakta kullanacağım. O yüzden yanıtına son halini verirken bunun resim üretmekte kullanılacak bir
    girdi yani prompt olduğunu dikkate al. İşte ek yönerge şöyle: {prompt}
    """

    # ==========================================================================
    # GEMİNİ VİSİON MODELİNİ YÜKLE
    # ==========================================================================
    # gemini-pro-vision modeli, metin ve görsel girdiyi birlikte işleyebilir.
    # Bu model, görsel anlama ve tanımlama görevleri için optimize edilmiştir.
    # ==========================================================================
    
    client = genai.GenerativeModel(model_name="gemini-pro-vision")

    # ==========================================================================
    # GÖRSELİ YÜKLE
    # ==========================================================================
    # PIL.Image.open() ile yerel görsel dosyasını yükleyip
    # Gemini API'sine gönderilmeye hazır hale getiriyoruz.
    # ==========================================================================
    
    source_image = PIL.Image.open(image_path)  # Görseli aç

    # ==========================================================================
    # GEMİNİ API ÇAĞRISI (ÇOKLU-MODAL)
    # ==========================================================================
    # generate_content() metodu, hem metin hem de görsel girdi alabilir.
    # Girdi bir liste olarak verilir: [metin_prompt, görsel]
    # ==========================================================================
    
    AI_Response = client.generate_content(
        [
            multimodality_prompt,  # Metin talimatları
            source_image  # Görsel girdi
        ]
    )

    # ==========================================================================
    # YANITI ÇÖZÜMLE
    # ==========================================================================
    # resolve() metodu, streaming yanıtları bekler ve tamamlandığından emin olur.
    # Bu, özellikle uzun yanıtlar için önemlidir.
    # ==========================================================================
    
    AI_Response.resolve()  # Yanıtın tamamlanmasını bekle

    return AI_Response.text  # Üretilen prompt metnini döndür


# =====================================================================================
# BİRLEŞİK GÖRSEL ÜRETME FONKSİYONU (İTERATİF DÜZENLEME)
# =====================================================================================

def generate_image(image_path, prompt):
    """
    Mevcut bir görseli analiz edip, kullanıcının taleplerine göre 
    yeni bir görsel üreten birleşik fonksiyon.
    
    İş Akışı:
    1. Gemini Vision ile mevcut görseli analiz et
    2. Kullanıcının değişiklik talebini analiz sonucuyla birleştir
    3. Birleşik prompt'u DALL-E 3'e gönder
    4. Yeni görseli oluştur ve kaydet
    
    Bu yaklaşım "iteratif görsel düzenleme" olarak adlandırılır ve
    kullanıcının adım adım bir görseli iyileştirmesine olanak tanır.
    
    Örnek Kullanım:
    - İlk prompt: "Bir orman manzarası çiz"
    - İkinci prompt (iteratif): "Arka plana dağlar ekle"
    - Üçüncü prompt (iteratif): "Gökyüzüne kuşlar ekle"
    
    Args:
        image_path (str): Düzenlenecek görselin dosya yolu
        prompt (str): Kullanıcının değişiklik talebi
        
    Returns:
        str: Yeni oluşturulan görsel dosyasının yolu
    """
    
    # Adım 1: Gemini ile görsel analizi ve prompt oluşturma
    image_based_prompt = gemini_vision_with_local_file(
        image_path=image_path, 
        prompt=prompt
    )

    # Adım 2: DALL-E ile yeni görsel üretimi
    filename = generate_image_with_dalle(prompt=image_based_prompt)

    return filename  # Yeni görsel dosya yolunu döndür