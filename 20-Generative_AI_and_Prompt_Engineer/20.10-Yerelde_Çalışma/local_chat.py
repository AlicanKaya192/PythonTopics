# ===================================================================================
# 19.10 - YERELDE ÇALIŞMA: LOCAL CHAT UYGULAMASI
# ===================================================================================
# Bu dosya, yerel olarak çalışan açık kaynak LLM modelleri ile sohbet edebileceğiniz
# bir Streamlit chatbot arayüzünü içerir.
# 
# PROJE AMACI:
# ------------
# Bu proje, bulut tabanlı AI servislerine (OpenAI, Anthropic vb.) alternatif olarak
# kendi bilgisayarınızda çalışan açık kaynak modeller ile etkileşim kurmanızı sağlar.
# Ollama ve LM Studio entegrasyonu ile tamamen yerel ve özel bir AI deneyimi sunar.
#
# NEDEN YERELDE ÇALIŞMA?
# ----------------------
# 1. GİZLİLİK: Verileriniz bilgisayarınızdan çıkmaz, hiçbir sunucuya gitmez
# 2. MALİYET: API ücreti ödemezsiniz, tamamen ücretsiz kullanım
# 3. BAĞIMSIZLIK: İnternet bağlantısı gerekmez (model indirildikten sonra)
# 4. ÖZELLEŞTİRME: İstediğiniz modeli kullanabilir, fine-tune edebilirsiniz
# 5. ÖĞRENME: LLM'lerin nasıl çalıştığını daha iyi anlarsınız
#
# DESTEKLENEN PLATFORMLAR:
# ------------------------
# - Ollama: macOS, Linux ve Windows için açık kaynak LLM runner
# - LM Studio: Kullanıcı dostu GUI ile yerel model çalıştırma
#
# ÖN GEREKSİNİMLER:
# -----------------
# 1. Ollama veya LM Studio kurulu olmalı
# 2. En az bir model indirilmiş olmalı (örn: mistral, llama2, codellama)
# 3. İlgili uygulama çalışır durumda olmalı (API sunucusu aktif)
# ===================================================================================

import streamlit as st  # Web arayüzü oluşturmak için Streamlit kütüphanesi
import localhelper       # Yerel model API çağrıları için yardımcı modülümüz

# ===================================================================================
# SESSION STATE - SOHBET GEÇMİŞİ YÖNETİMİ
# ===================================================================================
# Streamlit'te session_state, sayfa yenilense bile verileri korur.
# 
# NEDEN SESSION STATE KULLANIYORUZ?
# ---------------------------------
# - Streamlit her etkileşimde sayfayı yeniden render eder
# - Session state olmadan sohbet geçmişi kaybolur
# - "messages" listesi tüm konuşmayı saklar
# 
# MESAJ FORMATI:
# --------------
# Her mesaj bir dictionary:
# - {"role": "system", "content": "..."} - Sistem talimatı
# - {"role": "user", "content": "..."}   - Kullanıcı mesajı
# - {"role": "assistant", "content": "..."} - AI yanıtı
#
# BU BİZE NE SAĞLAR?
# ------------------
# - Bağlamsal sohbet (AI önceki mesajları hatırlar)
# - Doğal diyalog akışı
# - Çok turlu konuşma desteği

if "messages" not in st.session_state:
    # İlk açılışta boş mesaj listesi oluştur
    st.session_state.messages = []
    
    # Sistem mesajı ekle - AI'ın davranışını belirler
    # NEDEN SİSTEM MESAJI?
    # - AI'a kim olduğunu ve nasıl davranacağını söyler
    # - Yanıt kalitesini artırır
    # - Kişiselleştirme imkanı sağlar (örn: "Sen bir Python uzmanısın")
    st.session_state.messages.append({
        "role": "system", 
        "content": "You are a helpful assistant."
    })


# ===================================================================================
# YANIT ÜRETİM FONKSİYONU
# ===================================================================================

