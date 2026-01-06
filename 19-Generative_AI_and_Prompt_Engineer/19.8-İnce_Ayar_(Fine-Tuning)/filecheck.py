"""
===================================================================================
FINE-TUNING DOSYA FORMAT VE TOKEN ANALİZ ARACI
(Fine-Tuning File Format and Token Analysis Tool)
===================================================================================

Bu modül, OpenAI Fine-Tuning için hazırlanan JSONL dosyalarının:
- Format doğruluğunu kontrol eder
- Token sayılarını hesaplar
- Maliyet tahminlemesi yapar
- Veri kalitesi analizi sunar

AMAÇ:
-----
- Fine-tuning veri setinin OpenAI standartlarına uygunluğunu doğrulamak
- Eğitim maliyetini önceden tahmin etmek
- Potansiyel format hatalarını tespit etmek
- Token dağılımını analiz etmek

ÇALIŞMA PRENSİBİ:
-----------------
1. JSONL dosyası okunur ve parse edilir
2. Her örnek için format kontrolü yapılır
3. Token sayıları hesaplanır (tiktoken kullanarak)
4. İstatistiksel dağılım analizi yapılır
5. Tahmini maliyet ve epoch sayısı hesaplanır

KONTROL EDİLEN FORMAT KURALLARI:
---------------------------------
- Her satır geçerli bir JSON objesi olmalı
- "messages" anahtarı zorunlu
- Her mesajda "role" ve "content" zorunlu
- Role değerleri: "system", "user", "assistant", "function"
- En az bir "assistant" mesajı olmalı

KULLANIM:
---------
Terminal'de çalıştırmak için:
    python filecheck.py

ÇIKTI:
------
- Örnek sayısı
- Format hataları (varsa)
- Token dağılım istatistikleri
- Tahmini eğitim maliyeti

GEREKSINIMLER:
--------------
- tiktoken: OpenAI token sayacı
- numpy: İstatistiksel hesaplamalar
- json: JSON işlemleri

Yazar: [Proje Sahibi]
Tarih: 2024
Kaynak: OpenAI Cookbook - Fine-tuning veri doğrulama örneği
===================================================================================
"""

# ===================================================================================
# KÜTÜPHANE İMPORTLARI (Library Imports)
# ===================================================================================

import json                        # JSON dosya okuma ve parse etme
import tiktoken                    # OpenAI'ın resmi token sayma kütüphanesi
import numpy as np                 # Sayısal hesaplamalar ve istatistikler
from collections import defaultdict # Varsayılan değerli sözlük yapısı

# ===================================================================================
# DOSYA YOLU TANIMLAMASI (File Path Definition)
# ===================================================================================

# Fine-tuning veri dosyasının yolu
# NOT: JSONL formatı - her satır ayrı bir JSON objesi
# Dosya assets klasöründen çekilmektedir
ft_file_path = "../assets/19.8-Materyaller/data/processed data files/siir.jsonl"

# ===================================================================================
# VERİ YÜKLEME (Data Loading)
# ===================================================================================

# JSONL dosyasını oku ve her satırı ayrı JSON objesi olarak parse et
# encoding='utf-8': Türkçe karakterlerin doğru okunması için gerekli
with open(ft_file_path, 'r', encoding='utf-8') as f:
    dataset = [json.loads(line) for line in f]

# Toplam örnek sayısını yazdır
print("Num examples:", len(dataset))
print("*"*100)

# İlk örneği detaylı göster (veri yapısını anlamak için)
print("First example:")
for message in dataset[0]["messages"]:
    print(message)

print("*"*100)

# ===================================================================================
# FORMAT DOĞRULAMA (Format Validation)
# ===================================================================================

# Hata sayaçları için defaultdict kullan
# Otomatik olarak 0 ile başlayan sayaç oluşturur
format_errors = defaultdict(int)

