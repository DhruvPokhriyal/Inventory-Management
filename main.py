from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from email_function import Email

email = Email()

acc_scopes = ["https://www.googleapis.com/auth/spreadsheets"]
spreadsheetid = "1sRZsNiwImNwalonyiKfDyF0N9_UGduJBPYCDwbp-bos"
# FIXME: Change variable name from range to anything else meaningful since it is shadowing built-in name range which
# might cause problem in future
range = "Sheet1!A4:H"  # https://developers.google.com/sheets/api/guides/concepts
dateformat = "%d/%m/%Y"

credentials = service_account.Credentials.from_service_account_file("creds.json", scopes=acc_scopes)
service = build("sheets", "v4", credentials=credentials)

sheet = service.spreadsheets()
result = (
    sheet.values()
    .get(spreadsheetId=spreadsheetid, range=range)
    .execute()
)
values = result.get("values", [])

if not values:
    print("No data found.")
    exit()

for row in values:
    isDue = datetime.strptime(row[7], dateformat) < datetime.now()
    print(row, "DueDate past:", isDue)
    if isDue:
        email.set_recipient(row[3])
        email.send_mail()

email.close_connection()
