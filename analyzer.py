# --- analyzer.py (Final Version - Analyzing Titles) ---
import pandas as pd
from collections import Counter

SKILLS_LIST = [
    'python', 'r', 'sql', 'sas', 'matlab', 'java', 'c++', 'scala', 'julia',
    'excel', 'tableau', 'power bi', 'powerbi', 'qlik', 'd3.js', 'looker',
    'hadoop', 'spark', 'hive', 'pig', 'aws', 'azure', 'gcp',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
    'git', 'docker', 'agile', 'scrum'
]

def load_data(input_csv='indeed_jobs.csv'):
    """Loads the initial data with job titles from the parser."""
    try:
        df = pd.read_csv(input_csv)
        df['title'] = df['title'].astype(str).fillna('')
        return df
    except FileNotFoundError:
        print(f"ERROR: Input file '{input_csv}' not found. Please run parser.py first.")
        return None

def extract_skills_from_title(title):
    """Finds skills from our list that are mentioned in the job title."""
    found_skills = set()
    title_lower = title.lower()
    for skill in SKILLS_LIST:
        if skill in title_lower:
            if skill == 'r' and not (' r ' in title_lower or title_lower.endswith(' r') or title_lower.startswith('r ')):
                continue
            found_skills.add(skill.replace('powerbi', 'power bi'))
    return list(found_skills)

if __name__ == "__main__":
    print("Step 2: Analyzing Job TITLES for skills...")
    df = load_data()
    if df is not None:
        df['skills'] = df['title'].apply(extract_skills_from_title)
        df_skills = df[df['skills'].apply(lambda x: len(x) > 0)].copy()
        output_filename = 'jobs_analyzed.csv'
        df_skills.to_csv(output_filename, index=False)
        print(f"\n-> SUCCESS! Title Analysis Complete! Found skills in {len(df_skills)} titles.")
        print(f"   Saved data to '{output_filename}'")