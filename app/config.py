import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    POSTGRES_USER = os.environ['POSTGRESQL_USER']
    POSTGRES_PASSWD = os.environ['POSTGRESQL_PASSWD']
    POSTGRES_HOSTNAME = os.environ['POSTGRESQL_HOSTNAME']
    POSTGRES_DB_NAME = os.environ['POSTGRESQL_DB_NAME']

    SMTP_PORT = int(os.environ.get("SMTP_PORT"))
    SMTP_SERVER = os.environ.get("SMTP_SERVER")
    SENDER_EMAIL = os.environ.get("SMTP_SENDER_EMAIL")
    SENDER_PASSWD = os.environ.get("SMTP_SENDER_PASSWD")

    SECRET_KEY = os.environ.get("SECRET_KEY")
