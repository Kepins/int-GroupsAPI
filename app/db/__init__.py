import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = os.environ['POSTGRESQL_USER']
passwd = os.environ['POSTGRESQL_PASSWD']
hostname = os.environ['POSTGRESQL_HOSTNAME']
db_name = os.environ['POSTGRESQL_DB_NAME']
engine = create_engine(f'postgresql+psycopg2://{user}:{passwd}@{hostname}/{db_name}')


session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)
