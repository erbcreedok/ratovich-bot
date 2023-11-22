from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

def save_data(data):
    # Set up the credentials
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = './service_account.json'

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID of your spreadsheet
    SPREADSHEET_ID = '10zzl13AWTMWJgC9asFebhuejvwGWxLZa6nwNuMNggtc'

    service = build('sheets', 'v4', credentials=credentials)

    # Data to be added as a new row
    new_row_data = [
        data['action'],
        data['name'],
        data['age'],
        data['city'],
        data['level'],
        data['location'],
        data['price'],
        data['phone'],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Formatting the datetime
    ]

    body = {
        'values': [new_row_data]
    }
    range_ = 'All Data' 
    value_input_option = 'USER_ENTERED'
    request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=range_,
                                                     valueInputOption=value_input_option, body=body, insertDataOption="INSERT_ROWS")
    response = request.execute()

    print('Row added to Sheet:', response)
