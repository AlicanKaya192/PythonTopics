# ===================================================================================
# 19.10 - YERELDE ÇALIŞMA: LOCAL HELPER MODÜLÜ
# ===================================================================================
# Bu dosya, yerel olarak çalışan LLM modelleri ile iletişim kurmak için
# gerekli yardımcı fonksiyonları içerir.
# 
# MODÜL AMACI:
# ------------
# Ollama ve LM Studio gibi yerel AI çözümleri ile OpenAI uyumlu API üzerinden
# iletişim kurmayı sağlar. Bu sayede bulut API'larından bağımsız çalışabilirsiniz.
#
# NEDEN AYRI BİR MODÜL?
# ---------------------
# - Separation of Concerns (Endişelerin Ayrılması) prensibi
# - UI kodu (local_chat.py) ile API mantığı ayrı tutulur
# - Kod tekrarı önlenir, bakım kolaylaşır
# - Farklı UI'lar (CLI, web, desktop) aynı helper'ı kullanabilir
#
# OPENAI UYUMLULUĞU NEDİR?
# ------------------------
# Ollama ve LM Studio, OpenAI'ın API formatını taklit eder.
# Bu sayede:
# - Aynı kod yapısı hem bulut hem yerel için çalışır
# - OpenAI Python kütüphanesi doğrudan kullanılabilir
# - Sadece base_url değiştirilerek farklı sağlayıcılara geçiş yapılır
# - Öğrenme eğrisi minimuma iner
#
# DESTEKLENEN YEREL ARAÇLAR:
# --------------------------
# 1. OLLAMA (https://ollama.ai)
#    - Port: 11434
#    - API: OpenAI uyumlu
#    - Modeller: mistral, llama2, codellama, phi, neural-chat vb.
#    - Kurulum: brew install ollama (macOS) veya installer (Windows)
#
# 2. LM STUDIO (https://lmstudio.ai)
#    - Port: 1234 (varsayılan)
#    - API: OpenAI uyumlu
#    - Modeller: GGUF formatında tüm modeller
#    - Kurulum: GUI installer
# ===================================================================================

from openai import OpenAI  # OpenAI uyumlu API'ler için Python client

# ===================================================================================
# OLLAMA İLE YANIT ÜRETİMİ
# ===================================================================================

