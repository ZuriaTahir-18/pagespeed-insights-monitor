# PageSpeed Insights to Google Sheets Monitor

This Python script automates the process of monitoring website performance. It fetches Core Web Vitals and other key metrics from the Google PageSpeed Insights API and logs them directly into a Google Sheet for analysis.

## 🚀 Features
- **Performance Tracking:** Captures CLS, TBT, SI, LCP, FCP, and Screen Type.
- **Automation:** Scheduled to run automatically every 4 hours.
- **Multithreading:** Handles multiple URLs concurrently for faster execution (Bonus Feature).
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
- A Service Account `credentials.json` file.
- A Google Sheet (Share it with your Service Account Email).

### 2. Installation
Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/pagespeed-insights-monitor.git
cd pagespeed-insights-monitor
