import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

# --- Page Configuration ---
# This sets the title and icon of the browser tab, and uses a wide layout.
st.set_page_config(
    page_title="Indian Job Market Analyzer",
    page_icon="🇮🇳",
    layout="wide"
)

# --- Caching Data ---
# This is a key Streamlit feature. It prevents the app from reloading the
# data from the CSV file every single time a user interacts with a widget.
@st.cache_data
def load_data():
    """
    Loads data for the app. It first tries to load the full, dynamically
    generated dataset. If that fails (e.g., on the deployment server),
    it falls back to loading the pre-saved sample data.
    """
    try:
        # Try to load the main dataset first
        df = pd.read_csv('jobs_analyzed.csv')
    except FileNotFoundError:
        # If the main dataset is not found, show a message and load the sample
        st.info("💡 Displaying sample data. To see fresh insights, you can run the full data pipeline locally.")
        try:
            df = pd.read_csv('sample_data.csv')
        except FileNotFoundError:
            # If even the sample data is missing, return nothing.
            return None
            
    # The 'skills' column is saved as a string (e.g., "['python', 'sql']").
    # We need to use eval() to convert it back into a real Python list.
    df['skills'] = df['skills'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    return df

# --- Main Application ---
st.title("🇮🇳 Indian Job Market Analyzer for Data Roles")
st.markdown("This dashboard analyzes job listings to identify the most in-demand technical skills.")

df = load_data()

# --- Main Logic: Check if data is loaded before displaying the dashboard ---
if df is None:
    st.error("❌ ERROR: No data could be loaded. Please ensure `sample_data.csv` is in the GitHub repository or that you have run the full pipeline locally.")
elif df.empty:
    st.warning("⚠️ The loaded data is empty. No skills were found based on the analysis.")
else:
    # If data is loaded successfully, display the entire dashboard.
    
    st.header("📊 Overall Job Market Snapshot")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs with Skills", f"{len(df)}")
    
    # Flatten the list of lists into a single list of all skills
    all_skills = [skill for sublist in df['skills'] for skill in sublist]
    col2.metric("Unique Skills Identified", f"{len(set(all_skills))}")
    
    col3.metric("Unique Companies Hiring", f"{df['company'].nunique()}")

    st.header("🛠️ Most In-Demand Skills")
    
    # Count the frequency of each skill
    skill_counts = Counter(all_skills)
    top_skills_df = pd.DataFrame(skill_counts.most_common(10), columns=['Skill', 'Count'])
    
    # Create an interactive bar chart
    fig = px.bar(
        top_skills_df, 
        x='Count', 
        y='Skill', 
        orientation='h', 
        title='Top 10 Most In-Demand Skills',
        text='Count' # Show the count values on the bars
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}) # Sort the skills by count
    st.plotly_chart(fig, use_container_width=True)
    
    st.header("🏢 Top Hiring Companies")
    top_companies = df['company'].value_counts().nlargest(10).reset_index()
    top_companies.columns = ['Company', 'Number of Openings']
    st.dataframe(top_companies, use_container_width=True, hide_index=True)
    
    st.header("🔍 Explore Job Listings")
    
    all_unique_skills_sorted = sorted(list(set(all_skills)))
    
    # Make the default selection robust
    default_skills = [skill for skill in ['python', 'sql', 'tableau'] if skill in all_unique_skills_sorted]
    
    selected_skills = st.multiselect(
        "Filter jobs by skills (select one or more):",
        options=all_unique_skills_sorted,
        default=default_skills
    )

    if selected_skills:
        # Filter the DataFrame to show only jobs that contain ALL the selected skills
        filtered_df = df[df['skills'].apply(lambda x: set(selected_skills).issubset(set(x)))]
    else:
        # If no skills are selected, show all jobs
        filtered_df = df

    st.write(f"Showing {len(filtered_df)} jobs:")
    st.dataframe(filtered_df[['title', 'company', 'location', 'skills', 'link']], use_container_width=True, hide_index=True)