# Her örneği format kuralları açısından kontrol et
for ex in dataset:
    
    # Kontrol 1: Her örnek bir dictionary (sözlük) olmalı
    if not isinstance(ex, dict):
        format_errors["data_type"] += 1
        continue
    
    # Kontrol 2: "messages" anahtarı zorunlu
    messages = ex.get("messages", None)
    if not messages:
        format_errors["missing_messages_list"] += 1
        continue
    
    # Her mesajı ayrı ayrı kontrol et
    for message in messages:
        
        # Kontrol 3: "role" ve "content" anahtarları zorunlu
        if "role" not in message or "content" not in message:
            format_errors["message_missing_key"] += 1
        
        # Kontrol 4: Sadece izin verilen anahtarlar kullanılmalı
        # İzin verilenler: role, content, name, function_call, weight
        if any(k not in ("role", "content", "name", "function_call", "weight") for k in message):
            format_errors["message_unrecognized_key"] += 1
        
        # Kontrol 5: Role değeri geçerli olmalı
        # Geçerli roller: system, user, assistant, function
        if message.get("role", None) not in ("system", "user", "assistant", "function"):
            format_errors["unrecognized_role"] += 1
        
        # Kontrol 6: Content veya function_call bulunmalı
        content = message.get("content", None)
        function_call = message.get("function_call", None)
        
        if (not content and not function_call) or not isinstance(content, str):
            format_errors["missing_content"] += 1
    
    # Kontrol 7: En az bir assistant mesajı olmalı
    # Fine-tuning'de model assistant yanıtlarını öğrenir
    if not any(message.get("role", None) == "assistant" for message in messages):
        format_errors["example_missing_assistant_message"] += 1

# Hata sonuçlarını raporla
if format_errors:
    print("Found errors:")
    for k, v in format_errors.items():
        print(f"{k}: {v}")
else:
    print("No errors found")

# ===================================================================================
# TOKEN SAYMA FONKSİYONLARI (Token Counting Functions)
# ===================================================================================

# cl100k_base: GPT-3.5 ve GPT-4 için kullanılan tokenizer
# Bu encoding, modelin metni nasıl parçalara ayırdığını simüle eder
encoding = tiktoken.get_encoding("cl100k_base")

def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
    """
    Mesaj listesindeki toplam token sayısını hesaplar.
    
    Bu fonksiyon, OpenAI'ın dahili token hesaplama yöntemini taklit eder.
    Tam olarak doğru olmayabilir, ancak iyi bir yaklaşım sağlar.
    
    Parametreler:
    -------------
    messages : list
        Mesaj listesi (her biri role ve content içeren dict)
    tokens_per_message : int
        Her mesaj için eklenen sabit token sayısı (varsayılan: 3)
        Bu, mesaj formatlaması için kullanılan özel tokenları temsil eder
    tokens_per_name : int
        "name" alanı varsa eklenen ek token sayısı (varsayılan: 1)
    
    Döndürür:
    ---------
    int : Toplam token sayısı
    
    Kaynak: OpenAI Cookbook - tiktoken token sayma örneği
    """
    num_tokens = 0
    for message in messages:
        # Her mesaj için sabit overhead token ekle
        num_tokens += tokens_per_message
        
        # Mesajdaki her alan için token say
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            # "name" alanı varsa ek token ekle
            if key == "name":
                num_tokens += tokens_per_name
    
    # Konuşma sonu için ek token ekle
    num_tokens += 3
    return num_tokens


def num_assistant_tokens_from_messages(messages):
    """
    Sadece assistant (asistan) mesajlarındaki token sayısını hesaplar.
    
    Fine-tuning'de asıl öğrenilen kısım assistant yanıtlarıdır.
    Bu nedenle assistant token sayısı özellikle önemlidir.
    
    Parametreler:
    -------------
    messages : list
        Mesaj listesi
    
    Döndürür:
    ---------
    int : Assistant mesajlarındaki toplam token sayısı
    """
    num_tokens = 0
    for message in messages:
        if message["role"] == "assistant":
            num_tokens += len(encoding.encode(message["content"]))
    return num_tokens


def print_distribution(values, name):
    """
    Sayısal değerlerin dağılım istatistiklerini yazdırır.
    
    Bu fonksiyon, veri setinin karakteristiklerini anlamak için
    temel istatistikleri hesaplar ve gösterir.
    
    Parametreler:
    -------------
    values : list
        Analiz edilecek sayısal değerler listesi
    name : str
        Dağılımın adı (çıktıda görüntülenecek)
    
    Çıktı:
    ------
    - min / max: Minimum ve maksimum değerler
    - mean / median: Ortalama ve medyan değerler
    - p5 / p95: 10. ve 90. yüzdelik dilimler (aykırı değer analizi için)
    """
    print(f"\n#### Distribution of {name}:")
    print(f"min / max: {min(values)}, {max(values)}")
    print(f"mean / median: {np.mean(values)}, {np.median(values)}")
    print(f"p5 / p95: {np.quantile(values, 0.1)}, {np.quantile(values, 0.9)}")

