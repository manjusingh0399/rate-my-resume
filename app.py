import streamlit as st
import pandas as pd
import plotly.express as px

# --- App Configuration ---
st.set_page_config(page_title="Resume vs Reality", page_icon="🧠", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
        background: #f4f4f9;
        color: #2c2c2c;
    }
    h1, h2, h3 {
        color: #6a1b9a;
    }
    .box {
        background-color: #ffffff;
        border-left: 6px solid #6a1b9a;
        padding: 1em;
        margin-bottom: 1.5em;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .highlight {
        color: #d81b60;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Dummy Skill Data (Replace with real CSVs) ---
def load_data():
    return pd.DataFrame({
        "Skill": ["Excel", "SQL", "Python", "Communication", "Teamwork", "Power BI", "Market Research"],
        "Job Ads": [92, 76, 68, 45, 41, 32, 29],
        "Resumes": [88, 49, 37, 93, 88, 27, 30],
        "Hires": [64, 54, 55, 37, 31, 18, 15]
    })

data = load_data()
roles = {
    "Analyst": ["SQL", "Python", "Excel"],
    "Marketing": ["SEO", "Canva", "Market Research"],
    "HR": ["Communication", "Recruitment"],
    "Sales": ["Negotiation", "CRM"]
}
advice = {
    "Python": "Python opens up analytics & automation.",
    "SQL": "Knowing SQL lets you speak to databases.",
    "Excel": "Excel is versatile and required almost everywhere.",
    "SEO": "Helps boost content visibility for marketers.",
    "Communication": "Essential for collaboration and impact.",
    "Recruitment": "Key for people-oriented roles like HR.",
    "Negotiation": "Boosts your influence in sales & deals.",
    "CRM": "Customer Relationship tools are sales gold.",
    "Canva": "Your go-to for quick creative content."
}

# --- Tab Navigation ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Welcome", "📊 Insights", "🎯 Fit Score", "💡 Suggestions", "ℹ️ About"])

# --- Welcome Tab ---
with tab1:
    st.markdown("<h1 style='text-align:center;'>Welcome to Resume vs Reality ✨</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class='box'>
        <p>This isn't just another job tool — it's your career compass 🧭. Using real data from resumes, job ads, and actual hires, this app shows <span class='highlight'>what truly matters</span> when you're looking for a job.</p>
        <ul>
            <li>📊 Discover which skills companies value most</li>
            <li>🧠 Compare your skills with what's in demand</li>
            <li>🚀 Get personalized feedback to upskill smartly</li>
        </ul>
        <p><em>Designed with empathy, built with data.</em></p>
    </div>
    <div class='box'>
        <h3>👩‍💻 From the Developer</h3>
        <p>I'm Manju, an MBA student and an aspiring analyst. Like many of you, I’m on a job hunt journey filled with doubts and dreams. I built this app to turn my own job-search anxiety into something useful — something that gives clarity when you feel lost in a sea of skills and expectations.</p>
        <p>This app is more than a project. It’s a warm nudge from someone who’s figuring it out too.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Insights Tab ---
with tab2:
    st.subheader("What Skills Appear Most?")
    st.markdown("<div class='box'>Compare the top skills across resumes, job listings, and real-world hires.</div>", unsafe_allow_html=True)
    fig = px.bar(data, x="Skill", y=["Job Ads", "Resumes", "Hires"],
                 barmode="group", color_discrete_sequence=["#6a1b9a", "#ec407a", "#00bcd4"])
    fig.update_layout(xaxis_title="", yaxis_title="Frequency")
    st.plotly_chart(fig, use_container_width=True)

# --- Fit Score Tab ---
with tab3:
    st.subheader("🎯 Check Your Resume Fit")
    st.markdown("<div class='box'>Enter your skills and target role to calculate your resume fit score.</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        skill_input = st.text_input("Your skills (comma-separated)", "Excel, Python, Communication")
    with col2:
        role = st.selectbox("Target Role", list(roles.keys()))

    your_skills = set([s.strip().title() for s in skill_input.split(",")])
    needed = set(roles.get(role, []))
    matched = your_skills & needed
    missing = needed - your_skills
    score = int(100 * len(matched) / len(needed)) if needed else 0

    st.metric("Fit Score", f"{score}/100")
    if score == 100:
        st.success("You're a perfect match!")
    elif score >= 60:
        st.info(f"You're close. Just need to work on: {', '.join(missing)}")
    else:
        st.warning("You might want to learn these: " + ", ".join(missing))

# --- Suggestions Tab ---
with tab4:
    st.subheader("💡 Smart Suggestions")
    if missing:
        for skill in missing:
            st.markdown(f"<div class='box'><b>{skill}</b>: {advice.get(skill, 'Consider learning this skill.')}</div>", unsafe_allow_html=True)
    else:
        st.success("Nothing missing! You're job-ready ✨")

# --- About Tab ---
with tab5:
    st.subheader("ℹ️ About This App")
    st.markdown("""
    <div class='box'>
        <p>This app was built to support job seekers with real data and real talk. No buzzwords, no fluff — just honest, data-driven feedback on what recruiters actually value.</p>
        <p>Whether you're polishing your resume or preparing for your dream role, this tool is here to help you act smarter, not just hustle harder.</p>
        <p><i>Built with 💜 by Manju Singh, for every dreamer with a resume and a hope.</i></p>
    </div>
    """, unsafe_allow_html=True)
