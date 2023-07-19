import smtplib
import ssl

from app import config


def send_email(message):
    context = ssl.create_default_context()
    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(config.SENDER_EMAIL, config.SENDER_PASSWD)
        server.send_message(message)