# ===================================================================================
# VERİ SETİ ANALİZİ (Dataset Analysis)
# ===================================================================================

# Eksik mesaj türü sayaçları
n_missing_system = 0   # System mesajı eksik olan örnek sayısı
n_missing_user = 0     # User mesajı eksik olan örnek sayısı

# Dağılım analizi için listeler
n_messages = []           # Her örnekteki mesaj sayısı
convo_lens = []           # Her örneğin toplam token sayısı
assistant_message_lens = [] # Her örnekteki assistant token sayısı

# Her örneği analiz et
for ex in dataset:
    messages = ex["messages"]
    
    # System mesajı kontrolü
    # System mesajı zorunlu değil ama önerilir (modelin davranışını belirler)
    if not any(message["role"] == "system" for message in messages):
        n_missing_system += 1
    
    # User mesajı kontrolü
    # User mesajı olmadan model neye yanıt vereceğini bilemez
    if not any(message["role"] == "user" for message in messages):
        n_missing_user += 1
    
    # Mesaj ve token istatistiklerini topla
    n_messages.append(len(messages))
    convo_lens.append(num_tokens_from_messages(messages))
    assistant_message_lens.append(num_assistant_tokens_from_messages(messages))

# Eksik mesaj istatistiklerini yazdır
print("Num examples missing system message:", n_missing_system)
print("Num examples missing user message:", n_missing_user)

# Dağılım istatistiklerini yazdır
print_distribution(n_messages, "num_messages_per_example")
print_distribution(convo_lens, "num_total_tokens_per_example")
print_distribution(assistant_message_lens, "num_assistant_tokens_per_example")

# Token limiti aşımı kontrolü
# OpenAI fine-tuning'de maksimum context window 4096 token
n_too_long = sum(l > 4096 for l in convo_lens)
print(f"\n{n_too_long} examples may be over the 4096 token limit, they will be truncated during fine-tuning")

# ===================================================================================
# MALİYET VE EPOCH TAHMİNLEMESİ (Cost and Epoch Estimation)
# ===================================================================================

# Fine-tuning fiyatlandırma parametreleri
MAX_TOKENS_PER_EXAMPLE = 4096  # Örnek başına maksimum faturalanacak token

# Epoch (dönem) hesaplama parametreleri
# Epoch: Tüm veri setinin bir kez işlenmesi
TARGET_EPOCHS = 3           # Hedef epoch sayısı
MIN_TARGET_EXAMPLES = 100   # Minimum toplam örnek (epoch * veri sayısı)
MAX_TARGET_EXAMPLES = 25000 # Maksimum toplam örnek
MIN_DEFAULT_EPOCHS = 1      # Minimum epoch sayısı
MAX_DEFAULT_EPOCHS = 25     # Maksimum epoch sayısı

# Dinamik epoch hesaplama
# Veri seti küçükse daha fazla epoch, büyükse daha az epoch
n_epochs = TARGET_EPOCHS
n_train_examples = len(dataset)

if n_train_examples * TARGET_EPOCHS < MIN_TARGET_EXAMPLES:
    # Veri seti çok küçük - daha fazla epoch gerekli
    n_epochs = min(MAX_DEFAULT_EPOCHS, MIN_TARGET_EXAMPLES // n_train_examples)
elif n_train_examples * TARGET_EPOCHS > MAX_TARGET_EXAMPLES:
    # Veri seti çok büyük - daha az epoch yeterli
    n_epochs = max(MIN_DEFAULT_EPOCHS, MAX_TARGET_EXAMPLES // n_train_examples)

# Faturalanacak toplam token sayısını hesapla
# Her örnek maksimum MAX_TOKENS_PER_EXAMPLE token faturalanır
n_billing_tokens_in_dataset = sum(min(MAX_TOKENS_PER_EXAMPLE, length) for length in convo_lens)

# Sonuçları yazdır
print(f"Dataset has ~{n_billing_tokens_in_dataset} tokens that will be charged for during training")
print(f"By default, you'll train for {n_epochs} epochs on this dataset")
print(f"By default, you'll be charged for ~{n_epochs * n_billing_tokens_in_dataset} tokens")