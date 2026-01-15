# =============================================================================
# CHROMADB İLE BENZERİLİK SKORLARINI GÖSTERME ÖRNEĞİ
# Bu dosya, ChromaDB vektör veritabanı kullanarak doküman araması yapar ve
# dönen sonuçların benzerlik (distance) skorlarını gösterir.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# chromadb: Açık kaynaklı, embedding-native vektör veritabanı.
# Basit API'si ve hızlı başlangıcı ile popüler bir seçenektir.
# Hem in-memory hem de kalıcı depolama modlarını destekler.
import chromadb

# -----------------------------------------------------------------------------
# CHROMADB CLİENT'I OLUŞTURMA
# -----------------------------------------------------------------------------

# HTTP client oluştur - ayrı çalışan ChromaDB sunucusuna bağlan.
# NOT: Bu kodu çalıştırmadan önce, başka bir terminalde "chroma run" komutu
# ile ChromaDB sunucusunu başlatmanız gerekir.
# Varsayılan olarak localhost:8000 adresinde çalışır.
client = chromadb.HttpClient()

# -----------------------------------------------------------------------------
# KOLEKSİYON KONTROLÜ VE OLUŞTURMA
# -----------------------------------------------------------------------------

# Koleksiyon durumu flag'i - koleksiyon var mı yok mu?
collection_status = False

# Mevcut koleksiyonları listele
current_collections = client.list_collections()

# Koleksiyon listesinde "new_collection" var mı kontrol et
for collection in current_collections:
    if collection.name == "new_collection":
        collection_status = True
        break
        
# Koleksiyon mevcutsa, mevcut koleksiyonu al
# Aksi halde yeni koleksiyon oluştur ve dokümanları ekle
if collection_status:
    # Mevcut koleksiyonu al
    my_collection = client.get_collection("new_collection")
else:
    # Yeni koleksiyon oluştur
    # ChromaDB otomatik olarak varsayılan embedding modelini kullanır
    my_collection = client.create_collection("new_collection")

    # Koleksiyona dokümanlar ekle
    # add() metodu üç temel parametre alır:
    # - documents: Metin dokümanları (otomatik embed edilir)
    # - metadatas: Her doküman için metadata bilgileri
    # - ids: Her doküman için benzersiz kimlik
    my_collection.add(
        # Örnek dokümanlar - laboratuvar deneyleri temalı
        documents=[
            # Doküman 1: Labirent deneyi
            "labirentte peynir arayan hayvanlara yardım ettik", 
            # Doküman 2: Peynir tercihi deneyi
            "deneklerin hepsi aynı peyniri tercih etti", 
            # Doküman 3: Sıçan türü bilgisi
            "deneyde kullanılan sıçanlar aynı türden",
            # Doküman 4: Hayvan sayısı
            "araştırmada on laboratuvar hayvanı kullanıldı",
            # Doküman 5: Tamamen farklı konu - roket bilimi (karşılaştırma için)
            "Zahmetli hesaplamalar sayesinde roketlerin yörünge hızı hesaplanıyor"
            ],
        
        # Her doküman için metadata - kaynak bilgisi    
        metadatas=[
            {"source": "notion"},        # Notion'dan alınmış
            {"source": "google-docs"},   # Google Docs'tan alınmış
            {"source": "txt file"},      # TXT dosyasından
            {"source": "txt file"},      # TXT dosyasından
            {"source": "txt file"}       # TXT dosyasından
            ],
        
        # Benzersiz doküman ID'leri - her ID koleksiyonda tek olmalı
        ids=[
            "doc1", 
            "doc2", 
            "doc3",
            "doc4",
            "doc5"
            ], # must be unique for each doc 
    )

# -----------------------------------------------------------------------------
# BENZERİLİK ARAMASI (QUERY)
# -----------------------------------------------------------------------------

# Koleksiyonda sorgu yap
# query() metodu, verilen metne en benzer dokümanları döndürür
results = my_collection.query(
    query_texts=["deney faresi kullanıldı"],  # Arama sorgusu
    n_results=5,                               # Döndürülecek sonuç sayısı
)

# Sonuçlardan dokümanları ve mesafe (distance) değerlerini çıkar
# results bir dictionary'dir ve şu anahtarları içerir:
# - 'documents': Bulunan dokümanların metinleri (liste içinde liste)
# - 'distances': Her doküman için mesafe skoru (liste içinde liste)
# - 'ids': Doküman ID'leri
# - 'metadatas': Metadata bilgileri
retrieved_docs = results['documents'][0]      # İlk sorgunun dokümanları
retrieved_distances = results['distances'][0]  # İlk sorgunun mesafe değerleri

