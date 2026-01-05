# =============================================================================
# MULTI-QUERY RAG (SORGU ÇEŞİTLENDİRME) STREAMLIT UYGULAMASI
# Bu dosya, tek bir kullanıcı sorusundan birden fazla arama sorgusu üreterek
# daha kapsamlı sonuçlar elde eden gelişmiş RAG tekniğini gösterir.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# streamlit: İnteraktif web uygulamaları oluşturmak için kullanılır.
# Veri bilimi ve ML uygulamaları için popüler bir Python framework'üdür.
import streamlit as st

# multiqueryhelper: Bu proje için özel olarak yazılmış yardımcı modül.
# Çoklu sorgu oluşturma, doküman getirme ve reranking fonksiyonlarını içerir.
import multiqueryhelper

# -----------------------------------------------------------------------------
# STREAMLIT SAYFA YAPILANDIRMASI
# -----------------------------------------------------------------------------

# Sayfa düzenini geniş (wide) olarak ayarla - daha fazla içerik gösterimi için.
st.set_page_config(layout="wide")

# Sayfa başlığı - Multi-Query tekniğini açıklayan bilgilendirici başlık.
st.title("Advanced RAG: Multi-Query | Sorgu Çeşitlendirme ile Bellek Genişletme Örneği")

# Görsel ayırıcı çizgi
st.divider()

# -----------------------------------------------------------------------------
# SAYFA DÜZENİ - BEŞ SÜTUNLU YAPI
# -----------------------------------------------------------------------------

# Beş sütunlu düzen oluştur - her biri farklı işlev için:
# - col_input: Giriş alanları (1 birim)
# - col_docs: Tüm getirilen dokümanlar (2 birim)
# - col_uniquedocs: Benzersiz dokümanlar (2 birim)
# - col_rerankeddocs: Yeniden sıralanmış dokümanlar (2 birim)
# - col_response: Final AI yanıtı (1 birim)
col_input, col_docs, col_uniquedocs, col_rerankeddocs, col_response = st.columns([1,2,2,2,1])

# -----------------------------------------------------------------------------
# GİRİŞ ALANI YAPISI
# -----------------------------------------------------------------------------

with col_input:
    # Web adresi giriş alanı
    # Varsayılan değer: Yapay zeka tehlikeleri hakkında bir makale
    target_url = st.text_input(label="Hedef Web Adresini Giriniz", value="https://cbarkinozer.medium.com/reg%C3%BCle-edilmemi%C5%9F-yapay-zeka-teknolojileri-kullanman%C4%B1n-tehlikeleri-nelerdir-fa465da15491")
    
    # Kullanıcı sorusu giriş alanı
    original_prompt = st.text_input(label="Sorunuzu Giriniz:", value="Yapay zeka kullanımının yol açabileceği olumsuz durumlar nelerdir?")
    
    # Sorguyu gönder butonu
    submit_btn = st.button(label="Gönder")
    
    # Görsel ayırıcı
    st.divider()

# Diğer sütunlar başlangıçta boş - sonuçlar geldikçe doldurulacak
with col_docs:
    st.empty()

with col_uniquedocs:
    st.empty()

with col_rerankeddocs:
    st.empty()

with col_response:
    st.empty()

# -----------------------------------------------------------------------------
# MULTI-QUERY RAG PIPELINE'I
# -----------------------------------------------------------------------------

