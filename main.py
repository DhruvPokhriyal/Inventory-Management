from googleapiclient.discovery import build 
from google.oauth2 import service_account
from datetime import datetime
import smtplib

MY_EMAIL = "";
PASSWORD = "";

acc_scopes = ["https://www.googleapis.com/auth/spreadsheets"]
spreadsheetid = "1sRZsNiwImNwalonyiKfDyF0N9_UGduJBPYCDwbp-bos"
range = "Sheet1!A4:H" # https://developers.google.com/sheets/api/guides/concepts
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
    print(row, "Duedate past:", datetime.strptime(row[7], dateformat) < datetime.now())