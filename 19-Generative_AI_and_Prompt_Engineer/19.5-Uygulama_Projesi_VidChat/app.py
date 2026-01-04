# ==============================================================================
# VidChat: YouTube Video ile Sohbet Uygulaması - Ana Modül
# ==============================================================================
# Bu uygulama, YouTube videolarının içeriğiyle sohbet etmenizi sağlayan
# bir RAG (Retrieval-Augmented Generation) sistemidir.
#
# Ne işe yarar?
# -------------
# Bir YouTube videosu izlemek yerine, videonun içeriği hakkında AI'a soru
# sorabilirsiniz. Örneğin 2 saatlik bir eğitim videosunu baştan sona izlemek
# yerine "Bu videoda Python'da listeler nasıl anlatılmış?" diye sorabilirsiniz.
#
# Nasıl çalışır?
# --------------
# 1. YouTube videosu seçilir (URL ile veya arama yaparak)
# 2. Videonun ses dosyası indirilir
# 3. OpenAI Whisper ile ses metne dönüştürülür (transkripsiyon)
# 4. Metin parçalara bölünür ve vektör veritabanına kaydedilir
# 5. Kullanıcının sorusu, ilgili parçalarla eşleştirilir
# 6. Gemini modeli, bu bağlamı kullanarak soruyu yanıtlar
#
# Gerekli Materyaller:
# --------------------
# Banner görseli: assets/19.5-Materyaller/img/app_banner.png
# ==============================================================================

import streamlit as st  # Web arayüzü için Streamlit framework'ü
import videohelper  # YouTube video işlemleri (transkripsiyon, arama)
import raghelper  # RAG (Retrieval-Augmented Generation) işlemleri

# ==============================================================================
# Session State Başlatma
# ==============================================================================
# Streamlit'te sayfa her yenilendiğinde değişkenler sıfırlanır.
# Session State, değişkenleri oturum boyunca saklamak için kullanılır.
# Böylece kullanıcı her soru sorduğunda videoyu tekrar indirmek zorunda kalmaz.
# Bu, hem performans hem de API maliyeti açısından çok önemli bir optimizasyon!
# ==============================================================================
if "current_video_url" not in st.session_state:
    st.session_state.current_video_url = None  # Şu an işlenen videonun URL'si
    st.session_state.current_transcript_docs = []  # Videonun transkript dökümanları
    st.session_state.videos = []  # Arama sonuçlarından gelen video listesi

# ==============================================================================
# Sayfa Yapılandırması ve Başlık
# ==============================================================================
st.set_page_config(page_title="VidChat: Youtube ile Sohbet!", layout="centered")
# Banner görseli - uygulamanın üst kısmında görünen tanıtım resmi
st.image(image="./img/app_banner.png")
st.title("VidChat: YouTube ile Sohbet!")
st.divider()

# ==============================================================================
# İki Farklı Video Seçim Yöntemi
# ==============================================================================
# Tab yapısı ile kullanıcıya iki seçenek sunuyoruz:
# 1. URL Girerek: Direkt YouTube video linkini yapıştırma
# 2. Arama Yaparak: YouTube'da arama yapıp sonuçlardan seçme
# ==============================================================================
tab_url, tab_search = st.tabs(["URL Girerek", "Arama Yaparak"])

# ==============================================================================
# TAB 1: URL ile Video Seçimi
# ==============================================================================
# En basit yöntem - kullanıcı direkt YouTube linkini yapıştırır ve soru sorar
# ==============================================================================
with tab_url:

    # Kullanıcıdan YouTube video URL'si ve sorusunu al
    video_url = st.text_input(label="YouTube Video Adresini Giriniz:", key="url_video_url")
    prompt = st.text_input(label="Sorunuzu Giriniz:", key="url_prompt")
    submit_btn = st.button("Sor", key="url_submit")

    if submit_btn:
        # Videoyu oynatıcıda göster - kullanıcı isterse izleyebilir
        st.video(data=video_url)
        st.divider()
        
        # Önbellekleme Kontrolü: Eğer farklı bir video seçildiyse transkripti yeniden al
        # Aynı videoysa, daha önce alınan transkripti kullan (performans optimizasyonu!)
        if st.session_state.current_video_url != video_url:
            with st.spinner("AŞAMA-1: Video metni hazırlanıyor..."):
                # Video sesini indir ve Whisper ile metne dönüştür
                video_transcript_docs = videohelper.get_video_transcript(url=video_url)
                st.session_state.current_transcript_docs = video_transcript_docs
        st.success("Video transkripti ön belleğe kaydedildi!")
        st.divider()
        st.session_state.current_video_url = video_url
        

        # RAG ile soruyu yanıtla - transkript üzerinde semantik arama yap
        with st.spinner("AŞAMA-2: Sorunuz yanıtlanıyor..."):
            AI_Response, relevant_documents = raghelper.rag_with_video_transcript(transcript_docs=st.session_state.current_transcript_docs, prompt=prompt)
        st.info("YANIT:")
        st.markdown(AI_Response)
        st.divider()

        # Şeffaflık: Hangi kaynaklardan bilgi alındığını göster
        # Bu, kullanıcının yanıtı doğrulamasına yardımcı olur
        for doc in relevant_documents:
            st.warning("REFERANS:")
            st.caption(doc.page_content)
            st.markdown(f"Kaynak: {doc.metadata}")
            st.divider()

