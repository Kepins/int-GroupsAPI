from email.mime.text import MIMEText
from flask import current_app

from app.email import send_email


def send_invitation_email(receiver_email, invitation_link):
    text = f"Invitation link: {invitation_link}"
    message = MIMEText(text)
    message["From"] = current_app.config["SENDER_EMAIL"]
    message["To"] = receiver_email
    message["Bcc"] = receiver_email
    message["Subject"] = "Invitation to group in GroupsAPP."
    send_email(message)
