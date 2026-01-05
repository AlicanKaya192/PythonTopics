# =============================================================================
# COHERE İLE YENİDEN SIRALAMA (RERANKING) STREAMLIT UYGULAMASI
# Bu dosya, Cohere'in rerank modelini kullanarak dokümanları
# alakalılık skorlarına göre yeniden sıralayan interaktif bir uygulama oluşturur.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# streamlit: İnteraktif web uygulamaları oluşturmak için kullanılır.
import streamlit as st

# cohere: Cohere AI platformunun Python SDK'sı.
# NLP görevleri ve özellikle reranking için güçlü modeller sunar.
import cohere

# os: İşletim sistemi işlemleri için
import os

# dotenv: .env dosyasından API anahtarlarını güvenli şekilde yükler.
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# ORTAM DEĞİŞKENLERİNİN YÜKLENMESİ
# -----------------------------------------------------------------------------

# .env dosyasındaki gizli değişkenleri yükle.
load_dotenv()

# Cohere API anahtarını ortam değişkenlerinden al.
my_key_cohere = os.getenv("cohere_apikey")

# Cohere client'ı oluştur - API ile iletişim için kullanılacak.
cohere_client = cohere.Client(api_key=my_key_cohere)

# -----------------------------------------------------------------------------
# ÖRNEK VERİ SETİ
# -----------------------------------------------------------------------------

# Arama sorgusu: Türkiye'nin başkenti hakkında
query = "Türkiye'nin başkenti neresidir?"

# Örnek doküman listesi - farklı alaka seviyelerinde cümleler.
# Bu dokümanlar, reranking'in etkisini görmek için tasarlanmıştır.
documents = [
   # Dolaylı olarak alakalı - turizm bağlamında Ankara
   "Ankara, Türkiye'nin başlıca turistik lokasyonlarından biridir ve her yıl beş milyondan fazla turist ev sahipliği yapar.",
   
   # Yanlış eşleşme potansiyeli - "Başkent" kelimesi var ama farklı anlam
   "Genç adam Başkent Üniversitesi'nde bilgisayar mühendisliği bölümüne yerleştiği için son derece heyecanlıydı.",
   
   # Alakasız - Türkiye hakkında ama başkent değil
   "Orta kuşak ikliminin özelliklerini gösteren Türkiye, dünya üzerinde dört mevsimi birden yaşayan şanslı coğrafyalardan biridir.",
   
   # DOĞRUDAN ALAKALI - Tam cevap
   "Türkiye'nin başkenti Ankara'dır",
   
   # Dolaylı alakalı - tarihsel bağlam
   "Yahya Kemal bir şiirinde Ankara'nın en çok İstanbul'a dönüş yolunu sevdim diyordu ama o sıralar eski bir başkent olarak bugünkü kaotik metropol havasından uzaktı.",
   
   # Tarihi bağlam - başkentin değişmesi
   "Cumhuriyetin ilanı ile birlikte yaşanan önemli değişikliklerden biri de başkentin yer değiştirerek Ankara'ya taşınmış olmasıydı.",
   
   # Tarihi bağlam - başkent seçimi süreci
   "Başkentin neresi olması gerektiğiyle ilgili tartışmalar sürerken, güvenli ve merkezi bir lokasyon aranıyordu tıpkı Ankara gibi.",
   
   # Tamamen alakasız - bilim konusu
   "Elektromanyetizmayla ilgili çalışmalarıyla ünlenen Maxwell, Einstein gibi pek çok bilim adamına da ilham olmuştu.",
   
   # Dolaylı alakalı - Ankara'nın ilçeleri
   "Ankara'nın başlıca ilçeleri Çankaya, Yenimahalle ve Keçiören'dir diyebiliriz.",
   
   # Alakasız - kentleşme konusu
   "Kentleşme, ülkemizde geç başlamış ve sancıları halen devam etmekte olan bir sosyolojik süreçtir.",
   
   # Alakalı - kar yağışı haberi ama Başkent Ankara vurgusu
   "Başkent Ankara'da yılın ilk kar yağışının keyfini yine çocuklar çıkardı.",
   
   # DOĞRUDAN ALAKALI - Resmi bilgi
   "Türkiye Cumhuriyeti devletinin resmi başkenti olan Ankara şehri İç Anadolu bölgesinde yer alır."
   ]

# -----------------------------------------------------------------------------
# STREAMLIT SAYFA YAPILANDIRMASI
# -----------------------------------------------------------------------------

# Sayfa düzenini geniş olarak ayarla.
st.set_page_config(layout="wide")

