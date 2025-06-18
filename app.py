# --- app.py ---
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

st.set_page_config(page_title="Indian Job Market Analyzer", page_icon="🇮🇳", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('jobs_analyzed.csv')
        df['skills'] = df['skills'].apply(lambda x: eval(x) if isinstance(x, str) else x)
        return df
    except FileNotFoundError:
        return None

st.title("🇮🇳 Indian Job Market Analyzer for Data Roles")
st.markdown("This dashboard analyzes job market data to identify the most in-demand skills.")

df = load_data()

if df is None:
    st.error("❌ ERROR: The 'jobs_analyzed.csv' file was not found. Please run the data pipeline first (parser -> analyzer).")
elif df.empty:
    st.warning("⚠️ The analyzed data is empty. No skills were found in the job titles.")
else:
    st.header("📊 Overall Job Market Snapshot")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs with Skills", f"{len(df)}")
    all_skills = [skill for sublist in df['skills'] for skill in sublist]
    col2.metric("Unique Skills Identified", f"{len(set(all_skills))}")
    col3.metric("Unique Companies Hiring", f"{df['company'].nunique()}")

    st.header("🛠️ Most In-Demand Skills")
    skill_counts = Counter(all_skills)
    top_skills_df = pd.DataFrame(skill_counts.most_common(10), columns=['Skill', 'Count'])
    fig = px.bar(top_skills_df, x='Count', y='Skill', orientation='h', title='Top 10 Most In-Demand Skills', text='Count')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.header("🏢 Top Hiring Companies")
    top_companies = df['company'].value_counts().nlargest(10).reset_index()
    top_companies.columns = ['Company', 'Number of Openings']
    st.dataframe(top_companies, use_container_width=True, hide_index=True)
    
    st.header("🔍 Explore Job Listings")
    all_unique_skills_sorted = sorted(list(set(all_skills)))
    default_skills = [skill for skill in ['python', 'sql', 'tableau'] if skill in all_unique_skills_sorted]
    selected_skills = st.multiselect("Filter jobs by skills:", options=all_unique_skills_sorted, default=default_skills)

    if selected_skills:
        filtered_df = df[df['skills'].apply(lambda x: set(selected_skills).issubset(set(x)))]
    else:
        filtered_df = df

    st.write(f"Showing {len(filtered_df)} jobs:")
    st.dataframe(filtered_df[['title', 'company', 'location', 'skills', 'link']], use_container_width=True, hide_index=True)