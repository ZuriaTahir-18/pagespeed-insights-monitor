# PageSpeed Insights to Google Sheets Monitor

This Python script automates the process of monitoring website performance. It fetches Core Web Vitals and other key metrics from the Google PageSpeed Insights API and logs them directly into a Google Sheet for analysis.

## 🚀 Features
- **Performance Tracking:** Captures CLS, TBT, SI, LCP, FCP, and Screen Type.
- **Automation:** Scheduled to run automatically every 4 hours.
- **Multithreading:** Handles multiple URLs concurrently for faster execution.
- **Google Sheets Integration:** Seamlessly appends data to your specified spreadsheet.
- **Error Logging:** Detailed logging to `pagespeed.log` for debugging.

## 📋 Metrics Collected
- URL & Date of Test
- Cumulative Layout Shift (CLS)
- Total Blocking Time (TBT)
- Speed Index (SI)
- Largest Contentful Paint (LCP)
- First Contentful Paint (FCP)
- Screen Type (Mobile/Desktop)

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.x installed.
- A Google Cloud Project with **PageSpeed Insights API** and **Google Sheets API** enabled.
- A Google Sheet (Create a blank sheet with headers in the first row).
- <img width="1920" height="414" alt="Screenshot (461)" src="https://github.com/user-attachments/assets/90bdc3dc-e5f1-40e7-888d-fcc61a8f55ff" />
### 2. Installation
Clone this repository:
```bash
git clone https://github.com/ZuriaTahir-18/pagespeed-insights-monitor.git
cd pagespeed-insights-monitor
```
## Install the required libraries:
pip install requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client schedule

### 3. Configuration (Where to put what?)
-Open main.py and update the following variables:

PAGESPEED_API_KEY:
-Go to Google Cloud Console.

Create an "API Key" and paste it here.

SHEET_ID:

-Open your Google Sheet in the browser.

Copy the long string in the URL between /d/ and /edit.

URLS_TO_TEST:

Add the list of websites you want to monitor.

### 4. Authentication (Google Sheets)

For security reasons, the credentials.json file is not included in this repository.

In Google Cloud Console, create a Service Account.

Download the JSON Key for that service account.

Rename the downloaded file to credentials.json and move it into the project folder.

Important: Copy the "Service Account Email" and Share your Google Sheet with this email as an Editor.

### 5. Running the Script

Start the monitor by running:
```bash
python main.py
```
