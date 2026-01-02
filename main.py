import requests
import logging
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import schedule
import time
import sys
from concurrent.futures import ThreadPoolExecutor

# ============================================
# 1. WINDOWS TERMINAL CONFIGURATION
# ============================================
# Fix for encoding issues on Windows terminals to ensure logs display correctly.
if sys.platform == "win32":
    import os
    os.system('chcp 65001')

# ============================================
# 2. LOGGING CONFIGURATION
# ============================================
# Configures logging to both a file ('pagespeed.log') and the standard output (terminal).
# This helps in debugging and tracking the history of the script's execution.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pagespeed.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# 3. CONFIGURATION & ACCESS KEYS
# ============================================
# Assumption: The user has set up a Google Cloud Project with PageSpeed and Sheets API enabled.
# Assumption: The 'credentials.json' is present in the root folder with proper service account permissions.
PAGESPEED_API_KEY = 'API Key '  # Placeholder for GitHub Security
SHEET_ID = 'SHEET ID'          # Placeholder for GitHub Security
CREDENTIALS_FILE = 'credentials.json'
SCOPES = ['Scope']

# List of URLs to monitor (Can be modified via the CLI bonus feature)
URLS_TO_TEST = ['https://buildberg.co/']

def get_pagespeed_data(url, strategy='mobile'):
    """
    Fetches raw performance data from the Google PageSpeed Insights API.
    :param url: The website URL to analyze.
    :param strategy: Either 'mobile' or 'desktop'.
    :return: JSON response from the API or None if failed.
    """
    try:
        logger.info(f"Testing {url} on {strategy} strategy...")
        api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            'url': url,
            'strategy': strategy,
            'category': 'performance',
            'key': PAGESPEED_API_KEY 
        }
        # Increased timeout to 120s as PageSpeed audits can take a significant amount of time.
        response = requests.get(api_url, params=params, timeout=120)
        response.raise_for_status() 
        return response.json()
    except Exception as e:
        logger.error(f"API Request Failed for {url} ({strategy}): {str(e)}")
        return None

def extract_metrics(api_response, url, strategy):
    """
    Parses the complex JSON response to extract specific Core Web Vitals and performance metrics.
    """
    try:
        if not api_response: return None
        
        # Accessing the 'audits' section of the Lighthouse result
        audits = api_response['lighthouseResult']['audits']
        
        metrics = {
            'URL': url,
            'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'CLS': round(audits.get('cumulative-layout-shift', {}).get('numericValue', 0), 3),
            'TBT': round(audits.get('total-blocking-time', {}).get('numericValue', 0), 2),
            'SI': round(audits.get('speed-index', {}).get('numericValue', 0), 2),
            'LCP': round(audits.get('largest-contentful-paint', {}).get('numericValue', 0), 2),
            'FCP': round(audits.get('first-contentful-paint', {}).get('numericValue', 0), 2),
            'Screen': strategy.capitalize()
        }
        return metrics
    except KeyError as e:
        logger.error(f"Data extraction failed. Key not found: {str(e)}")
        return None

def write_to_google_sheets(m):
    """
    Appends the extracted metrics as a new row in the specified Google Sheet.
    """
    if not m: return
    try:
        # Load credentials and build the Google Sheets service
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        
        # Prepare data in row format
        row_data = [[m['URL'], m['Date'], m['CLS'], m['TBT'], m['SI'], m['LCP'], m['FCP'], m['Screen']]]
        
        # Call the Sheets API to append data at the end of Sheet1
        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range='Sheet1!A:H',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': row_data}
        ).execute()
        logger.info(f"Successfully logged data to Google Sheets for {m['URL']}")
    except Exception as e:
        logger.error(f"Google Sheets API Error: {str(e)}")

def process_single_task(url, strategy):
    """
    Wrapper function to handle the full flow for a single URL/Strategy combination.
    Needed for the Multithreading implementation.
    """
    data = get_pagespeed_data(url, strategy)
    if data:
        metrics = extract_metrics(data, url, strategy)
        write_to_google_sheets(metrics)

def run_monitoring_cycle():
    """
    BONUS: Implements Multithreading using ThreadPoolExecutor to handle 
    multiple URLs and strategies concurrently, significantly reducing total execution time.
    """
    logger.info("--- Starting New Performance Monitoring Cycle ---")
    
    # We use max_workers=4 to process multiple requests in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        for url in URLS_TO_TEST:
            executor.submit(process_single_task, url, 'mobile')
            executor.submit(process_single_task, url, 'desktop')

# ============================================
# 4. COMMAND LINE INTERFACE (BONUS)
# ============================================
def start_app():
    """
    BONUS: Simple CLI to allow the user to manage URLs and start the automation.
    """
    while True:
        print("\n--- PageSpeed Insights Monitor Menu ---")
        print("1. Run Performance Test Now")
        print("2. Add URL to Test List")
        print("3. View Current URL List")
        print("4. Start Automation (Runs every 4 hours)")
        print("5. Exit")
        
        user_input = input("Selection: ")

        if user_input == '1':
            run_monitoring_cycle()
        elif user_input == '2':
            new_url = input("Enter website URL (including https://): ")
            URLS_TO_TEST.append(new_url)
            print(f"URL added to monitoring list.")
        elif user_input == '3':
            print(f"\nMonitoring list: {URLS_TO_TEST}")
        elif user_input == '4':
            print("Scheduler activated. Script will run every 4 hours. Press Ctrl+C to stop.")
            # Task Requirement: Schedule every 4 hours
            schedule.every(4).hours.do(run_monitoring_cycle)
            run_monitoring_cycle() # Run immediately for the first time
            while True:
                schedule.run_pending()
                time.sleep(60)
        elif user_input == '5':
            print("Exiting application...")
            break
        else:
            print("Invalid input. Please choose 1-5.")

if __name__ == "__main__":
    try:
        start_app()
    except KeyboardInterrupt:
        logger.info("Application closed by user.")
    except Exception as fatal_error:
        logger.fatal(f"A critical error occurred: {fatal_error}")