# ==============================================================================
# TAB 2: Arama ile Video Seçimi
# ==============================================================================
# Kullanıcı YouTube'da arama yapabilir ve sonuçlardan video seçebilir
# Bu özellik, belirli bir konuyu öğrenmek isteyenler için çok kullanışlı
# ==============================================================================
with tab_search:
    
    # İki sütunlu düzen: Sol tarafta arama işlemleri, sağ tarafta video önizlemeleri
    col_left, col_center, col_right = st.columns([20,1,10])

    with col_left:

        st.subheader("Video Arama İşlemleri")
        st.divider()
        # Arama terimi girişi
        search_term = st.text_input(label="Aramak İstediğiniz Sözcükleri Giriniz:", key="search_term")
        # Kaç video getirilecek - çok video yavaşlatabilir
        video_count = st.slider(label="Sonuç Sayısı", min_value=1, max_value=5, value=5, key="search_video_count")
        # Sıralama seçenekleri - YouTube API'nin desteklediği sıralama türleri
        sorting_options = ["En İlgili", "Tarihe Göre", "İzlenme Sayısı", "Beğeni Sayısı"]
        sorting_criteria = st.selectbox(label="Sıralama Ölçütü", options=sorting_options)
        search_btn = st.button(label="Video Ara", key="search_button")
        st.divider()

        # Arama butonuna basıldığında YouTube'da arama yap
        if search_btn:
            st.session_state.videos = []  # Önceki sonuçları temizle
            # scrapetube ile YouTube araması yap
            videolist = videohelper.get_videos_for_search_term(search_term=search_term, video_count=video_count, sorting_criteria=sorting_criteria)
            
            # Sonuçları session state'e kaydet
            for video in videolist:
                st.session_state.videos.append(video)
        
        # Seçim kutusu için video URL'lerini ve başlıklarını hazırla
        video_urls = []
        video_titles = {}
        for video in st.session_state.videos:
            video_urls.append(video.video_url)
            video_titles.update({video.video_url:video.video_title})

        # Video seçim dropdown'ı - format_func ile URL yerine başlık gösterilir
        selected_video = st.selectbox(
            label="Sohbet Etmek İstediğiniz Videoyu Seçiniz:",
            options=video_urls,
            format_func=lambda url: video_titles[url],
            key="search_selectbox"
        )
        
        # Video seçildiyse soru sorma alanını göster
        if selected_video:
            search_prompt = st.text_input(label="Sorunuzu Giriniz:", key="search_prompt")
            search_ask_btn = st.button(label="Sor", key="search_ask_button")

            if search_ask_btn:
                st.caption("Seçtiğiniz Video")
                st.video(data=selected_video)
                st.divider()
                
                # Aynı önbellekleme mantığı - farklı video için transkript al
                if st.session_state.current_video_url != selected_video:
                    with st.spinner("AŞAMA-1: Video metni hazırlanıyor..."):
                        video_transcript_docs = videohelper.get_video_transcript(url=selected_video)
                        st.session_state.current_transcript_docs = video_transcript_docs
                    st.success("Video transkripti ön belleğe kaydedildi!")
                    st.divider()
                    st.session_state.current_video_url = selected_video
            

                # RAG ile yanıt üret
                with st.spinner("AŞAMA-2: Sorunuz yanıtlanıyor..."):
                    AI_Response, relevant_documents = raghelper.rag_with_video_transcript(transcript_docs=st.session_state.current_transcript_docs, prompt=search_prompt)
                st.info("YANIT:")
                st.markdown(AI_Response)
                st.divider()

                # Referans bilgilerini göster - şeffaflık için önemli
                for doc in relevant_documents:
                    st.warning("REFERANS:")
                    st.caption(doc.page_content)
                    st.markdown(f"Kaynak: {doc.metadata}")
                    st.divider()

    # Orta sütun - görsel ayırıcı olarak boş bırakıldı
    with col_center:
        st.empty()

    # Sağ sütun - Arama sonuçlarını görsel olarak göster
    with col_right:

        st.subheader("İlgili Videolar")
        st.divider()

        # Tüm bulunan videoları thumbnail'larıyla listele
        for i, video in enumerate(st.session_state.videos):
            st.info(f"Video No: {i+1}")
            st.video(data=video.video_url)  # Video önizlemesi
            st.caption(f"Video Başlığı: {video.video_title}")
            st.caption(f"Kanal: {video.channel_name}")
            st.caption(f"Video Süresi: {video.duration}")
            st.divider()  