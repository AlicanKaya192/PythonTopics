# =============================================================================
# MMR (MAXIMUM MARGINAL RELEVANCE) ARAMA ÖRNEĞİ
# Bu dosya, ChromaDB vektör veritabanı kullanarak MMR arama yöntemini gösterir.
# MMR, hem alakalı hem de çeşitli sonuçlar döndürerek bilgi tekrarını azaltır.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# Chroma: Açık kaynaklı bir vektör veritabanıdır.
# Embedding vektörlerini saklar ve benzerlik aramaları yapar.
# MMR gibi gelişmiş arama yöntemlerini destekler.
from langchain_community.vectorstores.chroma import Chroma

# OpenAIEmbeddings: OpenAI'nin text-embedding modelini kullanarak metinleri vektörlere dönüştürür.
# Bu vektörler, metinlerin anlamsal temsilini oluşturur.
from langchain_openai import OpenAIEmbeddings

# os: İşletim sistemi işlemleri için (ortam değişkenleri okuma vb.)
import os

# dotenv: .env dosyasından API anahtarlarını güvenli bir şekilde yükler.
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# ORTAM DEĞİŞKENLERİNİN YÜKLENMESİ
# -----------------------------------------------------------------------------

# .env dosyasındaki gizli değişkenleri ortam değişkeni olarak yükle.
load_dotenv()

# OpenAI API anahtarını ortam değişkenlerinden al.
# Bu anahtar, embedding modeli için gereklidir.
my_key_openai = os.getenv("openai_apikey")

# OpenAI embedding modelini yapılandır.
# Bu model, metinleri yüksek boyutlu vektörlere dönüştürür.
embeddings = OpenAIEmbeddings(api_key=my_key_openai)

# -----------------------------------------------------------------------------
# ÖRNEK DOKÜMAN VERİ SETİ
# -----------------------------------------------------------------------------

# Benzerlik araması için kullanılacak örnek dokümanlar.
# İlk 4 doküman laboratuvar hayvanları ve deneylerle ilgili (semantik olarak benzer).
# Son doküman tamamen farklı bir konuda (roket yörüngesi).
documents=[
            # Doküman 1: Labirent deneyi - hayvan davranışı
            "labirentte peynir arayan hayvanlara yardım ettik", 
            # Doküman 2: Peynir tercihi - denek davranışı  
            "deneklerin hepsi aynı peyniri tercih etti", 
            # Doküman 3: Sıçan türü - hayvan bilgisi
            "deneyde kullanılan sıçanlar aynı türden",
            # Doküman 4: Laboratuvar hayvanı sayısı
            "araştırmada on laboratuvar hayvanı kullanıldı",
            # Doküman 5: Farklı konu - roket bilimi (çeşitlilik kontrolü için)
            "Zahmetli hesaplamalar sayesinde roketlerin yörünge hızı hesaplanıyor"
            ]

# Arama sorgusu: "Deney faresi kullanıldı"
# Bu sorgu, laboratuvar hayvanları hakkındaki dokümanlarla eşleşmeli.
query = "deney faresi kullanıldı"

# -----------------------------------------------------------------------------
# CHROMA VEKTÖR VERİTABANI OLUŞTURMA
# -----------------------------------------------------------------------------

# Dokümanlardan ChromaDB vektör veritabanı oluştur.
# Bu adımda her doküman için embedding vektörü hesaplanır ve saklanır.
# from_texts() metodu, basit metin listelerinden vektör deposu oluşturur.
vectorstore = Chroma.from_texts(documents, embeddings)

# -----------------------------------------------------------------------------
# YÖNTEM 1: DOĞRUDAN VEKTÖR DEPOSUNDAN MMR ARAMA
# -----------------------------------------------------------------------------

# max_marginal_relevance_search() metodunu kullanarak MMR araması yap.
# MMR (Maximum Marginal Relevance) algoritması:
# - İlk olarak en alakalı dokümanı seçer
# - Sonraki dokümanlarda hem alaka hem de çeşitlilik kriterini dengeler
# - Bu sayede birbirine çok benzer sonuçların tekrarlanmasını önler
#Method1 - directly from the vectorstore
relevant_documents_vs = vectorstore.max_marginal_relevance_search(query)

# -----------------------------------------------------------------------------
# YÖNTEM 2: RETRİEVER ÜZERİNDEN MMR ARAMA
# -----------------------------------------------------------------------------

# Vektör deposundan bir retriever (getirici) oluştur.
# search_type="mmr" parametresi, MMR algoritmasını kullanmasını sağlar.
# Retriever yaklaşımı, LangChain zincirleriyle entegrasyon için daha uygundur.
#Method2 - using a retriever
retriever = vectorstore.as_retriever(search_type="mmr") 

# Retriever'ı kullanarak MMR araması yap.
# get_relevant_documents() metodu, sorguya en uygun dokümanları döndürür.
relevant_documents_rt = retriever.get_relevant_documents(query)

# -----------------------------------------------------------------------------
# SONUÇLARIN KARŞILAŞTIRILMASI
# -----------------------------------------------------------------------------

# Yöntem 1'in sonuçlarını yazdır (doğrudan vektör deposundan)
print("Doğrudan MMR ile Elde Edilen Dokümanlar:")
print("*"*100)

# Her bir bulunan dokümanın içeriğini yazdır
for doc in relevant_documents_vs:
    print(doc.page_content)

# Görsel ayırıcı
print("-"*90)

# Yöntem 2'nin sonuçlarını yazdır (retriever üzerinden)
print("Retriever Üzerinden Elde Edilen Dokümanlar:")
print("*"*100)

# Her bir bulunan dokümanın içeriğini yazdır
for doc in relevant_documents_rt:
    print(doc.page_content)


# =============================================================================
# MMR ALGORİTMASI HAKKINDA AÇIKLAMA:
# =============================================================================
# MMR, bilgi getirme sistemlerinde çeşitlilik sağlamak için kullanılır.
# 
# Formül: MMR = argmax [λ * Sim(di, Q) - (1-λ) * max(Sim(di, dj))]
# 
# Burada:
# - λ (lambda): Alaka ve çeşitlilik arasındaki dengeyi kontrol eder
# - Sim(di, Q): Doküman di ile sorgu Q arasındaki benzerlik
# - Sim(di, dj): Doküman di ile zaten seçilmiş dokümanlar arasındaki benzerlik
#
# Avantajları:
# 1. Bilgi tekrarını azaltır
# 2. Daha geniş bir perspektif sunar
# 3. Kullanıcıya çeşitli bilgiler sağlar
# =============================================================================
