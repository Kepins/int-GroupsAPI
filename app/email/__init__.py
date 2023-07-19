import os
import smtplib
import ssl

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.environ.get("SMTP_PORT"))
SERVER = os.environ.get("SMTP_SERVER")
SENDER_EMAIL = os.environ.get("SMTP_SENDER_EMAIL")
SENDER_PASSWD = os.environ.get("SMTP_SENDER_PASSWD")


def send_email(message):
    context = ssl.create_default_context()
    with smtplib.SMTP(SERVER, PORT) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(SENDER_EMAIL, SENDER_PASSWD)
        server.send_message(message)
