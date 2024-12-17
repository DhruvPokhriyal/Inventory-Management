import smtplib
import json
from email.message import EmailMessage

with open("email_creds.json", "r") as file:
    CREDENTIALS = json.load(file)
    MY_EMAIL = CREDENTIALS["email"]
    PASSWORD = CREDENTIALS["password"]


class Email:
    def __init__(self):
        self.msg = EmailMessage()
        self.fill_msg()
        self.connection = smtplib.SMTP("smtp.gmail.com")
        self.connection.starttls()
        self.connection.login(user=MY_EMAIL, password=PASSWORD)

    def fill_msg(self):
        with open("email_content.txt") as file:
            mail_template = file.read()
            self.msg['From'] = MY_EMAIL
            self.msg['Subject'] = "Item return"
            self.msg.set_content(mail_template)

    def set_recipient(self, recipient):
        self.msg['To'] = recipient

    def send_mail(self):
        self.connection.send_message(self.msg)

    def close_connection(self):
        self.connection.close()
