# =============================================================================
# HyDE (HYPOTHETICAL DOCUMENT EMBEDDINGS) STREAMLIT UYGULAMASI
# Bu dosya, HyDE tekniğini gösteren interaktif bir Streamlit uygulaması oluşturur.
# HyDE, kullanıcı sorusuna hipotetik (kurgusal) bir yanıt oluşturup, bu yanıtı
# arama sorgusu olarak kullanarak daha iyi sonuçlar elde etmeyi hedefler.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# streamlit: İnteraktif web uygulamaları oluşturmak için kullanılır.
import streamlit as st

# hydehelper: Bu proje için özel olarak yazılmış HyDE yardımcı modülü.
# Kurgusal doküman oluşturma ve RAG fonksiyonlarını içerir.
import hydehelper

# -----------------------------------------------------------------------------
# STREAMLIT SAYFA YAPILANDIRMASI
# -----------------------------------------------------------------------------

# Sayfa düzenini geniş (wide) olarak ayarla.
st.set_page_config(layout="wide")

# Sayfa başlığı - HyDE tekniğini açıklayan Türkçe ve İngilizce başlık.
# HyDE: Hypothetical Document Embeddings (Kurgusal Doküman Gömmeleri)
st.title("Advanced RAG: HyDE | Kurgusal Yanıt Üzerinden Bellek Genişletme")

# Görsel ayırıcı çizgi
st.divider()

# -----------------------------------------------------------------------------
# SAYFA DÜZENİ OLUŞTURMA
# -----------------------------------------------------------------------------

# Beş sütunlu düzen oluştur:
# - col_input: Giriş alanları (4 birim genişlik)
# - col_dummy1: Boşluk (1 birim)
# - col_hyde: HyDE sonuçları (8 birim)
# - col_dummy2: Boşluk (1 birim)
# - col_normal: Standart RAG sonuçları (8 birim)
col_input, col_dummy1, col_hyde, col_dummy2, col_normal = st.columns([4,1,8,1,8])

# -----------------------------------------------------------------------------
# GİRİŞ ALANLARI
# -----------------------------------------------------------------------------

with col_input:
    # Web adresi giriş alanı
    # Varsayılan değer: Yapay zeka tehlikeleri hakkında bir makale
    target_url = st.text_input(label="Hedef Web Adresini Giriniz", value="https://cbarkinozer.medium.com/reg%C3%BCle-edilmemi%C5%9F-yapay-zeka-teknolojileri-kullanman%C4%B1n-tehlikeleri-nelerdir-fa465da15491")
    
    # Soru giriş alanı
    # Varsayılan soru: Yapay zeka kullanımının olumsuz etkileri
    original_prompt = st.text_input(label="Sorunuzu Giriniz:", value="Yapay zeka kullanımının yol açabileceği olumsuz durumlar nelerdir?")
    
    # Gönder butonu
    submit_btn = st.button(label="Gönder")
    
    # Görsel ayırıcı
    st.divider()

# İlk boşluk sütunu
with col_dummy1:
    st.empty()

# HyDE sonuçları başlığı
with col_hyde:
    st.subheader("HyDE")
    st.empty()

# İkinci boşluk sütunu
with col_dummy2:
    st.empty()

# Standart RAG sonuçları başlığı
with col_normal:
    st.subheader("Standart RAG")
    st.empty()

# -----------------------------------------------------------------------------
# HyDE VE STANDART RAG KARŞILAŞTIRMASI
# -----------------------------------------------------------------------------

