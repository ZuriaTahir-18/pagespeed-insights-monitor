import requests
import logging
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import schedule
import time
import sys

# Windows terminal encoding fix
if sys.platform == "win32":
    import os
    os.system('chcp 65001')

# ============================================
# LOGGING SETUP (Simple Text - No Emojis)
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('pagespeed.log', encoding='utf-8'), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ============================================
# CONFIGURATION
# ============================================
PAGESPEED_API_KEY = 'Your API Key' 
SHEET_ID = ''
CREDENTIALS_FILE = 'Credential File'
SCOPES = ['scope']
URLS_TO_TEST = ['url']

def get_pagespeed_data(url, strategy='mobile'):
    try:
        logger.info(f"Testing {url} on {strategy}...")
        api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            'url': url,
            'strategy': strategy,
            'category': 'performance',
            'key': PAGESPEED_API_KEY 
        }
        response = requests.get(api_url, params=params, timeout=90)
        response.raise_for_status()
        logger.info(f"Data received for {url} ({strategy})")
        return response.json()
    except Exception as e:
        logger.error(f"API Error for {url}: {str(e)}")
        raise

def extract_metrics(api_response, url, strategy):
    try:
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
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        raise

def write_to_google_sheets(m):
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        row = [[m['URL'], m['Date'], m['CLS'], m['TBT'], m['SI'], m['LCP'], m['FCP'], m['Screen']]]
        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range='Sheet1!A:H',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': row}
        ).execute()
        logger.info(f"Data written to Sheet for {m['Screen']}")
    except Exception as e:
        logger.error(f"Sheets Error: {str(e)}")

def run_pagespeed_test():
    logger.info("Starting PageSpeed test cycle...")
    for url in URLS_TO_TEST:
        for strategy in ['mobile', 'desktop']:
            try:
                data = get_pagespeed_data(url, strategy)
                metrics = extract_metrics(data, url, strategy)
                write_to_google_sheets(metrics)
                time.sleep(5)
            except Exception as e:
                logger.error(f"{strategy.capitalize()} test failed: {e}")

if __name__ == "__main__":
    try:
        logger.info("PageSpeed Monitor Started")
        run_pagespeed_test()
        schedule.every(4).hours.do(run_pagespeed_test)
        logger.info("Waiting for next run (every 4 hours)...")
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