# Sayfa başlığı - Reranking tekniğini açıklayan bilgilendirici başlık.
st.title("Advanced RAG: Reranking | Yeniden Sıralama")

# Görsel ayırıcı
st.divider()

# -----------------------------------------------------------------------------
# BUTON ALANI DÜZENİ
# -----------------------------------------------------------------------------

# Üç sütunlu düzen - ortada geniş buton
col_left, col_input, col_right = st.columns([1,8,1])

# Sol boşluk
with col_left:
    st.empty()

# Ortada yeniden sıralama butonu   
with col_input:
    # Tam genişlikte buton oluştur
    submit_btn = st.button(label="Yeniden Sırala",use_container_width=True)

# Sağ boşluk
with col_right:
    st.empty()

# -----------------------------------------------------------------------------
# SONUÇ ALANI DÜZENİ
# -----------------------------------------------------------------------------

# İki ana sütun: orijinal sıra ve yeniden sıralanmış sonuçlar
col_original, col_dummy, col_reranked = st.columns([9,1,9])

# Orijinal sıralamayı göster (her zaman görünür)
with col_original:
    st.subheader("Orijinal Sırayla Dokümanlar")
    # Her dokümanı mavi bilgi kutusu olarak göster
    for doc in documents:
        st.info(doc)

# Ortada boşluk (görsel ayırıcı)
with col_dummy:
    st.empty()

# Yeniden sıralanmış sonuçlar başlığı
with col_reranked:
    st.subheader("Yeniden Sıralanmış Dokümanlar")

# -----------------------------------------------------------------------------
# RERANKING İŞLEMİ
# -----------------------------------------------------------------------------

# Buton tıklandığında reranking işlemini gerçekleştir
if submit_btn:
    
   # Cohere rerank API'sini çağır.
   # Bu API, dokümanları sorguya göre alakalılık skorlarına göre sıralar.
   results = cohere_client.rerank(
       query=query,                           # Sıralama kriteri olarak sorgu
       documents=documents,                   # Sıralanacak dokümanlar
       top_n=12,                              # Tüm dokümanları döndür (12 doküman var)
       model="rerank-multilingual-v2.0"       # Çok dilli rerank modeli
   )

   # Yeniden sıralanmış sonuçları göster
   for result in results:
      # Her sonuç için:
      # - result.document['text']: Doküman metni
      # - result.relevance_score: Alakalılık skoru (0-1 arası)
      # - result.index: Orijinal listedeki sıra (0-indexed, +1 ile 1-indexed)
      col_reranked.success(f"{result.document['text']}   ||   {result.relevance_score} || #Sıra {result.index+1}")

# =============================================================================
# RERANKING TEKNİĞİ AÇIKLAMASI:
# =============================================================================
#
# 1. RERANKING NEDİR?
#    - İlk arama sonuçlarını daha hassas bir modelle yeniden sıralama
#    - İki aşamalı retrieval stratejisi:
#      1. İlk aşama: Hızlı ama daha az hassas (bi-encoder)
#      2. İkinci aşama: Yavaş ama çok hassas (cross-encoder/reranker)
#
# 2. Bİ-ENCODER VS CROSS-ENCODER:
#    
#    Bi-encoder (Embedding tabanlı arama):
#    - Sorgu ve doküman ayrı ayrı encode edilir
#    - Sonra vektörler karşılaştırılır
#    - Çok hızlı (milyonlarca doküman aranabilir)
#    - Daha az hassas
#    
#    Cross-encoder (Reranker):
#    - Sorgu ve doküman BİRLİKTE işlenir
#    - Daha derin bağlamsal anlama
#    - Çok yavaş (sadece yüzlerce doküman)
#    - Çok hassas
#
# 3. COHERE RERANK MODELİ:
#    - rerank-multilingual-v2.0: 100+ dil desteği
#    - Türkçe için optimize edilmiş
#    - Cross-encoder mimarisi kullanır
#    - 0-1 arası relevance_score döndürür
#
# 4. KULLANIM SENARYOLARI:
#    - RAG sistemlerinde sonuç kalitesini artırma
#    - Arama motorlarında sıralamayı iyileştirme
#    - Müşteri destek sistemlerinde doğru cevapları öne çıkarma
#    - E-ticaret ürün aramalarında
#
# 5. ÖRNEKTEKİ BEKLENEN SONUÇLAR:
#    Yüksek skor: "Türkiye'nin başkenti Ankara'dır"
#    Yüksek skor: "...resmi başkenti olan Ankara şehri..."
#    Orta skor: Tarihsel başkent referansları
#    Düşük skor: Alakasız konular (Maxwell, kentleşme vb.)
#
# =============================================================================