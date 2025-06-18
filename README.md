# AI-Powered Indian Job Market Analyzer

This project is an end-to-end data analytics application that scrapes job postings for data roles in India, analyzes the job titles to extract key skills, and displays the findings in an interactive web dashboard built with Streamlit.

**[>> View the Live Deployed App Here! <<](https://your-app-url-will-go-here.streamlit.app)**

---

## Project Story
The initial goal was to scrape full job descriptions from Indeed. However, after developing a robust scraper with Selenium, I encountered advanced, dynamic anti-bot measures that made full-text scraping unreliable. 

Demonstrating a key data science skill—**adapting to real-world data limitations**—I pivoted the project's strategy. The final, successful approach focuses on parsing job **titles** for technical skills, which proved to be a more robust and consistent method for gathering insights. This entire journey reflects a realistic, problem-solving approach to data projects.

## Features
- **Data Acquisition:** A manual-first approach to bypass CAPTCHA, with automated parsing using Python and BeautifulSoup.
- **Skill Extraction:** A custom script to parse job titles for over 30 pre-defined technical skills.
- **Interactive Dashboard:** A dynamic and filterable front-end built with Streamlit and Plotly Express to visualize the findings.

## Tech Stack
- **Language:** Python
- **Data Manipulation:** Pandas
- **Web Parsing:** BeautifulSoup4
- **Dashboarding:** Streamlit, Plotly Express

## How to Run Locally
1. Clone the repository: `git clone [your-repo-url]`
2. Set up a Python 3.11 virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Manually save the target job search page as `jobs.html` in the root directory.
5. Run the data pipeline:
   ```bash
   python parser.py
   python analyzer.py