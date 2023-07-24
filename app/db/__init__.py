from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class AlchemyDatabase:
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.Session = None

    def init_app(self, app):
        self.engine = create_engine(
            f'postgresql+psycopg2://{app.config["POSTGRES_USER"]}:{app.config["POSTGRES_PASSWD"]}'
            f'@{app.config["POSTGRES_HOSTNAME"]}/{app.config["POSTGRES_DB_NAME"]}'
        )

        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
