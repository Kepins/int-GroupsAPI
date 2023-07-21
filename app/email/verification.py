from email.mime.text import MIMEText
from flask import current_app

from app.email import send_email


def send_verification_email(receiver_email, verification_link):
    text = f"Verification link: {verification_link}"
    message = MIMEText(text)
    message['From'] = current_app.config["SENDER_EMAIL"]
    message['To'] = receiver_email
    message["Bcc"] = receiver_email
    message['Subject'] = 'Verify your email address for GroupsAPP.'
    send_email(message)
