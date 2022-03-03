from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import settings

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = settings.GOOGLE_SPREADSHEET_ID
RANGE = settings.GOOGLE_SHEETS_RANGE


def write_to_google(phone_number, username):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        
        values = [
            [phone_number, username],
            # Additional rows ...
        ]
        
        body = {
            'values': values
        }

        # Call the Sheets API
        sheet = service.spreadsheets()
        
        request = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE,
                                valueInputOption='RAW', body=body)

        while True:
            try:
                response = request.execute()
                break
            except TimeoutError:
                print('write failed, trying again')
                continue
        
        print(response)

    except HttpError as err:
        print(err)
        
        
def read_all_phone_numbers():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
    

        # Call the Sheets API
        sheet = service.spreadsheets()
        
        request = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE)

        while True:
            try:
                response = request.execute()
                break
            except TimeoutError:
                continue
        
        # print(response)
        
        phones_list = convert_to_single_list(response['values'])
        
        return phones_list

    except HttpError as err:
        print(err)


def convert_to_single_list(origin_list: list):
    phones_list = [row[0] for row in origin_list]
    return phones_list
        

if __name__ == '__main__':
    # write_to_google('123')
    print(read_all_phone_numbers())
