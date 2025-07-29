import streamlit as st
import pandas as pd
import plotly.express as px

# -- Load enriched skills data
@st.cache_data
def load_data():
    return pd.read_csv("enriched_skills_data.csv")

df = load_data()

# -- App layout setup
st.set_page_config(
    page_title="Resume vs Reality",
    layout="wide",
    page_icon="🎯"
)

# -- Global Colors and Fonts
st.markdown("""
    <style>
    html, body {
        font-family: 'Helvetica', sans-serif;
        background-color: #f9f9f9;
        color: #333;
    }
    .big-title {
        font-size: 40px;
        font-weight: bold;
        color: #ff4da6;
        text-align: center;
        margin-top: 20px;
    }
    .tagline {
        font-size: 18px;
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }
    .section {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# -- Main Title
st.markdown('<div class="big-title">💡 Resume vs Reality</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Your friendly compass through the hiring maze — backed by real data, designed for dreamers & doers.</div>', unsafe_allow_html=True)

# -- Tabs Layout
tabs = st.tabs(["🏠 Welcome", "📊 Insights", "🧠 Role Fit & Score", "🔍 Custom Prediction", "💬 About"])

# -------- TAB 1: WELCOME --------
with tabs[0]:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("## 👋 Welcome to Resume vs Reality")
    st.write("""
    Have you ever wondered whether the skills on your resume really align with what hiring managers want?

    As an **MBA student myself**, I’ve felt the anxiety of trying to guess what skills to highlight. That’s why I built this app — to help job seekers **see through the fog** using actual data from:
    - Real **job listings**
    - Actual **resumes**
    - Profiles of **hired candidates**

    💖 Think of this app as your wiser, tech-savvy older sister telling you: “That’s cute, but SQL is what’ll get you hired.”

    🔄 Navigate through the tabs to:
    - Explore **trending and overhyped skills**
    - Get a **score on your skill set** for different roles
    - Predict your **probability of getting hired**

    Let's channel the stress into clarity and confidence. ✨
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# -------- TAB 2: INSIGHTS --------
with tabs[1]:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("📊 Insights: What Skills Really Matter?")
    category_filter = st.multiselect("🎯 Filter by Skill Category", df['Category'].unique(), default=df['Category'].unique())

    filtered = df[df['Category'].isin(category_filter)]

    fig = px.bar(filtered.sort_values("Job Ads", ascending=False).head(15),
                 x="Skill", y=["Job Ads", "Resumes", "Hires"],
                 barmode="group",
                 color_discrete_sequence=["#ff4da6", "#ffc107", "#8bc34a"],
                 title="Top Skills by Appearance in Job Ads, Resumes & Hires")

    fig.update_layout(xaxis_title="", yaxis_title="Frequency", plot_bgcolor="#fafafa")
    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 Insight: Skills like Python and SQL appear in fewer resumes than expected — yet are consistently present in hires!")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- TAB 3: ROLE FIT SCORE --------
with tabs[2]:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("🧠 Role Fit Score")
    role_skills = {
        "Analyst": ["SQL", "Python", "Excel", "Power BI", "Data Visualization"],
        "Marketing": ["SEO", "Canva", "Market Research", "Creativity", "Social Media"],
        "HR": ["Recruitment", "Communication", "Teamwork", "Leadership"],
        "Sales": ["Negotiation", "CRM", "Time Management", "Presentation Skills"]
    }

    role = st.selectbox("Choose a job role:", list(role_skills.keys()))
    user_input = st.text_input("🔍 Enter your skills (comma-separated)", placeholder="e.g., Python, Excel, Communication")

    if user_input:
        user_set = set([s.strip().title() for s in user_input.split(',')])
        role_set = set(role_skills[role])
        match = user_set & role_set
        missing = role_set - user_set

        score = round((len(match) / len(role_set)) * 100)
        st.metric(label="💼 Fit Score", value=f"{score}%", delta_color="normal")

        st.success(f"✅ Matched Skills: {', '.join(match) if match else 'None'}")
        st.warning(f"📌 Missing Key Skills for {role}: {', '.join(missing) if missing else 'None'}")

        if score < 70:
            st.info("📘 Pro Tip: Consider learning these to boost your profile!")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- TAB 4: CUSTOM PREDICTION --------
with tabs[3]:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("🔍 Predict Hiring Probability")

    input_skills = st.multiselect("Select your current skills:", options=sorted(df["Skill"].unique()))
    top_hire_avg = df[df["Hires"] > df["Hires"].mean()]

    if input_skills:
        match_count = sum([1 for skill in input_skills if skill in top_hire_avg["Skill"].values])
        prediction_score = int((match_count / len(top_hire_avg)) * 100)
        st.metric("📈 Predicted Hiring Score", f"{prediction_score}%", delta=None)

        st.info(f"🧠 {match_count} of your skills are frequently seen among hired profiles.")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- TAB 5: ABOUT --------
with tabs[4]:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("💬 About This Project")
    st.write("""
    - 🔧 **Built by**: Manju Singh, an MBA student with a deep interest in data, design & decision-making.
    - 🎯 **Purpose**: To demystify the resume-writing process by helping others visualize what skills matter most — based on hiring data.
    - 📌 **Technologies Used**: Streamlit, Plotly, Pandas

    ❤️ If this app gave you even a tiny bit of clarity, consider sharing it with someone else staring at a blank resume right now.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
