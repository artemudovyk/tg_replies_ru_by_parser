import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SPREADSHEET_ID=os.getenv('GOOGLE_SPREADSHEET_ID')
GOOGLE_SHEETS_RANGE=os.getenv('GOOGLE_SHEETS_RANGE')
TELEGRAM_API_ID=os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH=os.getenv('TELEGRAM_API_HASH')