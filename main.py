from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from email_function import Email
import functions_framework

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    email = Email()
    acc_scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    spreadsheetid = "1_lt5a0S2JfNrA7CcJkhQ-39BWbioNwRyAhi4arH0Ngw"
    # datarange needs to be updated every year to point to the correct sheet
    datarange = "2024-2025!B6:I13"  # https://developers.google.com/sheets/api/guides/concepts
    dateformat = "%d/%m/%Y"

    credentials = service_account.Credentials.from_service_account_file("sheets_creds.json", scopes=acc_scopes)
    service = build("sheets", "v4", credentials=credentials)

    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=spreadsheetid, range=datarange)
        .execute()
    )
    values = result.get("values", [])

    if not values:
        print("No data found.")
        exit()

    for row in values:
        isDue = datetime.strptime(row[6], dateformat) < datetime.now()
        print(row, "DueDate past:", isDue)
        if isDue and row[2] == "":
            email.send_mail(name = row[4], component=row[1], interestgroup=row[0], recipient=f"{row[3].lower()}@iittp.ac.in")


