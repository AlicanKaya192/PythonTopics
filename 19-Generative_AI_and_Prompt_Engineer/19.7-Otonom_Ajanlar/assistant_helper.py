# =======================================================================================
# DOSYA: assistant_helper.py
# AÇIKLAMA: OpenAI Assistants API ile etkileşim için yardımcı fonksiyonlar içerir.
#
# KONU: OTONOM AJANLAR - OpenAI Assistants API
# 
# Bu modül, OpenAI'nin Assistants API'si ile çalışmak için gerekli tüm fonksiyonları
# içerir. Assistants API, önceki Chat Completions API'den farklı olarak kalıcı
# (persistent) sohbet geçmişi, dosya işleme ve araç kullanımı gibi gelişmiş
# özellikler sunar.
#
# OpenAI Assistants API Temel Kavramları:
# ----------------------------------------
# 1. ASSISTANT: Önceden tanımlanmış bir yapay zeka asistanı. Her asistan:
#    - Belirli bir rol ve kişiliğe sahiptir
#    - Belirli araçları kullanabilir (code interpreter, retrieval, function calling)
#    - Belirli dosyalara erişebilir
#    - Belirli talimatları takip eder
#
# 2. THREAD: Bir konuşmayı temsil eder. Thread içinde:
#    - Tüm mesajlar sıralı olarak saklanır
#    - Bağlam (context) korunur
#    - Birden fazla run çalıştırılabilir
#
# 3. MESSAGE: Thread içindeki bir mesajı temsil eder:
#    - Kullanıcı veya asistan tarafından oluşturulabilir
#    - Metin, kod veya dosya içerebilir
#
# 4. RUN: Asistanın bir thread üzerinde çalışmasını temsil eder:
#    - Asistan, thread'deki tüm mesajları okur
#    - Yanıt oluşturur
#    - Gerekirse araçları kullanır
#
# API Akışı:
# ----------
# 1. Yeni bir Thread oluştur (veya mevcut olanı kullan)
# 2. Thread'e kullanıcı mesajı ekle
# 3. Run oluştur (asistanı çalıştır)
# 4. Run tamamlanana kadar bekle
# 5. Asistan yanıtını al
# =======================================================================================

from openai import OpenAI  # OpenAI Python SDK - Assistants API erişimi için
import time  # Zamanlama işlemleri - run durumunu kontrol ederken bekleme için
import os  # İşletim sistemi fonksiyonları - ortam değişkenlerine erişim için
from dotenv import load_dotenv  # .env dosyasından ortam değişkenlerini yükler

# =======================================================================================
# ORTAM DEĞİŞKENLERİ VE API YAPILANDIRMASI
# =======================================================================================
# load_dotenv() fonksiyonu, .env dosyasındaki değişkenleri ortam değişkenlerine yükler.
# Bu güvenli bir yöntemdir çünkü API anahtarları kod içinde görünmez.
# .env dosyası formatı: ANAHTAR_ADI=değer
# =======================================================================================

load_dotenv()  # .env dosyasını yükle

# OpenAI API anahtarını ortam değişkenlerinden al
# os.getenv() fonksiyonu, ortam değişkeninin değerini döndürür
# Değişken yoksa None döner
my_key_openai = os.getenv("openai_apikey")

# OpenAI client'ı oluştur - tüm API çağrıları bu client üzerinden yapılır
# Client, API anahtarını ve diğer yapılandırma ayarlarını saklar
client = OpenAI(api_key=my_key_openai)

# =======================================================================================
# ASISTAN KİMLİĞİ
# =======================================================================================
# assistant_id: OpenAI platformunda önceden oluşturulmuş bir asistanın benzersiz kimliği
# Bu asistan, OpenAI Playground veya API üzerinden oluşturulmuş olmalıdır.
# 
# Asistan oluştururken belirlenen özellikler:
# - İsim (name): "Python Kodlama Asistanı"
# - Talimatlar (instructions): Asistanın nasıl davranacağını belirler
# - Model (model): Kullanılacak dil modeli (gpt-4, gpt-3.5-turbo vb.)
# - Araçlar (tools): code_interpreter, retrieval, function calling
# =======================================================================================

assistant_id = "asst_9PkxJouK0097L2lrUxSznB2U"  # Python Kodlama Asistanı ID'si

# =======================================================================================
# THREAD YÖNETİM FONKSİYONLARI
# =======================================================================================
# Thread, bir konuşmayı temsil eder ve tüm mesajları içerir.
# Aynı thread_id kullanılarak sohbet devam ettirilebilir.
# =======================================================================================


def start_new_thread():
    """
    Yeni bir konuşma thread'i oluşturur.
    
    Thread Nedir?
    -------------
    Thread, OpenAI Assistants API'de bir konuşmayı temsil eden veri yapısıdır.
    - Her thread benzersiz bir ID'ye sahiptir
    - Thread içindeki tüm mesajlar kronolojik sırada saklanır
    - Thread silininceye kadar kalıcıdır (persistent)
    
    Returns:
        str: Yeni oluşturulan thread'in benzersiz kimliği (thread_id)
    
    Kullanım Senaryosu:
    -------------------
    1. Kullanıcı uygulamayı ilk kez açtığında yeni thread oluşturulur
    2. Bu thread_id session_state'te saklanır
    3. Sonraki mesajlar aynı thread'e eklenir
    """
    # client.beta.threads.create(): Yeni bir thread oluşturur
    # beta: Assistants API hala beta aşamasında olduğu için bu namespace kullanılır
    thread = client.beta.threads.create()
    
    # Thread nesnesinden ID'yi al
    thread_id = thread.id

    return thread_id