# Gönder butonuna tıklandığında tüm işlem zincirini başlat
if submit_btn:

    # =========================================================================
    # ADIM 1: ÇOKlu SORGU OLUŞTURMA
    # =========================================================================
    
    # Spinner ile kullanıcıya işlemin devam ettiğini göster
    with st.spinner("Soru havuzu oluşturuluyor..."):
        # Orijinal sorudan birden fazla alternatif sorgu üret.
        # Bu, LLM kullanarak yapılır - farklı bakış açılarından soru varyasyonları oluşturulur.
        # Örnek: "Yapay zeka tehlikeleri nelerdir?" sorusundan:
        # - "Yapay zeka riskleri nelerdir?"
        # - "AI'ın olumsuz etkileri nedir?"
        # - "Makine öğrenmesinin potansiyel zararları nelerdir?"
        #Generate alternative queries and show
        query_list = multiqueryhelper.generate_multi_query(original_prompt=original_prompt)

        # Oluşturulan soru havuzunu göster
        col_input.markdown("SORU HAVUZU")
        st.divider()
        
        # Her bir alternatif soruyu listele
        for query in query_list:
            col_input.markdown(f"**{query}**")
    
    # =========================================================================
    # ADIM 2: HER SORGU İÇİN DOKÜMAN GETİRME
    # =========================================================================
    
    # Tüm sorgulardan bulunan dokümanları toplamak için liste
    #Get relevant documents for each query and show
    retrieved_documents = []

    # Her bir sorgu için ayrı ayrı doküman getir
    for query in query_list:
        # Bu sorgu için en alakalı dokümanları bul
        relevant_documents = multiqueryhelper.get_relevant_documents(target_url=target_url, prompt=query)

        # Bulunan dokümanları genel listeye ekle
        # extend() kullanarak tüm dokümanları tek bir listeye birleştir
        retrieved_documents.extend(relevant_documents)
    
    # Toplam bulunan doküman sayısını göster
    # Not: Bu sayıda tekrarlar olabilir (aynı doküman farklı sorgularla bulunmuş olabilir)
    col_docs.code(f"Bulunan Doküman Sayısı: {len(retrieved_documents)}")

    # Tüm bulunan dokümanları kırmızı uyarı kutularında göster
    for retrieved_doc in retrieved_documents:
        col_docs.error(f"ID: {retrieved_doc.metadata['doc_id']} | {retrieved_doc.page_content}")
    
    # =========================================================================
    # ADIM 3: TEKRARLAYAN DOKÜMANLARI KALDIRMA (DE-DUPLICATION)
    # =========================================================================
    
    # Tekrarlayan dokümanları filtrele - yalnızca benzersiz dokümanları tut.
    # Farklı sorgular aynı dokümanı bulabilir, bu tekrarları kaldırıyoruz.
    #Get unique documents out of all retrieved documents and show
    final_documents = multiqueryhelper.get_unique_documents(retrieved_documents=retrieved_documents)

    # Benzersiz doküman sayısını göster
    col_uniquedocs.code(f"Bulunan Özgün Doküman Sayısı: {len(final_documents)}")

    # Benzersiz dokümanları sarı uyarı kutularında göster
    for final_doc in final_documents:
        col_uniquedocs.warning(f"ID: {final_doc.metadata['doc_id']} | {final_doc.page_content}")
    
    # =========================================================================
    # ADIM 4: DOKÜMANLARI YENİDEN SIRALAMA (RERANKING)
    # =========================================================================
    
    # Cohere'in rerank modelini kullanarak dokümanları orijinal soruya göre yeniden sırala.
    # Bu adım, semantik aramadan daha hassas bir sıralama sağlar.
    # Cross-encoder modeli kullanılarak her doküman-soru çifti değerlendirilir.
    #Get reranked documents and show
    reranked_docs = multiqueryhelper.get_reranked_documents(documents=final_documents, query=original_prompt)

    # Yeniden sıralanmış doküman sayısını göster
    col_rerankeddocs.code(f"Yeniden Sıralanmış Doküman Sayısı: {len(reranked_docs)}")

    # Yeniden sıralanmış dokümanları mavi bilgi kutularında göster
    for reranked_doc in reranked_docs:
        col_rerankeddocs.info(f"ID: {reranked_doc.metadata['doc_id']} | {reranked_doc.page_content}")
    
    # =========================================================================
    # ADIM 5: FİNAL YANIT ÜRETME
    # =========================================================================
    
    # Yeniden sıralanmış en alakalı dokümanları kullanarak final yanıt üret.
    # RAG: Dokümanlar bağlam olarak kullanılır, LLM bu bağlamla yanıt oluşturur.
    #Get AI response and show
    AI_Response  = multiqueryhelper.run_rag(relevant_documents=reranked_docs, prompt=original_prompt)
    
    # Final yanıtı yeşil başarı kutusunda göster
    col_response.code("NİHAİ YANIT")
    col_response.success(AI_Response)

# =============================================================================
# MULTI-QUERY RAG TEKNİĞİ AÇIKLAMASI:
# =============================================================================
#
# PROBLEM:
# - Tek bir arama sorgusu, tüm alakalı dokümanları bulamayabilir
# - Kullanıcının soru formülasyonu, doküman içeriğiyle tam eşleşmeyebilir
# - Semantik arama, farklı ifadelerden aynı anlama ulaşmakta zorlanabilir
#
# ÇÖZÜM - MULTI-QUERY YAKLAŞIMI:
# 
# 1. SORGU ÇEŞİTLENDİRME:
#    - Orijinal sorudan LLM ile alternatif sorgular üret
#    - Farklı kelimeler, farklı bakış açıları kullan
#    - Soru havuzu oluştur
#
# 2. PARALEL ARAMA:
#    - Her sorgu için ayrı ayrı doküman getir
#    - Tüm sonuçları birleştir
#    - Daha geniş bir doküman havuzu elde et
#
# 3. DE-DUPLIKASYON:
#    - Tekrarlayan dokümanları kaldır
#    - Benzersiz ID'lere göre filtrele
#
# 4. RERANKING:
#    - Cross-encoder modeli ile hassas sıralama
#    - Orijinal soruya en alakalı dokümanları üste taşı
#
# 5. YANIT ÜRETME:
#    - En alakalı dokümanları bağlam olarak kullan
#    - LLM ile kapsamlı yanıt oluştur
#
# AVANTAJLAR:
# - Daha kapsamlı arama
# - Kelime mismatch problemini azaltır
# - Yüksek kaliteli sonuçlar
#
# DEZAVANTAJLAR:
# - Daha fazla API çağrısı (maliyet)
# - Artan gecikme süresi
# - Kompleks pipeline
#
# =============================================================================
