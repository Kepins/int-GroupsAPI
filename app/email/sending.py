import smtplib
import ssl

from flask import current_app


def send_email(message):
    context = ssl.create_default_context()
    with smtplib.SMTP(current_app.config["SMTP_SERVER"], current_app.config["SMTP_PORT"]) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(current_app.config["SENDER_EMAIL"], current_app.config["SENDER_PASSWD"])
        server.send_message(message)