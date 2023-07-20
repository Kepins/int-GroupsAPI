from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class AlchemyDatabase:
    def __init__(self):
        self.Session = None

    def init_app(self, app):
        engine = create_engine(
            f'postgresql+psycopg2://{app.config["POSTGRES_USER"]}:{app.config["POSTGRES_PASSWD"]}'
            f'@{app.config["POSTGRES_HOSTNAME"]}/{app.config["POSTGRES_DB_NAME"]}')

        session_factory = sessionmaker(bind=engine)
        self.Session = scoped_session(session_factory)
