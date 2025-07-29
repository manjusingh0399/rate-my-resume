import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Resume vs Reality", page_icon="📄", layout="wide")

# -------------------------------
# CUSTOM STYLING
# -------------------------------
st.markdown("""
    <style>
    html, body {
        font-family: 'Helvetica', sans-serif;
        background-color: #fefefe;
        color: #333333;
    }
    .big-title {
        font-size: 2.4em;
        font-weight: bold;
        color: #ff4da6;
        margin-top: 0.5em;
    }
    .tagline {
        font-size: 1.2em;
        color: #ff944d;
        margin-bottom: 1.5em;
    }
    .section-box {
        background-color: #fff6fb;
        border-left: 6px solid #ff4da6;
        padding: 1.2em;
        margin-bottom: 1.2em;
        border-radius: 10px;
    }
    .stTabs [role="tab"] {
        background: #ffe0f0;
        color: black;
        font-weight: bold;
        border-radius: 10px 10px 0 0;
        margin-right: 8px;
    }
    .stTabs [aria-selected="true"] {
        background: #ff4da6;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# SAMPLE DATA
# -------------------------------
@st.cache_data
def load_data():
    data = {
        "Skill": [
            "Python", "SQL", "Excel", "Communication", "Teamwork", "Power BI",
            "Market Research", "SEO", "Canva", "Recruitment", "Negotiation",
            "CRM", "Time Management", "Leadership", "Data Visualization", "Creativity",
            "Presentation Skills"
        ],
        "Job Ads": [80, 75, 70, 68, 65, 60, 58, 55, 52, 50, 48, 47, 45, 42, 40, 39, 38],
        "Resumes": [60, 50, 72, 90, 88, 40, 35, 48, 30, 55, 60, 50, 44, 41, 30, 60, 39],
        "Hires": [75, 70, 65, 60, 55, 58, 40, 42, 29, 50, 55, 45, 38, 39, 48, 34, 33],
        "Category": [
            "Technical", "Technical", "Technical", "Soft Skill", "Soft Skill", "Technical",
            "Analytical", "Marketing", "Marketing", "HR", "Sales", "Sales", "Productivity",
            "Leadership", "Data", "Creativity", "Presentation"
        ]
    }
    return pd.DataFrame(data)

skills_df = load_data()

# -------------------------------
# SIDEBAR FOR FILTERS
# -------------------------------
st.sidebar.title("🔍 Filters")
category_filter = st.sidebar.multiselect(
    "Select Skill Categories",
    options=skills_df["Category"].unique(),
    default=skills_df["Category"].unique()
)

filtered_df = skills_df[skills_df["Category"].isin(category_filter)]

# -------------------------------
# TABS UI
# -------------------------------
tabs = st.tabs(["🏠 Welcome", "📊 Skill Reality", "🎯 Score Check"])

# -------------------------------
# WELCOME TAB
# -------------------------------
with tabs[0]:
    st.markdown("<div class='big-title'>Resume vs Reality</div>", unsafe_allow_html=True)
    st.markdown("<div class='tagline'>What we list. What they want. What actually gets you hired.</div>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class='section-box'>
        👋 Welcome! This app helps job seekers understand which skills matter the most in the hiring process.
        
        You'll explore how your **resume aligns with job postings** and what people who get hired usually have on their resumes.

        As the developer (and a fellow MBA student 😅), I built this because I’ve personally felt the anxiety of job hunting. This app is like a flashlight in the dark job market, giving you **insights, encouragement**, and **real data**.

        Let's channel our stress into strategy! 🚀
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class='section-box'>
        🧭 **How to use this app:**
        - Go to **Skill Reality** to see which skills are common in resumes vs hiring vs job ads
        - Try **Score Check** to input your own skills and see your match with job expectations
        - Use sidebar to filter by skill categories like Technical, Soft Skills, Marketing, etc.
        </div>
    """, unsafe_allow_html=True)

# -------------------------------
# INSIGHTS TAB
# -------------------------------
with tabs[1]:
    st.markdown("## 📊 Skill Popularity & Reality")

    fig = px.bar(
        filtered_df.sort_values("Job Ads", ascending=False),
        x="Skill", y=["Job Ads", "Resumes", "Hires"],
        barmode="group", text_auto=True,
        color_discrete_sequence=["#ff944d", "#d63384", "#007bff"]
    )
    fig.update_layout(title="Skill Mentions in Job Ads vs Resumes vs Hires", xaxis_title="", yaxis_title="Frequency")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        <div class='section-box'>
        💡 <b>Insight:</b> Some skills like Python and SQL are underrepresented in resumes but highly sought in job ads and present in hires. On the other hand, soft skills like "Teamwork" and "Communication" are heavily listed but don't always give you a hiring edge.
        </div>
    """, unsafe_allow_html=True)

# -------------------------------
# SCORE CHECK TAB
# -------------------------------
with tabs[2]:
    st.markdown("## 🎯 Check Your Resume Fit")
    st.markdown("Type the skills from your resume and see how well you align with actual job expectations.")

    user_input = st.text_input("🔠 Enter your skills (comma-separated)", "Python, Excel, Teamwork")
    user_skills = [x.strip().title() for x in user_input.split(",") if x.strip()]

    if user_skills:
        match = skills_df[skills_df["Skill"].isin(user_skills)]
        total = len(user_skills)
        matched = len(match)
        score = round((matched / total) * 100) if total > 0 else 0

        st.metric("📈 Resume Match Score", f"{score}%")
        
        missing = [s for s in user_skills if s not in skills_df["Skill"].values]
        matched_skills = ", ".join(match["Skill"].tolist()) or "None"

        st.markdown(f"<b>✅ Recognized Skills:</b> {matched_skills}", unsafe_allow_html=True)
        if missing:
            st.markdown(f"<b>⚠️ Not in hiring data:</b> {', '.join(missing)}", unsafe_allow_html=True)

        st.markdown("""
            <div class='section-box'>
            🎯 Your score tells you how well your listed skills match up with real-world job needs. It's not perfect—but it's a start! Consider brushing up on the top-demand skills from earlier tabs.
            </div>
        """, unsafe_allow_html=True)

# -------------------------------
# END
# -------------------------------
