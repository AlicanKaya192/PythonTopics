import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
import anthropic
import cohere

load_dotenv()

openai_key = os.getenv("openai_apikey")

client_gpt = OpenAI(api_key=openai_key)
##############################################################
google_key = os.getenv("google_apikey")

genai.configure(api_key=google_key)

client_gemini = genai.GenerativeModel(model_name="gemini-pro")
##############################################################

anthropic_key = os.getenv("anthropic_apikey")

client_claude = anthropic.Anthropic(api_key=anthropic_key)
##############################################################

cohere_key = os.getenv("cohere_apikey")

client = cohere.Client(api_key=cohere_key)
##############################################################
##############################################################

def gpt_generate_response(prompt):

    AI_Response = client_gpt.chat.completions.create(

        model = "gpt-4-1106-preview",
        temperature=0,
        messages=[
            {"role": "system", "content":"Sen yardımsever bir asistansın."},
            {"role": "user", "content": prompt}
        ]
    )

    return AI_Response.choices[0].message.content


def gemini_generate_response(prompt):

    chat = client_gemini.start_chat(history=[])

    AI_Response = chat.send_message(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0,
        )
    )

    return AI_Response.text


def claude_generate_response(prompt):

    AI_Response = client_claude.beta.messages.create(
        model = "claude-2.1",
        temperature=0,
        max_tokens=1000,
        messages=[
            {"role":"user", "content":prompt}
        ]
    )

    return AI_Response.content[0].text


def command_generate_response(prompt):

    AI_Response = client.chat(
        model = "command",
        temperature=0,
        message=prompt
    )

    return AI_Response.text

