from app import create_app
from models import User, Group, Event
from app.db import Session

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'Session': Session, 'User': User, 'Group': Group, 'Event': Event}