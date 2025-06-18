# --- parser.py ---
import pandas as pd
from bs4 import BeautifulSoup

def get_job_data(job_card):
    try:
        title_element = job_card.find('a', class_='jcs-JobTitle')
        job_title = title_element.text.strip()
        href = title_element.get('href')
        if href and href.startswith('/'):
            job_link = 'https://in.indeed.com' + href
        else:
            job_link = href
    except AttributeError:
        job_title, job_link = 'N/A', 'N/A'
    
    try:
        company_element = job_card.find(attrs={'data-testid': 'company-name'})
        company_name = company_element.text.strip() if company_element else 'N/A'
    except AttributeError:
        company_name = 'N/A'
        
    try:
        location_element = job_card.find(attrs={'data-testid': 'text-location'})
        company_location = location_element.text.strip() if location_element else 'N/A'
    except AttributeError:
        company_location = 'N/A'
        
    return {'title': job_title, 'company': company_name, 'location': company_location, 'link': job_link}

def parse_local_html(file_path='jobs.html'):
    all_jobs_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: The file '{file_path}' was not found. Please save the page from your browser first.")
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    job_title_anchors = soup.find_all('a', class_='jcs-JobTitle')
    
    if not job_title_anchors:
        print("ERROR: Could not find any job titles with class 'jcs-JobTitle'.")
        return None
        
    for anchor in job_title_anchors:
        job_card = anchor.find_parent('li')
        if job_card:
            job_data = get_job_data(job_card)
            if job_data['title'] != 'N/A':
                all_jobs_data.append(job_data)
                
    return all_jobs_data

if __name__ == "__main__":
    print("Step 1: Parsing local HTML file 'jobs.html'...")
    job_listings = parse_local_html()
    if job_listings:
        df = pd.DataFrame(job_listings)
        df.drop_duplicates(subset='link', inplace=True, keep='first')
        output_filename = 'indeed_jobs.csv'
        df.to_csv(output_filename, index=False)
        print(f"-> SUCCESS: Saved {len(df)} jobs to '{output_filename}'")