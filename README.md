# Snowbird (Unofficial) Patrol Dashboard

Link for Render: https://patroldashboard25.onrender.com/

Password protected - request password by messaging me on github or emailing me at mathieubfoucher@gmail.com 

## SOP: Deploying & Maintaining the Snowbird Patrol Dashboard

## Overview

This SOP describes how to set up, run, and extend the Snowbird Patrol Dashboard—a Streamlit-based web app that scrapes, processes, and visualizes live weather data from Snowbird’s weather stations. The dashboard is designed for ski patrol and operations teams to make fast, data-driven decisions.

---

## 1. Repository Structure

- `app.py` — Main Streamlit app and dashboard UI
- `scraper.py` — Scrapes and parses weather data from Snowbird patrol sites
- `utils.py` — Data formatting and visualization utilities

---

## 2. Prerequisites

- Python 3.8+
- Install required packages:
  ```bash
  pip install streamlit requests beautifulsoup4 pandas plotly gspread oauth2client

- (Optional) For Google Sheets integration, set up a service account and place your credentials file as needed.

---

## 3. Running the Dashboard

1. **Clone the repository** and navigate to the project directory.
2. **Start the app**:
   ```bash
   streamlit run app.py
   ```
3. The dashboard will open in your browser. You can now:
   - Select weather stations (PEAK, REDSTACK, etc.)
   - View live wind, temperature, and summary stats
   - Explore interactive visualizations (rose graphs, gauges, line charts)

---

## 4. How It Works

- **Data Scraping**:  
  `scraper.py` fetches and parses weather data from Snowbird patrol URLs using `requests` and `BeautifulSoup`, then structures it into Pandas DataFrames.
- **Data Processing & Visualization**:  
  `utils.py` provides functions to format time columns, plot wind gauges, rose graphs, and temperature trends using Plotly.
- **Dashboard UI**:  
  `app.py` ties everything together, handling user interaction, layout, and rendering all visualizations in Streamlit.

---

## 5. Security & Customization

- **Password Protection**:  
  There is commented-out code in `app.py` for password-protecting the dashboard using an environment variable. Uncomment and configure as needed for production.
- **Google Sheets Logging**:  
  `scraper.py` includes (commented) logic for logging data to Google Sheets. To enable, set up your service account and credentials, then uncomment and configure the relevant code.

---

## 6. Extending the Dashboard

- **Add new weather stations**: Update scraping logic and DataFrame processing in `scraper.py`.
- **Enable AI summaries**: Uncomment and configure the AI summary logic in `utils.py` for automated condition reports.
- **Deploy securely**: Consider deploying on Azure or another secure cloud platform for broader access and reliability.

---

## 7. Troubleshooting

- If data is missing or visualizations fail, check the source URLs and ensure the scraping logic matches the current HTML structure.
- For authentication or Google Sheets issues, verify your environment variables and credentials.




