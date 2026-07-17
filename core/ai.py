import streamlit as st
from google import genai

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
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