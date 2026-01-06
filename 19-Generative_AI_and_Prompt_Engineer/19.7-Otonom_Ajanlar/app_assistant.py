# =======================================================================================
# DOSYA: app_assistant.py
# AÇIKLAMA: OpenAI Assistants API kullanarak Python Kodlama Asistanı oluşturan
#           Streamlit web uygulaması.
#
# KONU: OTONOM AJANLAR - OpenAI Assistants API
# 
# Bu uygulama, OpenAI'nin Assistants API'sini kullanarak bir Python kodlama asistanı
# oluşturur. Kullanıcılar bu sohbet arayüzü üzerinden Python programlama ile ilgili
# sorular sorabilir ve yapay zeka destekli yanıtlar alabilir.
#
# OpenAI Assistants API Nedir?
# ----------------------------
# OpenAI Assistants API, çeşitli görevleri gerçekleştirebilen yapay zeka asistanları
# oluşturmak için kullanılan bir API'dir. Bu API şu temel özellikleri sunar:
# - Persistant Threads (Kalıcı Sohbet Geçmişi): Aynı thread_id ile devam eden sohbetler
# - Kod Yorumlama (Code Interpreter): Python kodlarını çalıştırabilme
# - Bilgi Erişimi (Retrieval): Yüklenen dosyalardan bilgi alabilme
# - Fonksiyon Çağırma (Function Calling): Özel fonksiyonları çağırabilme
#
# Streamlit Session State:
# ------------------------
# Streamlit'te session_state, kullanıcı oturumları arasında veri saklamak için 
# kullanılır. Bu sayede sayfa yenilendiğinde bile sohbet geçmişi korunur.
# - st.session_state.messages: Tüm sohbet mesajlarını saklar
# - st.session_state.thread_id: OpenAI thread ID'sini saklar
# =======================================================================================

import streamlit as st  # Streamlit - web arayüzü oluşturmak için kullanılan Python kütüphanesi
import assistant_helper  # OpenAI Assistants API ile etkileşim için yardımcı modül

# =======================================================================================
# SESSION STATE BAŞLATMA
# =======================================================================================
# Session state, Streamlit'te kullanıcı oturumu boyunca verileri saklamak için kullanılır.
# İlk çalıştırmada bu değerler mevcut değilse, boş listeler ve None değerleri ile başlatılır.
# Bu yapı sayesinde:
# - Sayfa yenilense bile sohbet geçmişi kaybolmaz
# - Her kullanıcının kendi thread_id'si olur
# =======================================================================================

if "messages" not in st.session_state:
    # messages: Tüm sohbet mesajlarını saklar (kullanıcı ve asistan mesajları)
    # Her mesaj {"role": "user/assistant", "content": "mesaj içeriği"} formatındadır
    st.session_state.messages = []
    
    # thread_id: OpenAI Assistants API'deki konuşma thread'inin benzersiz kimliği
    # İlk başta None olarak başlatılır, kullanıcı ilk mesajını gönderdiğinde oluşturulur
    st.session_state.thread_id = None


# =======================================================================================
# SAYFA YAPISI VE BAŞLIK AYARLARI
# =======================================================================================
# Streamlit'in page_config fonksiyonu, web sayfasının genel ayarlarını yapar:
# - page_title: Tarayıcı sekmesinde görünen başlık
# - page_icon: Tarayıcı sekmesinde görünen ikon (emoji veya dosya yolu olabilir)
# =======================================================================================

st.set_page_config(page_title="Python Kodlama Asistanı", page_icon=":speech_balloon:")

# Ana başlık - sayfanın en üstünde görünür
st.title("Python Kodlama Asistanı")

# Görsel ayırıcı çizgi - içerik bölümlerini ayırmak için kullanılır
st.divider()


# =======================================================================================
# SOHBET GEÇMİŞİNİ GÖRÜNTÜLEME
# =======================================================================================
# Daha önce gönderilen tüm mesajlar ekrana yazdırılır.
# Bu döngü, session_state'teki tüm mesajları sırayla render eder.
# st.chat_message(): Mesajı uygun formatta (user veya assistant) gösterir
# st.markdown(): Mesaj içeriğini Markdown formatında render eder
# =======================================================================================

for message in st.session_state.messages:
    # Her mesaj için uygun chat baloncuğu oluştur
    # role="user" ise kullanıcı baloncuğu, role="assistant" ise asistan baloncuğu
    with st.chat_message(message["role"]):
        # Mesaj içeriğini Markdown formatında göster
        # Markdown, kod blokları, linkler, kalın/italik yazı gibi formatlamayı destekler
        st.markdown(message["content"])

# =======================================================================================
# KULLANICI GİRİŞİ VE YANIT OLUŞTURMA
# =======================================================================================
# st.chat_input(): Kullanıcının mesaj yazabileceği bir input alanı oluşturur
# Walrus operatörü (:=): Hem değer atar hem de koşul kontrolü yapar
# prompt değişkeni, kullanıcının girdiği metni içerir
# =======================================================================================

if prompt := st.chat_input("Mesajınızı yazınız"):
    
    # ---------------------------------------------------------------------
    # KULLANICI MESAJINI GÖRÜNTÜLEME
    # ---------------------------------------------------------------------
    # Kullanıcının gönderdiği mesaj hemen ekranda gösterilir
    # Bu, anlık geri bildirim sağlar ve kullanıcı deneyimini iyileştirir
    # ---------------------------------------------------------------------
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # ---------------------------------------------------------------------
    # YAPAY ZEKA YANITI OLUŞTURMA
    # ---------------------------------------------------------------------
    # st.spinner(): İşlem sırasında dönen bir loading göstergesi gösterir
    # Bu, kullanıcıya sistemin çalıştığını bildirir
    # ---------------------------------------------------------------------
    
    with st.spinner("Yanıt oluşturuluyor..."):
        
        # İlk mesajda thread_id yoksa yeni bir thread oluştur
        # Thread, OpenAI Assistants API'de bir konuşmayı temsil eder
        # Aynı thread içindeki tüm mesajlar birbirleriyle bağlantılıdır
        if st.session_state.thread_id is None:
            st.session_state.thread_id = assistant_helper.start_new_thread()
        
        # Kullanıcının mesajını mevcut thread'e ekle
        # Bu, OpenAI'nin konuşma bağlamını korumasını sağlar
        assistant_helper.add_message_to_thread(thread_id=st.session_state.thread_id, prompt=prompt)

        # Asistanı çalıştır ve yanıt al
        # execute_run_cycle fonksiyonu:
        # 1. Yeni bir run başlatır
        # 2. Run tamamlanana kadar bekler
        # 3. Son yanıtı alır ve döndürür
        AI_Response = assistant_helper.execute_run_cycle(thread_id=st.session_state.thread_id)

        # Asistan yanıtını ekranda göster
        with st.chat_message("assistant"):
            st.markdown(AI_Response)
    
    # ---------------------------------------------------------------------
    # MESAJLARI SESSION STATE'E KAYDETME
    # ---------------------------------------------------------------------
    # Her iki mesaj da (kullanıcı ve asistan) session_state'e kaydedilir
    # Bu sayede sayfa yenilendiğinde sohbet geçmişi korunur
    # ---------------------------------------------------------------------
    
    st.session_state.messages.append({"role":"user", "content": prompt})
    st.session_state.messages.append({"role":"assistant", "content": AI_Response})