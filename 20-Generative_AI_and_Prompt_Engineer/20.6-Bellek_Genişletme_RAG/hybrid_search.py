# =============================================================================
# HİBRİT ARAMA (HYBRID SEARCH) STREAMLIT UYGULAMASI
# Bu dosya, BM25 (anahtar kelime bazlı) ve semantik aramanın birleştirildiği
# hibrit arama yöntemini gösteren interaktif bir Streamlit uygulaması oluşturur.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# streamlit: Python ile hızlı ve kolay web uygulamaları oluşturmak için kullanılır.
# Veri bilimi ve makine öğrenimi uygulamaları için popüler bir framework'tür.
import streamlit as st

# hybridhelper: Bu proje için özel olarak yazılmış yardımcı modül.
# BM25 ve FAISS retriever'larını, hibrit arama fonksiyonlarını içerir.
import hybridhelper

# -----------------------------------------------------------------------------
# STREAMLIT SAYFA YAPILANDIRMASI
# -----------------------------------------------------------------------------

# Sayfa düzenini geniş (wide) olarak ayarla.
# Bu ayar, içeriğin tüm ekran genişliğini kullanmasını sağlar.
st.set_page_config(layout="wide")

# Sayfa başlığını ayarla.
# İngilizce ve Türkçe olarak hem konuyu hem de yöntemi açıklar.
st.title("Advanced RAG: Hybrid Search | Hibrit Arama")

# Görsel ayırıcı çizgi ekle
st.divider()

# -----------------------------------------------------------------------------
# GİRİŞ ALANI DÜZENİ
# -----------------------------------------------------------------------------

# Üç sütunlu bir düzen oluştur: sol boşluk, giriş alanı, sağ boşluk.
# Bu düzen, giriş alanını sayfa ortasına konumlandırır.
col_left, col_input, col_right = st.columns(3)

# Sol sütun - boş bırakılıyor (görsel denge için)
with col_left:
    st.empty()

# Orta sütun - kullanıcı giriş alanları
with col_input:
    # Web adresi giriş alanı.
    # Varsayılan değer olarak yapay zeka tehlikeleri hakkında bir Medium makalesi kullanılıyor.
    target_url = st.text_input(label="Hedef Web Adresini Giriniz", value="https://cbarkinozer.medium.com/reg%C3%BCle-edilmemi%C5%9F-yapay-zeka-teknolojileri-kullanman%C4%B1n-tehlikeleri-nelerdir-fa465da15491")
    
    # Kullanıcı sorusu giriş alanı.
    # Varsayılan soru: Yapay zeka ile ilgili sorunlara yönelik aksiyonlar.
    original_prompt = st.text_input(label="Sorunuzu Giriniz:", value="Yapay zekayla ilgili muhtemel sorunları çözmek için yapılabilecek aksiyonlar nelerdir?")
    
    # Ağırlık seçenekleri listesi.
    # Bu seçenekler, BM25 ve semantik arama arasındaki dengeyi belirler.
    weight_options = ["%90 Karakter Bazlı", "%75 Karakter Bazlı", "%50 - %50", "%75 Semantik Bazlı", "%90 Semantik Bazlı"]
    
    # Kaydırıcı (slider) ile ağırlık seçimi.
    # Kullanıcı, arama yöntemlerinin ağırlıklarını görsel olarak ayarlayabilir.
    retriever_weight = st.select_slider(label="Arama Yöntemlerinini Ağırlıklarını Belirleyin:", options=weight_options, value="%50 - %50")
    
    # Gönder butonu
    submit_btn = st.button(label="Gönder")
    
    # Görsel ayırıcı
    st.divider()

# Sağ sütun - boş bırakılıyor (görsel denge için)
with col_right:
    st.empty()

# -----------------------------------------------------------------------------
# SONUÇ ALANI DÜZENİ
# -----------------------------------------------------------------------------

# Üç sütunlu sonuç düzeni: Karakter bazlı, Hibrit, Semantik
col_keyword, col_hybrid, col_semantic = st.columns(3)

# Sol sütun - BM25 (anahtar kelime bazlı) arama sonuçları başlığı
with col_keyword:
    # BM25: Best Matching 25 algoritması
    # Klasik bilgi getirme algoritmasıdır, TF-IDF'in geliştirilmiş versiyonudur.
    st.subheader("Karakter Bazlı Arama | BM25")
    st.divider()

# Orta sütun - Hibrit arama sonuçları başlığı
with col_hybrid:
    # Hibrit arama, her iki yöntemin avantajlarını birleştirir.
    st.subheader("Hibrit Arama")
    st.divider()

# Sağ sütun - Semantik arama sonuçları başlığı
with col_semantic:
    # Semantik arama, kelimelerin anlamsal benzerliğini kullanır.
    st.subheader("Semantik Arama")
    st.divider()

# -----------------------------------------------------------------------------
# ARAMA İŞLEMLERİ (BUTON TIKLANDIĞINDA)
# -----------------------------------------------------------------------------

