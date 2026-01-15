# ==============================================================================
# LangChain ile RAG (Retrieval-Augmented Generation) Uygulaması
# ==============================================================================
# Bu Streamlit uygulaması, LangChain kullanarak "Bellek Genişletme" (RAG)
# tekniğini göstermektedir.
#
# RAG Nedir?
# ----------
# Büyük dil modelleri (LLM) eğitildikleri veriye kadar bilgi sahibidir.
# Örneğin, şirketinizin iç dokümanları veya güncel haberler hakkında
# bilgi içermezler. RAG bu sorunu çözer:
#
# 1. Önce harici kaynaktan (URL, PDF, veritabanı) ilgili bilgiyi çek
# 2. Bu bilgiyi prompt'a "context" olarak ekle
# 3. LLM'den bu context'i kullanarak yanıt vermesini iste
#
# Bu sayede LLM, eğitim verisinde olmayan bilgilere de ulaşabilir!
#
# Bu uygulamada iki RAG yöntemi gösteriliyor:
# - URL tabanlı: Bir web sayfasından bilgi çekerek yanıt üretme
# - PDF tabanlı: Yüklenen PDF'den bilgi çekerek yanıt üretme
# ==============================================================================

import streamlit as st
import raghelper  # RAG işlemlerini yapan yardımcı modül

# Sayfa ayarları
st.set_page_config(page_title="LangChain ile Bellek Genişletme", layout="wide")
st.title("LangChain ile Bellek Genişletme: URL")
st.divider()

# ==============================================================================
# BÖLÜM 1: URL Tabanlı RAG
# ==============================================================================
# Bu bölümde bir web sayfasından içerik çekilir ve soru yanıtlamada kullanılır.
# Örneğin bir haber sitesindeki makaleyi çekip "Bu makalenin özeti nedir?" diye
# sorabilirsiniz. Model, makale içeriğini bilerek yanıt verecektir.
# ==============================================================================

# Üç sütun: Giriş, RAG yanıt, Normal yanıt
col_input, col_rag, col_normal = st.columns([1, 2, 2])

with col_input:
    # İçeriği çekilecek web adresi
    target_url = st.text_input(label="İşlenecek Web Adresini Giriniz:")
    st.divider()
    # Kullanıcının sorusu - bu soru hem RAG hem de normal modele gönderilecek
    prompt = st.text_input(label="Sorunuzu Giriniz:", key="url_prompt")
    st.divider()
    submit_btn = st.button(label="Sor", key="url_button")
    st.divider()

    if submit_btn:
        # RAG destekli yanıt - web sayfasından çekilen bilgiyi kullanır
        with col_rag:
            with st.spinner("Yanıt Hazırlanıyor..."):
                st.success("YANIT - Bellek Genişletme Devrede")
                # raghelper modülü URL'den içerik çeker, böler, ilgili parçaları bulur
                # ve bu bilgilerle zenginleştirilmiş bir prompt oluşturur
                st.markdown(raghelper.rag_with_url(target_url=target_url, prompt=prompt))
                st.divider()
        
        # Normal yanıt - sadece modelin bildiği bilgilerle yanıt verir
        # Bu sayede RAG'ın farkını görebilirsiniz!
        with col_normal:
            with st.spinner("Yanıt Hazırlanıyor..."):
                st.info("YANIT - Bellek Genişletme Devre Dışı")
                st.markdown(raghelper.ask_gemini(prompt=prompt))
                st.divider()


# ==============================================================================
# BÖLÜM 2: PDF Tabanlı RAG
# ==============================================================================
# Bu bölümde kullanıcının yüklediği PDF dosyasından bilgi çekilir.
# Özellikle şirket raporları, teknik dokümanlar, akademik makaleler için ideal.
# ==============================================================================

st.title("LangChain ile Bellek Genişletme: PDF")
st.divider()

col_input, col_rag, col_normal = st.columns([1, 2, 2])

with col_input:
    # PDF dosyası yükleme alanı
    # type=["pdf"]: Sadece PDF dosyalarını kabul et
    selected_file = st.file_uploader(label="İşlenecek Dosyayı Seçiniz", type=["pdf"])
    st.divider()
    prompt = st.text_input(label="Sorunuzu Giriniz:", key="pdf_prompt")
    st.divider()
    submit_btn = st.button(label="Sor", key="pdf_button")
    st.divider()

if submit_btn:
    with col_rag:
        with st.spinner("Yanıt Hazırlanıyor..."):
            st.success("YANIT - Bellek Genişletme Devrede")
            # PDF'den RAG yanıtı al
            # Dosya yolunu datasets_19/19.4-Datasets klasöründen alıyoruz
            AI_Response, relevant_documents = raghelper.rag_with_pdf(
                filepath=f"../datasets_19/19.4-Datasets/{selected_file.name}", 
                prompt=prompt
            )
            st.markdown(AI_Response)
            st.divider()
            
            # İlgili döküman parçalarını göster
            # Bu, hangi kaynaklardan bilgi alındığını gösterir (şeffaflık)
            for doc in relevant_documents:
                st.caption(doc.page_content)
                st.markdown(f"Kaynak: {doc.metadata}")
                st.divider()

    with col_normal:
        with st.spinner("Yanıt Hazırlanıyor..."):
            st.info("YANIT - Bellek Genişletme Devre Dışı")
            st.markdown(raghelper.ask_gemini(prompt=prompt))
            st.divider()