# Gönder butonuna tıklandığında işlemleri başlat
if submit_btn:

    # Hedef URL'den dokümanları yükle ve parçalara ayır.
    # Bu fonksiyon web sayfasını indirir ve chunk'lara böler.
    splitted_documents = hydehelper.load_and_split_documents(target_url=target_url)

    # ==========================================================================
    # HyDE YAKLAŞIMI
    # ==========================================================================
    
    # ADIM 1: Kurgusal (hipotetik) doküman oluştur.
    # LLM'den, soruya cevap verebilecek bir paragraf yazmasını iste.
    # Bu paragraf, gerçek cevabı bilmeden oluşturulan bir "tahmini cevap"tır.
    HyDE_query = hydehelper.generate_hypothetical_document(prompt=original_prompt)

    # Kurgusal yanıtı kullanıcıya göster
    col_input.subheader("Kurgusal Yanıt:")
    col_input.info(HyDE_query)

    # ADIM 2: Kurgusal yanıtı arama sorgusu olarak kullan.
    # Orijinal soru yerine, üretilen kurgusal yanıtla arama yap.
    # Bu yaklaşım, sorgu ve doküman arasındaki "semantik boşluğu" azaltır.
    relevant_documents = hydehelper.get_relevant_documents(prompt=HyDE_query, documents=splitted_documents)

    # ADIM 3: Bulunan dokümanları kullanarak gerçek yanıt üret.
    # Orijinal soruyu ve bulunan bağlamı birleştirerek LLM'den yanıt al.
    AI_Response = hydehelper.run_rag(relevant_documents=relevant_documents, prompt=original_prompt)
    
    # HyDE sonuçlarını göster
    col_hyde.info(AI_Response)  # AI yanıtı
    col_hyde.divider()
    
    # HyDE ile bulunan dokümanları listele
    for rel_doc in relevant_documents:
        col_hyde.info(f"{rel_doc.metadata['doc_id']} || {rel_doc.page_content}")
    
    # ==========================================================================
    # STANDART RAG YAKLAŞIMI (KARŞILAŞTIRMA İÇİN)
    # ==========================================================================
    
    # Standart RAG: Orijinal soruyu doğrudan arama sorgusu olarak kullan.
    # Bu, geleneksel yaklaşımdır - soru vektörü ile doküman vektörleri karşılaştırılır.
    relevant_documents_normal = hydehelper.get_relevant_documents(prompt=original_prompt, documents=splitted_documents)

    # Standart RAG ile yanıt üret
    AI_Response_normal = hydehelper.run_rag(relevant_documents=relevant_documents_normal, prompt=original_prompt)    

    # Standart RAG sonuçlarını göster
    col_normal.success(AI_Response_normal)  # AI yanıtı
    col_normal.divider()
    
    # Standart RAG ile bulunan dokümanları listele
    for rel_doc_n in relevant_documents_normal:
        col_normal.success(f"{rel_doc_n.metadata['doc_id']} || {rel_doc_n.page_content}")
    
# =============================================================================
# HyDE TEKNİĞİ AÇIKLAMASI:
# =============================================================================
# 
# HyDE (Hypothetical Document Embeddings) Nasıl Çalışır?
# 
# 1. PROBLEM:
#    - Kullanıcı sorusu ile doküman içeriği farklı "dillerde" yazılmıştır
#    - Soru: "X nedir?" formatında
#    - Doküman: "X, şu şekilde tanımlanır..." formatında
#    - Bu farklılık, embedding benzerliğini azaltır
#
# 2. ÇÖZÜM:
#    - LLM'den, soruya cevap verebilecek bir "tahmini doküman" oluşturmasını iste
#    - Bu tahmini doküman, gerçek dokümanlara daha benzer formattadır
#    - Tahmini dokümanın embedding'i ile arama yap
#
# 3. AVANTAJLAR:
#    - Sorgu ve doküman arasındaki format farkını ortadan kaldırır
#    - Daha alakalı sonuçlar getirir
#    - Özellikle karmaşık sorularda etkilidir
#
# 4. DEZAVANTAJLAR:
#    - Ek bir LLM çağrısı gerektirir (maliyet ve gecikme)
#    - Kurgusal yanıt yanlış olabilir
#    - Her durum için uygun olmayabilir
#
# =============================================================================