def generate_response():
    """
    Seçilen yerel AI sağlayıcısından yanıt üretir.
    
    NEDEN BU FONKSİYON?
    -------------------
    - Farklı sağlayıcıları (Ollama, LM Studio) tek noktadan yönetir
    - Kodun modüler ve bakımı kolay olmasını sağlar
    - Yeni sağlayıcı eklemek kolaylaşır
    
    BU FONKSİYON NE YAPAR?
    ----------------------
    1. Kullanıcının seçtiği sağlayıcıyı kontrol eder
    2. İlgili helper fonksiyonunu çağırır
    3. Tüm sohbet geçmişini API'ye gönderir (bağlam için)
    4. AI yanıtını döndürür
    
    TEMPERATURe=0.7 NEDEN?
    ----------------------
    - 0: Tamamen deterministik (aynı soru = aynı cevap)
    - 1: Maksimum yaratıcılık (çok rastgele olabilir)
    - 0.7: Dengeli seçim - yaratıcı ama tutarlı yanıtlar
    
    Returns:
        str: AI tarafından üretilen yanıt metni
    """
    
    # LM Studio seçiliyse
    if selected_provider == "LM Studio":
        # LM Studio API'sini kullanarak yanıt üret
        # NOT: LM Studio kendi GUI'sinden model seçimi yapılır
        AI_Response = localhelper.generate_with_lmstudio(
            chat_history=st.session_state.messages, 
            temperature=0.7
        )
    
    # Ollama seçiliyse
    if selected_provider == "Ollama":
        # Ollama API'sini kullanarak yanıt üret
        # NOT: Varsayılan model "mistral", değiştirilebilir
        AI_Response = localhelper.generate_with_ollama(
            chat_history=st.session_state.messages, 
            temperature=0.7
        )
    
    return AI_Response


# ===================================================================================
# SAYFA BAŞLIĞI VE TASARIM
# ===================================================================================
# Uygulamanın görsel kimliğini oluşturuyoruz.
# 
# NEDEN BU BAŞLIK?
# ----------------
# - Kullanıcıya uygulamanın amacını hemen anlatır
# - "Yerelde" kelimesi gizlilik ve bağımsızlığı vurgular
# - "Açık Kaynak" topluluk desteğini ve şeffaflığı belirtir

st.header("Sohbet Botu: Yerelde Açık Kaynak Model İşletimi")
st.divider()  # Görsel ayırıcı çizgi

# ===================================================================================
# SIDEBAR - SAĞLAYICI SEÇİMİ
# ===================================================================================
# Sidebar'da kullanıcı yerel AI sağlayıcısını seçer.
# 
# NEDEN SIDEBAR?
# --------------
# - Ana sohbet alanını temiz tutar
# - Ayarlar her zaman erişilebilir durumda
# - Profesyonel uygulama görünümü

st.sidebar.subheader("Yerel İşletim Türü Seçiniz:")
st.sidebar.divider()

# ===================================================================================
# SAĞLAYICI SEÇİM KUTUSU
# ===================================================================================
# Kullanıcı Ollama veya LM Studio arasında seçim yapar.
# 
# OLLAMA vs LM STUDIO:
# --------------------
# OLLAMA:
#   - Komut satırı odaklı, terminal kullanıcıları için
#   - Çok hafif ve hızlı
#   - Model indirme: "ollama pull mistral"
#   - API: http://localhost:11434
#
# LM STUDIO:
#   - GUI tabanlı, kullanımı kolay
#   - Model indirme GUI üzerinden
#   - Görsel model yönetimi
#   - API: http://localhost:1234

selected_provider = st.sidebar.selectbox(
    label="Yerel İşletim Türü:", 
    options=["LM Studio", "Ollama"]
)

# ===================================================================================
# SOHBET GEÇMİŞİNİ GÖRÜNTÜLEME
# ===================================================================================
# Önceki mesajları ekranda gösteriyoruz.
# 
# NEDEN [1:] DİLİMİ?
# ------------------
# - messages[0] sistem mesajıdır ("You are a helpful assistant")
# - Sistem mesajı kullanıcıya gösterilmez, sadece AI için bağlam sağlar
# - [1:] ile sistem mesajını atlayıp kullanıcı/asistan mesajlarını gösteriyoruz
#
# BU BİZE NE SAĞLAR?
# ------------------
# - Temiz sohbet görünümü
# - Kullanıcı sadece gerçek konuşmayı görür
# - WhatsApp/Telegram benzeri deneyim

