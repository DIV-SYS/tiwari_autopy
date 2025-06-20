import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CRED_PATH = 'permit_automation/creds/service-account.json'
SHEET_NAME = 'TDEC_TEST_SHEET'

def connect_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CRED_PATH, SCOPE)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).worksheet('Sheet2')

def get_permit_ids():
    sheet = connect_sheet()
    records = sheet.get_all_records()
    return [(row['Permit ID'], idx + 2) for idx, row in enumerate(records)]

def update_sheet_link(row, link):
    sheet = connect_sheet()
    sheet.update_cell(row, 2, link)
