from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class AlchemyDatabase:
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.Session = None

    def init_app(self, app):
        self.engine = create_engine(
            app.config["ENGINE_URL"]
        )

        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