for message in st.session_state.messages[1:]:
    # Her mesaj için uygun chat balonu oluştur
    # role="user" → kullanıcı balonu (sağda)
    # role="assistant" → AI balonu (solda)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===================================================================================
# KULLANICI GİRİŞİ VE YANIT DÖNGÜSÜ
# ===================================================================================
# Kullanıcıdan mesaj alıp AI yanıtı üretiyoruz.
# 
# WALRUS OPERATÖRÜ (:=) NEDİR?
# ----------------------------
# - Python 3.8+ özelliği
# - Değer ataması yaparken aynı anda koşul kontrolü yapar
# - prompt := st.chat_input(...) demek:
#   1. Kullanıcı input'unu prompt değişkenine ata
#   2. Eğer boş değilse if bloğuna gir
# 
# BU BİZE NE SAĞLAR?
# ------------------
# - Daha temiz ve okunabilir kod
# - Gereksiz if-else yapılarından kaçınma

if prompt := st.chat_input("Please enter your message"):

    # -------------------------------------------------------------------------
    # KULLANICI MESAJINI GÖSTER
    # -------------------------------------------------------------------------
    # Kullanıcının yazdığı mesajı hemen ekranda göster
    st.chat_message("user").markdown(prompt)

    # -------------------------------------------------------------------------
    # MESAJI GEÇMİŞE EKLE
    # -------------------------------------------------------------------------
    # Kullanıcı mesajını session_state'e kaydet
    # NEDEN? AI'ın sonraki turda bu mesajı da görmesi için
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt
    })

    # -------------------------------------------------------------------------
    # AI YANITINI ÜRET
    # -------------------------------------------------------------------------
    # st.spinner ile kullanıcıya bekleme göstergesi sunuyoruz
    # NEDEN SPINNER?
    # - Yerel modeller de yanıt üretmek için zaman alır
    # - Kullanıcı işlemin devam ettiğini bilmeli
    # - Daha profesyonel kullanıcı deneyimi
    with st.spinner("Yapay Zeka yanıtlıyor..."):
        response = generate_response()
    
    # -------------------------------------------------------------------------
    # AI YANITINI GÖSTER
    # -------------------------------------------------------------------------
    # AI'ın ürettiği yanıtı chat balonunda göster
    st.chat_message("assistant").markdown(response)

    # -------------------------------------------------------------------------
    # YANITI GEÇMİŞE EKLE
    # -------------------------------------------------------------------------
    # AI yanıtını da session_state'e kaydet
    # NEDEN? Sonraki turda AI kendi önceki yanıtlarını da görsün
    # Bu, tutarlı ve bağlamsal bir sohbet sağlar
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response
    })


# ===================================================================================
# UYGULAMA KULLANIM REHBERİ
# ===================================================================================
# 
# OLLAMA İLE KULLANMAK İÇİN:
# 1. Ollama'yı indirin: https://ollama.ai
# 2. Terminalde model indirin: ollama pull mistral
# 3. Ollama'nın çalıştığından emin olun
# 4. Bu uygulamayı başlatın: streamlit run local_chat.py
# 5. Sidebar'dan "Ollama" seçin ve sohbet edin!
#
# LM STUDIO İLE KULLANMAK İÇİN:
# 1. LM Studio'yu indirin: https://lmstudio.ai
# 2. Uygulama içinden bir model indirin
# 3. "Local Server" sekmesinden sunucuyu başlatın
# 4. Bu uygulamayı başlatın: streamlit run local_chat.py
# 5. Sidebar'dan "LM Studio" seçin ve sohbet edin!
#
# GELİŞTİRME ÖNERİLERİ:
# ---------------------
# 1. Model seçimi dropdown'u eklenebilir
# 2. Temperature slider'ı eklenebilir
# 3. Sohbet geçmişi kaydetme/yükleme
# 4. Farklı sistem promptları seçimi
# 5. Çoklu sohbet sekmeleri
# ===================================================================================
