import os


class Config:
    def __init__(self):
        self.ENGINE_URL = os.environ["ENGINE_URL"]

        self.SMTP_PORT = int(os.environ.get("SMTP_PORT"))
        self.SMTP_SERVER = os.environ.get("SMTP_SERVER")
        self.SENDER_EMAIL = os.environ.get("SMTP_SENDER_EMAIL")
        self.SENDER_PASSWD = os.environ.get("SMTP_SENDER_PASSWD")

        self.SECRET_KEY_ITSDANGEROUS = os.environ.get("SECRET_KEY_ITSDANGEROUS")
        self.SECRET_KEY_JWT = os.environ.get("SECRET_KEY_JWT")

        # Expiration time of JWT in seconds
        self.EXPIRATION_JWT_SECONDS = int(os.environ.get("EXPIRATION_JWT_SECONDS"))