# -----------------------------------------------------------------------------
# SONUÇLARIN YAZDIRMASI
# -----------------------------------------------------------------------------

# Her dokümanı mesafe skoruyla birlikte yazdır
# Mesafe (distance) değeri:
# - Düşük değer = Daha benzer (daha alakalı)
# - Yüksek değer = Daha farklı (daha az alakalı)
# ChromaDB varsayılan olarak L2 (Euclidean) mesafesi kullanır
for i, doc in enumerate(retrieved_docs):
    print(f"{doc}: {retrieved_distances[i]}")

# =============================================================================
# AÇIKLAMALAR VE ALTERNATİF KULLANIM ÖRNEKLERİ
# =============================================================================

# NOT: Bu dosyayı çalıştırmadan önce, ayrı bir terminalde "chroma run" komutu
# ile ChromaDB sunucusunu başlatmanız gerekir. Sunucu başladığında bu dosyayı
# çalıştırabilirsiniz.

# Alternatif: Python içinde sunucusuz (in-memory veya kalıcı) kullanım da mümkündür:
# chromadb.PersistentClient() - dosya sisteminde kalıcı depolama

# YORUM SATIRLARINA ALINMIŞ ALTERNATİF ÖRNEK:
# Bu örnek, aynı işlemleri İngilizce dokümanlarla gösterir

#Before running this file, first run the "chroma run" command from another terminal. Once server is up you can use this
# python can also run in-memory with no server running: chromadb.PersistentClient()

# import chromadb
# client = chromadb.HttpClient()
# collection = client.create_collection("thenewest_collection")

# # Add docs to the collection. Can also update and delete. Row-based API coming soon!
# collection.add(
#     documents=["You are not alone", "This is document2", "Seasons happen for some reason"], # we embed for you, or bring your own
#     metadatas=[{"source": "notion"}, {"source": "google-docs"}, {"source":"txt file"}], # filter on arbitrary metadata!
#     ids=["doc1", "doc2", "doc3"], # must be unique for each doc 
# )

# results = collection.query(
#     query_texts=["Earth has seasons due to certain factors"],
#     n_results=1,
#     # where={"metadata_field": "is_equal_to_this"}, # optional filter
#     # where_document={"$contains":"search_string"}  # optional filter
# )

# print(results)
# print("*"*100)
# print(f"Distances: {results['distances']}")

# =============================================================================
# CHROMADB HAKKINDA DETAYLI BİLGİ:
# =============================================================================
#
# 1. ÇALIŞMA MODLARI:
#    
#    In-Memory (Geçici):
#    client = chromadb.Client()
#    Avantaj: En hızlı, kurulum gerektirmez
#    Dezavantaj: Program kapanınca veriler silinir
#    
#    Persistent (Kalıcı):
#    client = chromadb.PersistentClient(path="/path/to/persist")
#    Avantaj: Veriler diskte saklanır, sunucu gerektirmez
#    Dezavantaj: Tek process erişimi
#    
#    Client-Server:
#    client = chromadb.HttpClient(host="localhost", port=8000)
#    Avantaj: Çoklu erişim, production ortamı için uygun
#    Dezavantaj: Ayrı sunucu yönetimi gerektirir
#
# 2. MESAFE METRİKLERİ:
#    ChromaDB farklı mesafe metrikleri destekler:
#    - L2 (Euclidean): Varsayılan, geometrik mesafe
#    - IP (Inner Product): Dot product tabanlı
#    - Cosine: Açısal benzerlik
#    
#    collection = client.create_collection(
#        name="my_collection",
#        metadata={"hnsw:space": "cosine"}  # cosine, l2, veya ip
#    )
#
# 3. FİLTRELEME SEÇENEKLERİ:
#    
#    Metadata filtreleme:
#    results = collection.query(
#        query_texts=["sorgu"],
#        where={"source": "notion"}  # Sadece notion'dan gelenler
#    )
#    
#    Doküman içerik filtreleme:
#    results = collection.query(
#        query_texts=["sorgu"],
#        where_document={"$contains": "laboratuvar"}
#    )
#
# 4. EMBEDDİNG FONKSİYONLARI:
#    ChromaDB farklı embedding fonksiyonlarını destekler:
#    - Varsayılan: all-MiniLM-L6-v2 (Sentence Transformers)
#    - OpenAI
#    - Cohere
#    - Özel embedding fonksiyonları
#
# =============================================================================