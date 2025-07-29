import streamlit as st
import pandas as pd
import plotly.express as px

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Resume vs Reality",
    layout="wide",
    page_icon="✨"
)

# ---- CUSTOM STYLE (Glassmorphism + Clean Fonts) ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Manrope', sans-serif;
        background: #f8f8f9;
    }
    .main {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stTabs [role="tab"] {
        padding: 8px 24px;
        font-weight: 600;
        font-size: 1rem;
        color: #333;
        border-radius: 12px 12px 0 0;
        background: #eaeaea;
        margin-right: 8px;
    }
    .stTabs [aria-selected="true"] {
        background: #5e60ce;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---- APP TITLE & HEADER ----
st.title("💼 Resume vs Reality")
st.subheader("✨ Which Skills Actually Help You Get Hired?")
st.markdown("We all build resumes hoping they reflect our potential. But behind every hiring decision lies a pattern. "
            "This project is a search for those patterns — an exploration of the gap between what we write and what employers value. "
            "**Here, data becomes your mentor.** The truth? It’s not always what you think.")

# ---- PERSONAL NARRATIVE ----
with st.expander("👩‍💻 Why this app matters (from the developer)"):
    st.markdown("""
    As an MBA student navigating the complex, anxiety-filled job market, I found myself wondering:
    > _"Am I listing the right skills? Do recruiters even care about what I’ve put on my resume?"_

    This app channels that anxiety into a **productive exploration** — one that helps job seekers see behind the curtain using real data.

    It’s not just about skills. It’s about **clarity**, **confidence**, and giving you a **lens to see what recruiters are actually hiring for**.

    Welcome to *Resume vs Reality* — your data-driven, friendly career coach. ✨
    """)

# ---- TABS LAYOUT ----
tab1, tab2, tab3, tab4 = st.tabs(["📊 Insights", "📎 Resume Match", "🔮 AI Prediction", "📥 Report"])

# ---- PLACEHOLDERS FOR NEXT PHASES ----
with tab1:
    st.markdown("#### 📊 Skill Trends and Visual Comparisons will appear here...")
    st.info("This section will compare skills in resumes, job listings, and hired profiles with charts. Coming soon!")

with tab2:
    st.markdown("#### 📎 Compare Your Resume to a Job Description")
    st.info("Paste your skills and a job ad to see overlap, gaps, and tips. This will be interactive.")

with tab3:
    st.markdown("#### 🔮 See How Likely You Are to Get Shortlisted")
    st.info("Enter your skill list and get a probability score based on our trained AI model. Visual scoring bar coming up!")

with tab4:
    st.markdown("#### 📥 Download Personalized Report")
    st.info("This section will allow export/sharing of your insights and feedback.")

# ---- FOOTER ----
st.markdown("---")
st.markdown("© 2025 Resume vs Reality | Built with ❤️ by an MBA student for fellow dream chasers.")
