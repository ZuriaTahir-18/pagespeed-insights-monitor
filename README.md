# Technical Documentation: PageSpeed Insights to Google Sheets Monitor

**Project Overview:**
This Python script automates the process of monitoring website performance. It fetches Core Web Vitals and other key metrics from the Google PageSpeed Insights API and logs them directly into a Google Sheet for analysis.

### 🚀 Key Features
- **Performance Tracking:** Captures essential metrics: CLS, TBT, SI, LCP, FCP, and Screen Type.
- **Multithreading (Bonus):** Utilizes `ThreadPoolExecutor` to handle multiple URLs and strategies (Mobile/Desktop) concurrently for faster execution.
- **Interactive CLI (Bonus):** Includes a Command Line Interface to manually run tests, add new URLs, or manage the background scheduler.
- **Automated Scheduling:** Built-in mechanism to run a full audit cycle every 4 hours.
- **Google Sheets Integration:** Seamlessly appends data to a specified spreadsheet.
- **Error Logging:** Detailed logging to `pagespeed.log` for debugging.

### 📋 Metrics Collected
- URL & Date of Test
- Cumulative Layout Shift (CLS)
- Total Blocking Time (TBT)
- Speed Index (SI)
- Largest Contentful Paint (LCP)
- First Contentful Paint (FCP)
- Screen Type (Mobile/Desktop)

### 🛠️ Setup & Installation Instructions

#### 1. Prerequisites
- Python 3.x installed on your system.
- A Google Cloud Project with **PageSpeed Insights API** and **Google Sheets API** enabled.
- A Google Sheet prepared with a header row (A1:H1).
  <img width="1897" height="355" alt="Screenshot (625)" src="https://github.com/user-attachments/assets/307b3fde-8a47-4c04-9d10-2bfdc32fd25f" />


#### 2. Installation
Clone the repository and install the required Python libraries:
```bash
git clone https://github.com/ZuriaTahir-18/pagespeed-insights-monitor.git
cd pagespeed-insights-monitor
pip install -r requirements.txt

```
### 3. Configuration
Open main.py and update the following variables:

PAGESPEED_API_KEY: Your Google API Key.

SHEET_ID: The ID of your Google Sheet.

URLS_TO_TEST: List of websites to monitor.

### 4. Authentication

Create a Service Account in Google Cloud and download the credentials.json.

Place it in the project folder.

Important: Share your Google Sheet with the Service Account email as an Editor.

### 5. Running the Script

Start the application by running:
``` bash 
python main.py

```

### Upon execution, use the interactive menu:
Press "1" for an immediate test.
Press "2" to add a new URL.
Press "4" to start the 4-hour automation.

