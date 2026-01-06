"""
===================================================================================
FINE-TUNING JSONL DOSYASI HAZIRLAMA ARACI
(Fine-Tuning JSONL File Preparation Tool)
===================================================================================

Bu modül, Excel formatındaki şiir veri setini OpenAI Fine-Tuning için gereken
JSONL (JSON Lines) formatına dönüştürür.

AMAÇ:
-----
- Etiketlenmiş şiir verisini fine-tuning formatına çevirmek
- OpenAI API'nin kabul edeceği veri yapısını oluşturmak
- Tutarlı ve kaliteli eğitim verisi üretmek

VERİ DÖNÜŞÜM SÜRECİ:
--------------------
Excel Kaynak Yapısı:
    | siir                    | response                          |
    |-------------------------|-----------------------------------|
    | Gemilerin en güzeli...  | deniz, aşk, özlem, romantizm      |
    | İstanbul'u dinliyorum...| şehir, melankoli, ses, gözlem     |

JSONL Hedef Yapısı:
    {"messages": [
        {"role": "system", "content": "Sen ünlü Türk şairi Orhan Veli'sin..."},
        {"role": "user", "content": "Şunlarla ilgili bir şiir yazar mısın? deniz, aşk..."},
        {"role": "assistant", "content": "Gemilerin en güzeli..."}
    ]}

NEDEN BU FORMAT?
----------------
- OpenAI Fine-Tuning API'si bu formatı zorunlu kılar
- Sohbet tarzı (chat) modeller için uygundur (GPT-3.5-turbo, GPT-4)
- System prompt model davranışını, user-assistant çifti örnek veriyi tanımlar

KULLANIM:
---------
Terminal'de çalıştırmak için:
    python prepare_ft_file.py

ÇIKTI:
------
- ../assets/19.8-Materyaller/data/processed data files/siir.jsonl dosyası oluşturulur

GEREKSINIMLER:
--------------
- pandas: Excel dosya okuma
- json: JSON formatında yazma
- openpyxl: Excel okuma motoru (pip install openpyxl)

Yazar: [Proje Sahibi]
Tarih: 2024
===================================================================================
"""

# ===================================================================================
# KÜTÜPHANE İMPORTLARI (Library Imports)
# ===================================================================================

import pandas as pd  # Veri manipülasyonu ve Excel dosya okuma
import json          # JSON formatında dosya yazma

# ===================================================================================
# DOSYA YOLLARI (File Paths)
# ===================================================================================

# Kaynak Excel dosyası - etiketlenmiş şiirleri içerir
# Bu dosya assign_labels.py tarafından oluşturulmuş/güncellenmiştir
# Assets klasöründen çekilmektedir
excel_file_path = '../assets/19.8-Materyaller/data/siir.xlsx'

# Hedef JSONL dosyası - fine-tuning için kullanılacak
# JSONL: Her satır ayrı bir JSON objesi (JSON Lines formatı)
jsonl_file_path = '../assets/19.8-Materyaller/data/processed data files/siir.jsonl'

# ===================================================================================
# VERİ OKUMA (Data Loading)
# ===================================================================================

# Excel dosyasını pandas DataFrame olarak oku
# Varsayılan olarak ilk sayfayı okur
df = pd.read_excel(excel_file_path)

# ===================================================================================
# SİSTEM PROMPTU TANIMLAMASI (System Prompt Definition)
# ===================================================================================

# System prompt: Fine-tuned modelin kişiliğini ve davranışını belirler
# Bu prompt her eğitim örneğinde aynı kalır
# Model bu talimatları öğrenerek Orhan Veli tarzında şiir yazmayı öğrenir
system_prompt = """Sen ünlü Türk şairi Orhan Veli'sin.
Sana verilen konu, tema, duygu, motifler veya anahtar kelimelerle ilgili şiirler yazıyorsun.
Yanıt olarak sadece şiir yazıyorsun. Yanıtında başka hiçbir açıklama ya da metne yer vermiyorsun.
Yalnızca, verilen kelimelerle alakalı yazdığın şiiri yanıt olarak iletiyorsun.
"""

# ===================================================================================
# JSONL DOSYASI OLUŞTURMA (JSONL File Creation)
# ===================================================================================

# JSONL dosyasını yazma modunda aç
# encoding='utf-8': Türkçe karakterlerin doğru yazılması için zorunlu
with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:

    # DataFrame'deki her satır için döngü
    # iterrows(): Her satırı (index, row) tuple'ı olarak döndürür
    for index, row in df.iterrows():

        # =======================================================================
        # KULLANICI SORGUSU OLUŞTURMA (User Query Creation)
        # =======================================================================
        
        # Kullanıcı promptu: 'response' sütunundaki etiketleri kullanır
        # Bu sütun, şiirin konu/tema/duygu/motiflerini içerir
        # Örnek: "Şunlarla ilgili bir şiir yazar mısın? deniz, aşk, özlem"
        user_query = f"Şunlarla ilgili bir şiir yazar mısın? {row['response']}"

        # =======================================================================
        # JSON OBJESİ OLUŞTURMA (JSON Object Creation)
        # =======================================================================
        
        # OpenAI Fine-Tuning formatına uygun mesaj yapısı
        # Her örnek üç mesajdan oluşur:
        json_object = {
            "messages": [
                # 1. System Message: Modelin rolü ve davranışı
                #    - Model bu talimatları her örneğe uygular
                #    - Fine-tuning sonrası bu davranış kalıcı olur
                {"role": "system", "content": system_prompt},
                
                # 2. User Message: Kullanıcı isteği
                #    - Etiketler/anahtar kelimeler burada yer alır
                #    - Model bu girdiye yanıt vermeyi öğrenir
                {"role": "user", "content": user_query},
                
                # 3. Assistant Message: Modelin öğrenmesi gereken yanıt
                #    - Gerçek şiir metni burada yer alır
                #    - Model bu tarz yanıtlar vermeyi öğrenir
                {"role": "assistant", "content": row['siir']}
            ]
        }

        # =======================================================================
        # JSONL SATIRI YAZMA (JSONL Line Writing)
        # =======================================================================
        
        # JSON objesini string'e çevir ve dosyaya yaz
        # ensure_ascii=False: Türkçe karakterlerin olduğu gibi yazılması için
        #   - True olsaydı: "şiir" → "\u015fiir" (Unicode escape)
        #   - False olunca: "şiir" → "şiir" (okunabilir)
        # '\n': Her JSON objesi ayrı satırda olmalı (JSONL formatı kuralı)
        jsonl_file.write(json.dumps(json_object, ensure_ascii=False) + '\n')

# ===================================================================================
# İŞLEM TAMAMLANDI
# ===================================================================================
# 
# Oluşturulan JSONL dosyası artık OpenAI Fine-Tuning API'sine yüklenebilir.
# 
# Sonraki adımlar:
# 1. filecheck.py ile dosya formatını doğrula
# 2. OpenAI platformuna dosyayı yükle
# 3. Fine-tuning işlemini başlat
# 
# API ile yükleme örneği:
#   from openai import OpenAI
#   client = OpenAI()
#   file = client.files.create(file=open(jsonl_file_path, "rb"), purpose="fine-tune")
# ===================================================================================
