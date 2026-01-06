"""
===================================================================================
OPENAI FINE-TUNED MODEL SİLME ARACI (Fine-Tuned Model Deletion Tool)
===================================================================================

Bu modül, OpenAI platformunda oluşturulmuş fine-tuned (ince ayar yapılmış) 
modelleri silmek ve mevcut modelleri listelemek için kullanılır.

AMAÇ:
-----
- Artık kullanılmayan fine-tuned modelleri OpenAI hesabından kaldırmak
- Mevcut modelleri listeleyerek yönetim kolaylığı sağlamak
- API maliyetlerini optimize etmek (kullanılmayan modellerin temizlenmesi)

ÇALIŞMA PRENSİBİ:
-----------------
1. OpenAI API istemcisi oluşturulur
2. Belirtilen fine-tuned model silinir
3. Hesaptaki tüm modeller listelenir

KULLANIM:
---------
Terminal'de çalıştırmak için:
    python delete_ft.py

DİKKAT:
-------
- Model silme işlemi GERİ ALINAMAZ!
- Silmeden önce modelin artık gerekli olmadığından emin olun
- Yanlış model adı girilirse hata alınır

GEREKSINIMLER:
--------------
- openai: OpenAI API istemcisi
- python-dotenv: Çevre değişkenleri yönetimi

Yazar: [Proje Sahibi]
Tarih: 2024
===================================================================================
"""

# ===================================================================================
# KÜTÜPHANE İMPORTLARI (Library Imports)
# ===================================================================================

from openai import OpenAI      # OpenAI API istemcisi - model yönetimi için
import os                      # İşletim sistemi işlemleri (environment variables)
from dotenv import load_dotenv # .env dosyasından çevre değişkenlerini yükleme

# ===================================================================================
# ÇEVRE DEĞİŞKENLERİ YAPILANDIRMASI (Environment Variables Configuration)
# ===================================================================================

# .env dosyasındaki çevre değişkenlerini sisteme yükle
# Bu dosyada OpenAI API anahtarı güvenli şekilde saklanır
load_dotenv()

# OpenAI API anahtarını çevre değişkenlerinden al
# NOT: API anahtarları asla kod içinde açık yazılmamalıdır (güvenlik riski)
my_key_openai = os.getenv("openai_apikey")

# ===================================================================================
# OPENAI İSTEMCİ OLUŞTURMA (OpenAI Client Initialization)
# ===================================================================================

# OpenAI API istemcisini başlat
# Bu istemci tüm API işlemleri için kullanılacak
client = OpenAI(api_key=my_key_openai)

# ===================================================================================
# FINE-TUNED MODEL SİLME İŞLEMİ (Fine-Tuned Model Deletion)
# ===================================================================================

# Silinecek fine-tuned modelin tam adı
# Format: ft:base-model:organization:suffix:id
# Örnek: ft:gpt-3.5-turbo-0125:emreyz:orhan-veli-siir:93r1jeZT
#   - ft: fine-tuned model olduğunu belirtir
#   - gpt-3.5-turbo-0125: temel model
#   - emreyz: organizasyon/kullanıcı adı
#   - orhan-veli-siir: model için verilen özel isim (suffix)
#   - 93r1jeZT: benzersiz model kimliği
fine_tuned_model_name = "ft:gpt-3.5-turbo-0125:emreyz:orhan-veli-siir:93r1jeZT"

# Modeli sil ve yanıtı al
# DİKKAT: Bu işlem geri alınamaz! Model kalıcı olarak silinir.
response = client.models.delete(model=fine_tuned_model_name)

# Silme işleminin sonucunu ekrana yazdır
# Başarılı silme durumunda: {"id": "model-id", "object": "model", "deleted": True}
print(response)

# ===================================================================================
# MEVCUT MODELLERİ LİSTELEME (List Available Models)
# ===================================================================================

# Hesaptaki tüm modelleri getir
# Bu liste hem OpenAI'ın temel modellerini hem de fine-tuned modelleri içerir
list = client.models.list()

# Her modelin kimliğini ekrana yazdır
# Fine-tuned modeller "ft:" ile başlar
for model in list.data:

    print(model.id)