def add_message_to_thread(thread_id, prompt):
    """
    Mevcut bir thread'e yeni bir kullanıcı mesajı ekler.
    
    Parametreler:
    -------------
    thread_id (str): Mesajın ekleneceği thread'in benzersiz kimliği
    prompt (str): Kullanıcının gönderdiği mesaj metni
    
    Mesaj Yapısı:
    -------------
    OpenAI Assistants API'de her mesaj şunları içerir:
    - role: "user" veya "assistant" (bu fonksiyonda her zaman "user")
    - content: Mesaj içeriği (metin, kod veya dosya olabilir)
    - thread_id: Mesajın ait olduğu thread
    
    Not:
    ----
    Bu fonksiyon sadece mesajı ekler, asistanı çalıştırmaz.
    Asistanın yanıt vermesi için execute_run_cycle() fonksiyonu çağrılmalıdır.
    """
    # client.beta.threads.messages.create(): Thread'e yeni mesaj ekler
    message = client.beta.threads.messages.create(
        thread_id=thread_id,  # Hedef thread
        role="user",  # Mesaj gönderen: kullanıcı
        content=prompt,  # Mesaj içeriği
    )


def execute_run_cycle(thread_id):
    """
    Asistanı çalıştırır ve yanıt alana kadar bekler.
    
    Bu fonksiyon, Assistants API'nin temel çalışma döngüsünü gerçekleştirir:
    1. Yeni bir Run oluştur
    2. Run durumunu kontrol et (polling)
    3. Run tamamlanınca yanıtı al
    
    Run Nedir?
    ----------
    Run, bir asistanın belirli bir thread üzerinde çalışmasını temsil eder.
    Run başlatıldığında asistan:
    - Thread'deki tüm mesajları okur
    - Bağlamı analiz eder
    - Uygun yanıtı oluşturur
    - Gerekirse araçları kullanır (code interpreter, retrieval vb.)
    
    Run Durumları (States):
    -----------------------
    - queued: Sırada bekliyor
    - in_progress: İşleniyor
    - requires_action: Araç çağrısı bekliyor
    - completed: Tamamlandı
    - failed: Hata oluştu
    - cancelled: İptal edildi
    - expired: Süresi doldu
    
    Parametreler:
    -------------
    thread_id (str): Asistanın çalışacağı thread'in benzersiz kimliği
    
    Returns:
        str: Asistanın ürettiği yanıt metni
    """
    # -------------------------------------------------------------------------
    # RUN OLUŞTURMA
    # -------------------------------------------------------------------------
    # client.beta.threads.runs.create(): Yeni bir run başlatır
    # Run başladığında asistan thread'deki mesajları işlemeye başlar
    # -------------------------------------------------------------------------
    
    run = client.beta.threads.runs.create(
        thread_id=thread_id,  # Çalışılacak thread
        assistant_id=assistant_id  # Kullanılacak asistan
    )

    # -------------------------------------------------------------------------
    # RUN DURUMU KONTROLÜ (POLLING)
    # -------------------------------------------------------------------------
    # Run asenkron çalışır, bu nedenle tamamlanana kadar beklememiz gerekir.
    # Polling: Belirli aralıklarla durumu kontrol etme yöntemi
    # -------------------------------------------------------------------------
    
    while True:
        # Run'ın güncel durumunu al
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        # Run tamamlandıysa döngüden çık
        # completed_at: Run'ın tamamlandığı zaman damgası
        # Eğer None ise run hala devam ediyor demektir
        if run.completed_at:
            # Geçen süreyi hesapla (tamamlanma zamanı - başlangıç zamanı)
            elapsed = run.completed_at - run.created_at
            # Süreyi okunabilir formata çevir (SS:DD:SS)
            elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            print(f"Run completed in {elapsed}")  # Geliştirici için loglama
            print("-"*100)  # Görsel ayırıcı
            break
        
        # Her saniye bir durum kontrolü yap
        # Bu değer artırılarak API çağrı sayısı azaltılabilir
        time.sleep(1)
    
    # -------------------------------------------------------------------------
    # YANIT ALMA
    # -------------------------------------------------------------------------
    # Run tamamlandıktan sonra thread'teki son mesajı al
    # Bu mesaj asistanın yanıtını içerir
    # -------------------------------------------------------------------------
    
    # Thread'deki tüm mesajları al
    # Mesajlar en yeniden en eskiye doğru sıralanır (varsayılan)
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    
    # İlk mesaj (en yeni) asistanın yanıtıdır
    last_message = messages.data[0]

    # Mesaj içeriğini al
    # content[0]: İlk içerik bloğu (metin)
    # .text.value: Metin değeri
    AI_Response = last_message.content[0].text.value

    return AI_Response