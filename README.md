# Technical Documentation: PageSpeed Insights to Google Sheets Monitor
Project Overview:
This Python script automates the process of monitoring website performance. It fetches Core Web Vitals and other key metrics from the Google PageSpeed Insights API and logs them directly into a Google Sheet for analysis. This tool is designed for developers and SEO specialists who need to track performance trends over time without manual intervention.
🚀 Key Features:
Performance Tracking: Captures essential metrics: CLS, TBT, SI, LCP, FCP, and Screen Type.
Multithreading (Bonus): Utilizes ThreadPoolExecutor to handle multiple URLs and strategies (Mobile/Desktop) concurrently. This ensures faster execution and avoids bottlenecks when monitoring multiple sites.
Interactive CLI (Bonus): Includes a Command Line Interface that allows users to manually run tests, add new URLs to the test list dynamically, and manage the background scheduler.
Automated Scheduling: Built-in mechanism to run a full audit cycle every 4 hours.
Google Sheets Integration: Seamlessly appends data to a specified spreadsheet using the Google Sheets API.
Error Logging: Detailed logging to pagespeed.log for debugging and process tracking.
📋 Metrics Collected:
URL & Date of Test
Cumulative Layout Shift (CLS)
Total Blocking Time (TBT)
Speed Index (SI)
Largest Contentful Paint (LCP)
First Contentful Paint (FCP)
Screen Type (Mobile/Desktop)
🛠️ Setup & Installation Instructions:
1. Prerequisites:
Python 3.x installed on your system.
A Google Cloud Project with PageSpeed Insights API and Google Sheets API enabled.
A Google Sheet prepared with a header row in the first line (A1:H1).
2. Installation:
Clone the repository and install the required Python libraries:
code
Bash
git clone https://github.com/ZuriaTahir-18/pagespeed-insights-monitor.git
cd pagespeed-insights-monitor
pip install requests google-auth google-api-python-client schedule
3. Configuration (Where to put what?):
Open main.py and update the following configuration variables:
PAGESPEED_API_KEY: Generate an "API Key" from the Google Cloud Console (APIs & Services > Credentials).
SHEET_ID: Copy the ID from your Google Sheet URL (the string between /d/ and /edit).
URLS_TO_TEST: Add your initial list of websites in the Python list.
4. Authentication (Google Sheets):
In the Google Cloud Console, create a Service Account and download the JSON Private Key.
Rename the file to credentials.json and place it in the project folder.
Crucial Step: Copy the service account email address and Share your Google Sheet with this email as an Editor.
5. Running the Script:
Start the application by running:
code
Bash
python main.py
Upon execution, an interactive menu will appear. You can press "1" to run an immediate test, "2" to add a new URL, or "4" to start the 4-hour automated monitoring cycle.
📝 Assumptions & Security:
Security: For GitHub submissions, the credentials.json file and sensitive API keys should be excluded from the repository.
Format: The script assumes the target sheet is named "Sheet1" and appends data starting from Column A to H.
Performance: A timeout of 120 seconds is set for API calls to allow Lighthouse to complete deep audits of heavy websites.
