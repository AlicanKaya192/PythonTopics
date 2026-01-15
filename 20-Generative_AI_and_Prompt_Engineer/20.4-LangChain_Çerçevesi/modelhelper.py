# ==============================================================================
# Model Yardımcı Modülü (Model Helper)
# ==============================================================================
# Farklı LLM API'lerini çağırmak için yardımcı fonksiyonlar.
# ==============================================================================

import os
from dotenv import load_dotenv
load_dotenv()

# ==============================================================================
# OpenAI GPT-4
# ==============================================================================
my_key_openai = os.getenv("openai_apikey")
from langchain_openai import ChatOpenAI

def ask_gpt(prompt, temperature, max_tokens):
    """
    OpenAI GPT-4 Turbo modeline soru sorar.
    - 128K context window
    - Kod ve analiz konusunda çok başarılı
    """
    llm = ChatOpenAI(
        api_key=my_key_openai, 
        temperature=temperature, 
        max_tokens=max_tokens, 
        model="gpt-4-1106-preview"
    )
    AI_Response = llm.invoke(prompt)
    return AI_Response.content


# ==============================================================================
# Google Gemini Pro
# ==============================================================================
my_key_google = os.getenv("google_apikey")
from langchain_google_genai import ChatGoogleGenerativeAI

def ask_gemini(prompt, temperature):
    """
    Google Gemini Pro modeline soru sorar.
    - Google'ın arama verileriyle entegre
    - 32K context window
    """
    llm = ChatGoogleGenerativeAI(
        google_api_key=my_key_google, 
        temperature=temperature, 
        model="gemini-pro"
    )
    AI_Response = llm.invoke(prompt)
    return AI_Response.content


# ==============================================================================
# Anthropic Claude 2.1
# ==============================================================================
my_key_anthropic = os.getenv("anthropic_apikey")
from langchain_community.chat_models import ChatAnthropic

def ask_claude(prompt, temperature, max_tokens):
    """
    Anthropic Claude 2.1 modeline soru sorar.
    - 200K context window (en büyüklerden!)
    - Detaylı analiz ve uzun belgeler için ideal
    """
    llm = ChatAnthropic(
        anthropic_api_key=my_key_anthropic, 
        temperature=temperature, 
        max_tokens=max_tokens, 
        model_name="claude-2.1"
    )
    AI_Response = llm.invoke(prompt)
    return AI_Response.content


# ==============================================================================
# Cohere Command
# ==============================================================================
my_key_cohere = os.getenv("cohere_apikey")
from langchain_community.chat_models import ChatCohere

def ask_command(prompt, temperature, max_tokens):
    """
    Cohere Command modeline soru sorar.
    - İş uygulamaları için optimize
    - RAG sistemleri için mükemmel
    """
    llm = ChatCohere(
        cohere_api_key=my_key_cohere, 
        temperature=temperature, 
        max_tokens=max_tokens, 
        model="command"
    )
    AI_Response = llm.invoke(prompt)
    return AI_Response.content