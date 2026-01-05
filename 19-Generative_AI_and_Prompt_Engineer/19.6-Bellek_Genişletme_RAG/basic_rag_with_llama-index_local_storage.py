# =============================================================================
# LLAMA-INDEX İLE TEMEL RAG (RETRIEVAL-AUGMENTED GENERATION) ÖRNEĞİ
# Bu dosya, LlamaIndex kütüphanesi kullanarak basit bir RAG sistemi oluşturur.
# RAG, büyük dil modellerinin dış veri kaynaklarından bilgi alarak yanıt 
# üretmesini sağlayan bir tekniktir.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# VectorStoreIndex: Dokümanları vektör formatında saklamak ve sorgulamak için kullanılır.
# Vektör indeksi, metinleri sayısal vektörlere dönüştürerek semantik arama yapmayı sağlar.
from llama_index import VectorStoreIndex

# SimpleDirectoryReader: Bir klasördeki tüm dosyaları okuyup Document nesnelerine dönüştürür.
# Bu sayede PDF, TXT, DOCX gibi farklı formatlardaki dosyalar otomatik olarak yüklenir.
from llama_index import SimpleDirectoryReader

# StorageContext: Vektör indeksinin depolama ayarlarını yönetir.
# Bu sınıf, indeksin nereden yükleneceğini veya nereye kaydedileceğini kontrol eder.
from llama_index import StorageContext

# load_index_from_storage: Daha önce diske kaydedilmiş bir indeksi yükler.
# Bu fonksiyon, her çalıştırmada indeksi yeniden oluşturmak yerine mevcut indeksi kullanmamızı sağlar.
from llama_index import load_index_from_storage

# pprint_response: Yanıtları güzel bir formatta yazdırmak için kullanılan yardımcı fonksiyon.
# Bu fonksiyon, hem yanıtı hem de kaynak dokümanları okunabilir şekilde görüntüler.
from llama_index.response.pprint_utils import pprint_response

# os: İşletim sistemi işlemleri için kullanılır (dosya/klasör kontrolü, ortam değişkenleri vb.)
import os

# dotenv: .env dosyasından ortam değişkenlerini yüklemek için kullanılır.
# Bu sayede API anahtarları gibi hassas bilgiler güvenli bir şekilde saklanabilir.
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# ORTAM DEĞİŞKENLERİNİN YÜKLENMESİ
# -----------------------------------------------------------------------------

# .env dosyasındaki değişkenleri ortam değişkeni olarak yükler.
# Bu dosya genellikle API anahtarları gibi gizli bilgileri içerir ve git'e eklenmez.
load_dotenv()

# OpenAI API anahtarını ortam değişkenlerinden alıp, OPENAI_API_KEY ortam değişkenine atar.
# LlamaIndex, OpenAI modellerini kullanırken bu ortam değişkenini otomatik olarak okur.
os.environ['OPENAI_API_KEY']=os.getenv("openai_apikey")

# -----------------------------------------------------------------------------
# DEPOLAMA DİZİNİ TANIMLAMASI
# -----------------------------------------------------------------------------

# PERSIST_DIR: Vektör indeksinin kaydedileceği klasör yolu.
# Bu klasör, indeksin kalıcı olarak saklanmasını sağlar.
PERSIST_DIR = "./storage"

# -----------------------------------------------------------------------------
# İNDEKS OLUŞTURMA VEYA YÜKLEME MANTIĞI
# -----------------------------------------------------------------------------

# Eğer depolama klasörü mevcut DEĞİLSE, yeni bir indeks oluşturulur.
# Bu kontrol, her çalıştırmada gereksiz yere indeks oluşturmayı önler.
if not os.path.exists(PERSIST_DIR):

    # "datasets_19/19.6-Datasets" klasöründeki tüm dokümanları (örn. gelecek.pdf) oku ve Document nesnelerine dönüştür.
    # SimpleDirectoryReader, klasördeki tüm desteklenen dosya formatlarını otomatik algılar.
    # Göreli yol kullanarak üst dizindeki datasets klasörüne erişilir.
    documents = SimpleDirectoryReader("../datasets_19/19.6-Datasets").load_data()
    
    # Okunan dokümanlardan bir vektör indeksi oluştur.
    # show_progress=True parametresi, indeksleme sürecini takip etmemizi sağlar.
    # Bu adımda dokümanlar parçalara ayrılır ve her parça için embedding vektörü oluşturulur.
    index = VectorStoreIndex.from_documents(documents, show_progress=True)

    # Oluşturulan indeksi belirtilen klasöre kalıcı olarak kaydet.
    # Bu sayede program yeniden çalıştırıldığında indeks yeniden oluşturulmaz.
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    
# Depolama klasörü mevcutsa, önceden oluşturulmuş indeksi yükle.
# Bu durum, programın daha hızlı başlamasını sağlar.
else:

    # Depolama ayarlarını mevcut klasörden oluştur.
    # StorageContext, indeksin bileşenlerini (node'lar, vektörler vb.) yönetir.
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    
    # Kaydedilmiş indeksi diskten belleğe yükle.
    # Bu işlem, indeksi yeniden oluşturmaktan çok daha hızlıdır.
    index = load_index_from_storage(storage_context)

# -----------------------------------------------------------------------------
# SORGU MOTORU OLUŞTURMA VE SORGULAMA
# -----------------------------------------------------------------------------

# İndeksten bir sorgu motoru oluştur.
# Sorgu motoru, kullanıcı sorularını alıp ilgili dokümanları bulur ve yanıt üretir.
query_engine = index.as_query_engine()

# Türkçe bir soru sor ve yanıt al.
# Sorgu motoru şu adımları gerçekleştirir:
# 1. Soruyu vektöre dönüştürür
# 2. En benzer doküman parçalarını bulur
# 3. Bu parçaları bağlam olarak kullanarak LLM'den yanıt alır
response = query_engine.query("Yapay Zekanın kullanım alanları nelerdir?")

# -----------------------------------------------------------------------------
# SONUÇLARIN GÖRÜNTÜLENMESİ
# -----------------------------------------------------------------------------

# Yanıtı ve kaynak dokümanları güzel bir formatta yazdır.
# show_source=True parametresi, yanıtın hangi kaynaklardan oluşturulduğunu gösterir.
# Bu özellik, RAG sistemlerinde şeffaflık sağlamak için önemlidir.
pprint_response(response,show_source=True)