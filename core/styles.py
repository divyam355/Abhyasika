import streamlit as st


def load_css():
    st.markdown("""
    <style>

    /* Main App */
    .stApp{
        background-color:#0E1117;
        color:white;
    }

    .main{
        background-color:#0E1117;
    }

    .block-container{
        padding-top:2rem;
        padding-left:2rem;
        padding-right:2rem;
        padding-bottom:2rem;
    }

    /* Sidebar */

    section[data-testid="stSidebar"]{
        background-color:#161B22 !important;
        color:white !important;
        border-right:1px solid #30363D;
    }

    section[data-testid="stSidebar"] *{
        color:white !important;
    }

    /* Radio Buttons */

    div[role="radiogroup"] label{
        background:#21262D;
        border-radius:10px;
        margin-bottom:8px;
        padding:8px;
    }

    /* Metric Card */

    .card{
        background:#161B22;
        border:1px solid #30363D;
        border-radius:15px;
        padding:20px;
        text-align:center;
    }

    .card-title{
        color:#9CA3AF;
        font-size:15px;
    }

    .card-value{
        color:#3B82F6;
        font-size:34px;
        font-weight:bold;
    }

    /* Section */

    .section{
        background:#161B22;
        border:1px solid #30363D;
        border-radius:15px;
        padding:20px;
        margin-top:15px;
        margin-bottom:15px;
    }

    .main-title{
        color:#3B82F6;
        font-size:40px;
        font-weight:bold;
    }

    .subtitle{
        color:#9CA3AF;
        font-size:18px;
    }

    </style>
    """, unsafe_allow_html=True)