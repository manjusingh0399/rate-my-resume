import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Resume vs Reality", page_icon="🎯", layout="wide")

# --- Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Helvetica&display=swap');
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Helvetica', sans-serif;
    }
    .big-title {
        color: #5a189a;
        font-size: 2.5em;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.2em;
    }
    .tagline {
        color: #9d4edd;
        font-size: 1.2em;
        text-align: center;
        margin-bottom: 1.5em;
    }
    .box {
        background-color: white;
        border-left: 6px solid #9d4edd;
        padding: 1.2em;
        margin-bottom: 1em;
        border-radius: 10px;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Dummy Data ---
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Skill": ["Excel", "SQL", "Python", "Communication", "Teamwork", "Power BI", "Market Research"],
        "Category": ["Tool", "Tool", "Tool", "Soft Skill", "Soft Skill", "Tool", "Domain Knowledge"],
        "Job Ads": [92, 76, 68, 45, 41, 32, 29],
        "Resumes": [88, 49, 37, 93, 88, 27, 30],
        "Hires": [64, 54, 55, 37, 31, 18, 15]
    })

df = load_data()

# --- Tabs Layout ---
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Welcome", "📊 Skill Insights", "🔍 Skill Analyzer", "🎯 Fit Predictor"])

# --- Tab 1: Welcome ---
with tab1:
    st.markdown("<div class='big-title'>✨ Resume vs Reality</div>", unsafe_allow_html=True)
    st.markdown("<div class='tagline'>A career compass that cuts through resume buzzwords and shows what *actually* helps you get hired.</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='box'>
    <p>
    Hi! I’m <strong>Manju Singh</strong>, an MBA student with a passion for analytics, storytelling, and all things data. Like many of you, I’ve spent hours tweaking my resume, wondering which skills truly matter. Do recruiters care more about Excel or Power BI? Is teamwork overrated? Where does reality meet expectation?
    </p>
    <p>
    This project was born from that very anxiety — the invisible gap between what we <em>think</em> employers want and what actually drives hiring. It’s part career tool, part therapist, part data dashboard.
    </p>
    <p>
    You’ll see skills visualized, resume myths debunked, and maybe even a little spark of hope. This app is for anyone who’s stared at a job ad with sweaty palms and thought: <em>“Am I enough?”</em> Here’s your friendly data-driven answer. Let's turn confusion into clarity. 🌸
    </p>
    </div>
    """, unsafe_allow_html=True)

# --- Tab 2: Skill Insights ---
with tab2:
    st.header("📊 Skill Frequency & Value")
    cols = st.columns(3)
    with cols[0]:
        category_filter = st.selectbox("🔍 Filter by Skill Type", ["All"] + sorted(df["Category"].unique()))
    with cols[1]:
        top_n = st.slider("🎯 Top N Skills", 3, len(df), 7)
    with cols[2]:
        metric_choice = st.selectbox("📈 Sort By", ["Job Ads", "Resumes", "Hires"])

    if category_filter != "All":
        df_filtered = df[df["Category"] == category_filter]
    else:
        df_filtered = df.copy()

    df_top = df_filtered.sort_values(by=metric_choice, ascending=False).head(top_n)

    fig = px.bar(df_top, x="Skill", y=["Job Ads", "Resumes", "Hires"], barmode="group",
                 color_discrete_sequence=["#9d4edd", "#f72585", "#3a86ff"])
    fig.update_layout(title="📊 Skill Visibility Across Sources", xaxis_title=None, yaxis_title="Frequency")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='box'>💡 Some skills look great on paper but don’t translate to interviews. Watch for those that rank high in resumes but low in hiring!</div>", unsafe_allow_html=True)

# --- Tab 3: Skill Analyzer ---
with tab3:
    st.header("🔍 Select Skills to Analyze")

    df["Resume Inflation"] = (df["Resumes"] + 1) / (df["Job Ads"] + 1)
    df["Hiring Edge"] = (df["Hires"] + 1) / (df["Resumes"] + 1)

    st.markdown("Choose skills and see how they stack up in reality. Use this to reflect on your current resume keywords.")

    selected_skills = st.multiselect("Select skills", df["Skill"].tolist(), default=["Python", "Communication"])

    if selected_skills:
        insight_df = df[df["Skill"].isin(selected_skills)]
        st.write(insight_df[["Skill", "Job Ads", "Resumes", "Hires", "Resume Inflation", "Hiring Edge"]].reset_index(drop=True))

        fig2 = px.scatter(insight_df, x="Resume Inflation", y="Hiring Edge", text="Skill",
                          color="Category", size="Hires", hover_data=["Job Ads", "Resumes"])
        fig2.update_traces(textposition="top center")
        st.plotly_chart(fig2, use_container_width=True)

# --- Tab 4: Fit Predictor ---
with tab4:
    st.header("🎯 Your Resume Fit Score")
    st.markdown("Enter the skills you currently have and your target job type. We'll tell you how close you are to the real deal.")

    user_skills = st.text_input("🧾 List your skills (comma separated)", "Excel, Python, Communication")
    target_role = st.selectbox("Choose a job target", ["Analyst", "Marketing", "HR", "Sales"], key="rolepicker")

    role_skills = {
        "Analyst": ["Excel", "Python", "SQL"],
        "Marketing": ["Communication", "SEO", "Market Research"],
        "HR": ["Recruitment", "Communication", "Teamwork"],
        "Sales": ["Negotiation", "CRM", "Communication"]
    }

    if user_skills:
        user_set = set([x.strip().title() for x in user_skills.split(",")])
        target_set = set(role_skills.get(target_role, []))
        matched = user_set & target_set
        score = int((len(matched) / len(target_set)) * 100) if target_set else 0

        st.metric("💡 Resume Fit Score", f"{score}%")

        if score == 100:
            st.success("🌟 Perfect Match! You're ready to go.")
        elif score >= 60:
            st.info(f"You're close! Consider adding: {', '.join(target_set - matched)}")
        else:
            st.warning(f"You may want to focus on these: {', '.join(target_set - matched)}")
