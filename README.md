
PageSpeed Insights to Google Sheets Monitor
This automated monitoring tool is designed to fetch Core Web Vitals (CLS, TBT, Speed Index, LCP, FCP) and performance metrics from the Google PageSpeed Insights API and log them directly into Google Sheets. It features built-in Multithreading to handle multiple URLs concurrently, a 4-hour automated scheduler, and detailed error logging to pagespeed.log for reliable performance tracking across both Mobile and Desktop views.
🚀 Setup & Installation Guide
To get started, ensure you have Python 3.x installed on your system. First, clone this repository and install the necessary dependencies:
code
Bash
git clone https://github.com/ZuriaTahir-18/pagespeed-insights-monitor.git
cd pagespeed-insights-monitor
pip install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client schedule
⚙️ Configuration & Authentication
Before running the script, you need to configure your environment in the main.py file and set up Google Cloud credentials:
API Key: Enable the PageSpeed Insights API in your Google Cloud Console, generate an "API Key," and paste it into the PAGESPEED_API_KEY variable.
Google Sheets Setup: Enable the Google Sheets API, create a Service Account, and download the JSON key. Rename this file to credentials.json and place it in the project folder. Important: Share your Google Sheet with the Service Account email as an Editor.
Variable Updates: Inside main.py, update SHEET_ID (the long string in your sheet's URL) and add your target websites to the URLS_TO_TEST list.
<img width="1920" height="414" alt="Screenshot (461)" src="https://github.com/user-attachments/assets/90bdc3dc-e5f1-40e7-888d-fcc61a8f55ff" />
🏃 Execution
Once configured, start the automated monitor by running:
code
Bash
python main.py
The script will immediately perform an initial audit of all URLs and then continue to run every 4 hours, appending the latest performance data (URL, Date, CLS, TBT, Speed Index, LCP, FCP, and Screen Type) to your spreadsheet.
