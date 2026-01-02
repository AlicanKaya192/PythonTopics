import streamlit as st
import helper

if "messages" not in st.session_state:
    st.session_state.messages = []
    #st.session_state.messages.append({"role": "system", "content":"Sen yardımsever bir asistansın."})

def adjust_model_relations():
    st.session_state.messages = []

def send_message(prompt):

    st.chat_message("user").markdown(prompt)

    if st.session_state.selected_model == "GPT-4 Turbo":
        response = helper.gpt_generate_response(prompt)

    elif st.session_state.selected_model == "Gemini Pro":
        response = helper.gemini_generate_response(prompt)

    elif st.session_state.selected_model == "Claude 2.1":
        response = helper.claude_generate_response(prompt)

    elif st.session_state.selected_model == "Command":
        response = helper.command_generate_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

st.sidebar.header("KONFİGÜRSYON")
st.sidebar.divider()
models_list = ["GPT-4 Turbo", "Gemini Pro", "Claude 2.1", "Command"]
st.sidebar.selectbox(label="Dil Modeli Seçiniz:", options=models_list, on_change=adjust_model_relations, key="selected_model")
st.sidebar.divider()
questions_list = [
    "İki sayının toplamını bulan Python kodunu yaz", 
    "Python Streamlit kullanarak basit kullanıcı girişi kodu yaz", 
    "Python Streamlit kullanarak Eisenhower Zaman Yönetimi Matrisi ekranda gösteren bir uygulamanın kodunu yaz", 
    "HTML, CSS ve Javascript dillerini kullanarak nihai çıktısı tek bir HTML dosyası olacak şekilde, bir sayı tahmin oyununun kodunu yaz",
    "Manuel Soru Yaz"
    ]
st.sidebar.selectbox(label="Örnek Soru Seçiniz:", options=questions_list, key="selected_question", index=4)


st.title("Dil Modellerinin Kod Yazma Yeteneklerinin Kıyaslanması")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.selected_question != "Manuel Soru Yaz":
    prompt = st.session_state.selected_question
    send_message(prompt)

elif prompt := st.chat_input("Mesajınızı Giriniz", key="prompt_box"):

    send_message(prompt)


    
    #st.session_state.messages.append({"role": "assistant", "content": response})

