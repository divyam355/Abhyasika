import streamlit as st
from google import genai

API_KEY = st.secrets["GEMINI_API_KEY"]
st.write("Gemini key loaded:", bool(API_KEY))
st.write("Gemini key length:", len(API_KEY))
st.write("Gemini key prefix:", API_KEY[:4])

client = genai.Client(
    api_key=API_KEY


)


MODEL = "gemini-3.1-flash-lite"


# ===========================================
# ASK AI
# ===========================================

from core.prompt_builder import build_prompt


def ask_ai(question, exam=None):

    try:

        prompt = build_prompt(
            question,
            exam
        )
        print("=" * 60)
        print(prompt)
        print("=" * 60)

        response = client.models.generate_content(

            model=MODEL,

            contents=prompt

        )

        return response.text

    except Exception as e:

        return f"❌ {str(e)}"