def generate_with_ollama(model_name="mistral", chat_history=[], temperature=0):
    """
    Ollama kullanarak yerel LLM'den yanıt üretir.
    
    OLLAMA NEDİR?
    -------------
    - Meta'nın Llama, Mistral AI ve diğer açık kaynak modelleri çalıştıran platform
    - Basit CLI arayüzü: "ollama run mistral"
    - OpenAI uyumlu API sunucusu built-in
    - Hafif ve hızlı, düşük sistem gereksinimleri
    
    NEDEN OLLAMA TERCİH EDİLİR?
    ---------------------------
    1. Ücretsiz ve açık kaynak
    2. Basit kurulum ve kullanım
    3. Geniş model desteği
    4. Aktif topluluk
    5. Apple Silicon optimizasyonu (M1, M2, M3)
    
    BU FONKSİYON NE YAPAR?
    ----------------------
    1. Ollama API sunucusuna bağlanır (localhost:11434)
    2. Tüm sohbet geçmişini gönderir
    3. Belirtilen modelden yanıt alır
    4. Yanıt metnini döndürür
    
    Args:
        model_name (str): Kullanılacak model adı. Varsayılan: "mistral"
            - Popüler seçenekler: mistral, llama2, codellama, phi, neural-chat
            - Yüklemek için: ollama pull <model_name>
            
        chat_history (list): Sohbet geçmişi. Her eleman bir dict:
            [{"role": "user", "content": "Merhaba"},
             {"role": "assistant", "content": "Merhaba!"}]
             
        temperature (float): Yaratıcılık seviyesi (0.0 - 1.0)
            - 0: Deterministik, tutarlı yanıtlar
            - 0.7: Dengeli yaratıcılık
            - 1: Maksimum yaratıcılık (rastgele olabilir)
    
    Returns:
        str: Model tarafından üretilen yanıt metni
    
    ÖRNEK KULLANIM:
    ---------------
    >>> history = [{"role": "user", "content": "Python nedir?"}]
    >>> response = generate_with_ollama("mistral", history, 0.7)
    >>> print(response)
    "Python, yüksek seviyeli bir programlama dilidir..."
    
    ÖNEMLİ NOTLAR:
    --------------
    - Ollama'nın çalışıyor olması gerekir: ollama serve
    - Model önceden indirilmiş olmalı: ollama pull mistral
    - İlk çağrı modeli belleğe yükler, biraz zaman alabilir
    """
    
    # ===================================================================================
    # OPENAI CLIENT OLUŞTURMA (OLLAMA İÇİN)
    # ===================================================================================
    # OpenAI client'ını Ollama sunucusuna yönlendiriyoruz.
    # 
    # BASE_URL NEDİR?
    # ---------------
    # - Normalde OpenAI API'si: https://api.openai.com/v1
    # - Ollama yerel sunucu: http://localhost:11434/v1
    # - Bu değişiklikle aynı kod yerel modelle çalışır
    # 
    # API_KEY NEDEN "ollama"?
    # -----------------------
    # - Ollama aslında API key gerektirmez (yerel çalışıyor)
    # - Ancak OpenAI client zorunlu kıldığı için placeholder değer veriyoruz
    # - Herhangi bir string olabilir, sadece boş olmamalı
    
    client = OpenAI(
        base_url='http://localhost:11434/v1',  # Ollama API adresi
        api_key="ollama"  # Placeholder - Ollama için gerçek key gerekmez
    )

    # ===================================================================================
    # CHAT COMPLETION İSTEĞİ
    # ===================================================================================
    # OpenAI formatında chat completion isteği gönderiyoruz.
    # 
    # BU İSTEK NE İÇERİR?
    # -------------------
    # - model: Hangi modelin kullanılacağı (örn: mistral)
    # - messages: Tüm sohbet geçmişi (bağlam için önemli)
    # - temperature: Yaratıcılık ayarı
    # 
    # NEDEN TÜM GEÇMİŞİ GÖNDERİYORUZ?
    # --------------------------------
    # - LLM'ler "stateless"tir, önceki mesajları hatırlamazlar
    # - Her istekte tüm bağlamı yeniden göndermeliyiz
    # - Bu sayede AI, konuşmanın akışını anlayabilir
    
    AI_Response = client.chat.completions.create(
        model=model_name,       # Kullanılacak model
        messages=chat_history,  # Tüm sohbet geçmişi
        temperature=temperature # Yaratıcılık seviyesi
    )

    # ===================================================================================
    # YANIT ÇIKARIMI
    # ===================================================================================
    # API yanıtından asıl metin içeriğini çıkarıyoruz.
    # 
    # YANIT YAPISI:
    # -------------
    # AI_Response.choices[0] → İlk (ve genelde tek) yanıt seçeneği
    # .message → Mesaj objesi
    # .content → Gerçek metin içeriği
    # 
    # NEDEN choices[0]?
    # -----------------
    # - API birden fazla yanıt üretebilir (n parametresi ile)
    # - Varsayılan olarak tek yanıt üretilir
    # - İlk elemanı (.choices[0]) alıyoruz
    
    return AI_Response.choices[0].message.content


# ===================================================================================
# LM STUDIO İLE YANIT ÜRETİMİ
# ===================================================================================

