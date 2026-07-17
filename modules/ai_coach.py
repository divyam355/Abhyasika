import streamlit as st
from datetime import datetime
from core.ai import ask_ai

def show(exam=None):

    if "messages" not in st.session_state:
        st.session_state.messages = []

    hour = datetime.now().hour

    if hour < 12:
        greeting = "🌅 Good Morning"
    elif hour < 17:
        greeting = "☀ Good Afternoon"
    else:
        greeting = "🌙 Good Evening"

    st.title("🤖 Divya AI")

    st.caption("Personal AI Study Mentor")

    st.divider()

    # Welcome message
    if len(st.session_state.messages) == 0:

        st.session_state.messages.append({

            "role": "assistant",

            "content":
f"""{greeting} 👋

Welcome to Abhyasika.

I'm Divya AI.

I can help you with:

📚 Concepts

📝 Mock Tests

📅 Timetable

📊 Analytics

🌐 Latest Notifications

💼 Career Guidance

Ask me anything below."""

        })

    # Display Chat History
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Chat Input
    prompt = st.chat_input(
        "Ask me anything..."
    )

    if prompt:

        st.session_state.messages.append({

            "role": "user",

            "content": prompt

        })

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.spinner("🤖 Divya AI is thinking..."):
            reply = ask_ai(
                prompt,
                exam
            )

        st.session_state.messages.append({

            "role": "assistant",

            "content": reply

        })

        with st.chat_message("assistant"):

            st.markdown(reply)

    st.divider()

    st.subheader("💡 Suggested Questions")

    c1, c2 = st.columns(2)

    with c1:

        st.button(
            "📚 Explain Industry 4.0",
            use_container_width=True
        )

        st.button(
            "📝 Generate Study Plan",
            use_container_width=True
        )

        st.button(
            "📖 Explain Lean Manufacturing",
            use_container_width=True
        )

    with c2:

        st.button(
            "📊 Analyse My Progress",
            use_container_width=True
        )

        st.button(
            "📅 Create Revision Plan",
            use_container_width=True
        )

        st.button(
            "🌐 Latest GATE Notification",
            use_container_width=True
        )