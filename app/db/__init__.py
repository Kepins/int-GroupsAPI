from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from app import config

engine = create_engine(f'postgresql+psycopg2://{config.POSTGRES_USER}:{config.POSTGRES_PASSWD}'
                       f'@{config.POSTGRES_HOSTNAME}/{config.POSTGRES_DB_NAME}')


session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)