# Gönder butonuna tıklandığında arama işlemlerini başlat
if submit_btn:

    # Hedef URL'den dokümanları yükle ve parçalara ayır.
    # Bu fonksiyon, web sayfasını indirir, metni çıkarır ve chunk'lara böler.
    initial_documents = hybridhelper.load_and_split_documents(target_url=target_url)

    # BM25 algoritması ile anahtar kelime bazlı arama yap.
    # BM25, kelime frekanslarına dayalı klasik bir bilgi getirme algoritmasıdır.
    # Döndürülen değerler: bulunan dokümanlar ve BM25 retriever nesnesi
    bm25_documents, bm25retriever = hybridhelper.get_relevant_documents_with_bm25(documents=initial_documents, query=original_prompt)

    # FAISS ile semantik (vektör bazlı) arama yap.
    # FAISS, metinlerin anlamsal temsillerini kullanarak benzerlik araması yapar.
    # Döndürülen değerler: bulunan dokümanlar ve FAISS retriever nesnesi
    faiss_documents, faissretriever = hybridhelper.get_relevant_documents_with_FAISS(documents=initial_documents, query=original_prompt)

    # Kullanıcının seçtiği ağırlık değerini sayısal değere dönüştür.
    # weight1: BM25 (karakter bazlı) aramanın ağırlığı
    # weight2: FAISS (semantik) aramanın ağırlığı (1 - weight1)
    weight1 = 0.5  # Varsayılan değer: %50-%50 dengeli
    
    # Kullanıcı seçimine göre ağırlığı belirle
    if retriever_weight == "%90 Karakter Bazlı":
        weight1 = 0.9  # BM25'e %90 ağırlık
    elif retriever_weight == "%75 Karakter Bazlı":
        weight1 = 0.75  # BM25'e %75 ağırlık
    elif retriever_weight == "%50 - %50 Dengeli":
        weight1 = 0.5  # Dengeli dağılım
    elif retriever_weight == "%75 Semantik Bazlı":
        weight1 = 0.25  # Semantik aramaya %75 ağırlık
    elif retriever_weight == "%90 Semantik Bazlı":
        weight1 = 0.1  # Semantik aramaya %90 ağırlık

    # Hibrit arama yap - her iki yöntemi belirlenen ağırlıklarla birleştir.
    # EnsembleRetriever, birden fazla retriever'ın sonuçlarını ağırlıklı olarak birleştirir.
    hybrid_search_documents = hybridhelper.get_relevant_documents_for_hybrid_search(
                                                        query=original_prompt, 
                                                        retriever1=bm25retriever,  # BM25 retriever
                                                        retriever2=faissretriever, # FAISS retriever
                                                        weight1=weight1,           # BM25 ağırlığı
                                                        weight2=1-weight1          # FAISS ağırlığı (tamamlayıcı)
                                                        )
    
    # -----------------------------------------------------------------------------
    # SONUÇLARIN GÖRÜNTÜLENMESİ
    # -----------------------------------------------------------------------------
    
    # BM25 ile bulunan dokümanları sarı uyarı kutusunda göster.
    # Her doküman için ID ve içerik bilgisi görüntülenir.
    for keyword_doc in bm25_documents:
        col_keyword.warning(f"ID: {keyword_doc.metadata['doc_id']} || {keyword_doc.page_content}")
    
    # FAISS (semantik) ile bulunan dokümanları mavi bilgi kutusunda göster.
    for faiss_doc in faiss_documents:
        col_semantic.info(f"ID: {faiss_doc.metadata['doc_id']} || {faiss_doc.page_content}")

    # Hibrit arama sonuçlarını yeşil başarı kutusunda göster.
    # Bu sonuçlar, her iki yöntemin ağırlıklı birleşimidir.
    for hybrid_doc in hybrid_search_documents:
        col_hybrid.success(f"ID: {hybrid_doc.metadata['doc_id']} || {hybrid_doc.page_content}")

# =============================================================================
# HİBRİT ARAMA AÇIKLAMASI:
# =============================================================================
# Hibrit arama, iki farklı arama paradigmasını birleştirir:
#
# 1. BM25 (Lexical/Keyword Search):
#    - Kelime eşleşmelerine dayalı klasik arama
#    - Tam kelime eşleşmelerinde güçlü
#    - Eşanlamlıları veya anlamsal benzerlikleri yakalayamaz
#
# 2. Semantik Arama (Dense Retrieval):
#    - Vektör embedding'lerine dayalı arama
#    - Anlamsal benzerlikleri yakalar
#    - Bazen spesifik anahtar kelimeleri kaçırabilir
#
# Hibrit yaklaşım:
# - Her iki yöntemin güçlü yönlerini birleştirir
# - Hem kelime eşleşmelerini hem de anlamsal benzerlikleri yakalar
# - Daha kapsamlı ve doğru sonuçlar sağlar
# =============================================================================