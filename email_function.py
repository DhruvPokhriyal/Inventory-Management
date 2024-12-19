import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os
from google.auth.transport.requests import Request

with open("email_content.txt") as file:
    msg_content = file.read()

msg_subject = "Item Return"

SERVICE_ACCOUNT_FILE = "creds.json"
IMPERSONATED_USER = "techmaniacs@iittp.ac.in"
SCOPES = ["https://mail.google.com", "https://www.googleapis.com/auth/gmail.send"]


def create_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


class Email:
    def __init__(self):
        self.service = create_gmail_service()
        self.msg = MIMEText(msg_content)
        self.msg['from'] = IMPERSONATED_USER
        self.msg['subject'] = msg_subject

    def set_recipient(self, recipient):
        if self.msg['to']:
            del self.msg['to']
        self.msg['to'] = recipient

    def send_mail(self):
        raw_msg = base64.urlsafe_b64encode(self.msg.as_bytes()).decode('utf-8')
        email_message = {'raw': raw_msg}
        try:
            sent_message = self.service.users().messages().send(userId="me", body=email_message).execute()
            print(f"Message sent! Message ID : {sent_message['id']}")
        except Exception as e:
            print(f"An error occured {e}")
            return None