def generate_with_lmstudio(chat_history=[], temperature=0):
    """
    LM Studio kullanarak yerel LLM'den yanıt üretir.
    
    LM STUDIO NEDİR?
    ----------------
    - GUI tabanlı yerel LLM çalıştırma platformu
    - GGUF formatındaki modelleri destekler
    - OpenAI uyumlu API sunucusu içerir
    - Windows, macOS ve Linux desteği
    
    NEDEN LM STUDIO TERCİH EDİLİR?
    ------------------------------
    1. Kullanıcı dostu grafik arayüz
    2. Kolay model indirme ve yönetim
    3. Görsel sohbet arayüzü (kendi chat UI'ı var)
    4. Detaylı model bilgileri (VRAM, hız vb.)
    5. Quantization seçenekleri (bellek optimizasyonu)
    
    LM STUDIO vs OLLAMA:
    --------------------
    | Özellik        | LM Studio          | Ollama           |
    |----------------|--------------------|--------------------|
    | Arayüz           | GUI (görsel)        | CLI (komut satırı) |
    | Model formatı  | GGUF               | Çeşitli            |
    | Öğrenme eğrisi | Düşük              | Orta               |
    | Kaynak kullanımı| Orta               | Düşük              |
    | Model yönetimi | GUI'dan kolay      | Komutlarla         |
    
    BU FONKSİYON NE YAPAR?
    ----------------------
    1. LM Studio API sunucusuna bağlanır (localhost:1234)
    2. Tüm sohbet geçmişini gönderir
    3. LM Studio'da yüklü modelden yanıt alır
    4. Yanıt metnini döndürür
    
    Args:
        chat_history (list): Sohbet geçmişi. Her eleman bir dict:
            [{"role": "user", "content": "Merhaba"},
             {"role": "assistant", "content": "Merhaba!"}]
             
        temperature (float): Yaratıcılık seviyesi (0.0 - 1.0)
    
    Returns:
        str: Model tarafından üretilen yanıt metni
    
    ÖRNEK KULLANIM:
    ---------------
    >>> history = [{"role": "user", "content": "JavaScript nedir?"}]
    >>> response = generate_with_lmstudio(history, 0.5)
    >>> print(response)
    "JavaScript, web tarayıcılarında çalışan..."
    
    ÖNEMLİ NOTLAR:
    --------------
    - LM Studio açık ve Local Server aktif olmalı
    - LM Studio'da bir model yüklenmiş olmalı
    - Model seçimi LM Studio GUI'dan yapılır (kod tarafında belirtilmez)
    """
    
    # ===================================================================================
    # OPENAI CLIENT OLUŞTURMA (LM STUDIO İÇİN)
    # ===================================================================================
    # OpenAI client'ını LM Studio sunucusuna yönlendiriyoruz.
    # 
    # PORT FARKI:
    # -----------
    # - LM Studio: 1234 (varsayılan)
    # - Ollama: 11434
    # 
    # API_KEY NEDEN "lm-studio"?
    # --------------------------
    # - LM Studio da API key gerektirmez (yerel çalışıyor)
    # - Sadece placeholder olarak kullanılıyor
    
    client = OpenAI(
        base_url="http://localhost:1234/v1",  # LM Studio API adresi
        api_key="lm-studio"  # Placeholder - gerçek key gerekmez
    )

    # ===================================================================================
    # CHAT COMPLETION İSTEĞİ
    # ===================================================================================
    # 
    # MODEL PARAMETRESI NEDEN BOŞ?
    # ----------------------------
    # - LM Studio'da model seçimi GUI üzerinden yapılır
    # - Hangi model yüklüyse o kullanılır
    # - Boş string göndermek, aktif modeli kullanmak demektir
    # - Bu esneklik sağlar: kodu değiştirmeden model değiştirebilirsiniz
    
    AI_Response = client.chat.completions.create(
        model="",               # LM Studio'da yüklü modeli kullan
        messages=chat_history,  # Tüm sohbet geçmişi
        temperature=temperature # Yaratıcılık seviyesi
    )

    # Yanıt metnini döndür
    return AI_Response.choices[0].message.content


# ===================================================================================
# MODÜL SONU
# ===================================================================================
# Bu modül, yerel LLM'lerle çalışmanın temelini oluşturur.
# OpenAI uyumluluğu sayesinde minimum kod değişikliğiyle
# bulut ve yerel modeller arasında geçiş yapabilirsiniz.
# 
# GELİŞTİRME ÖNERİLERİ:
# ---------------------
# 1. Otomatik model listesi alma (Ollama için /api/tags endpoint'i)
# 2. Streaming desteği (gerçek zamanlı yanıt akışı)
# 3. Hata yönetimi (bağlantı hatası, timeout vb.)
# 4. Retry mekanizması (başarısız istekleri tekrar deneme)
# 5. Token sayımı (yanıt uzunluğu kontrolü)
# 6. System prompt özelleştirme desteği
#
# YEREL MODEL ÖNERİLERİ:
# ----------------------
# - Genel Sohbet: mistral, llama2-chat, neural-chat
# - Kod Yazma: codellama, deepseek-coder, phind-codellama
# - Türkçe: Henüz sınırlı, mistral genelde en iyi performans
# - Düşük Bellek: phi-2, tinyllama, stablelm-zephyr
# ===================================================================================
