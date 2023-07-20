from app import create_app
from models import User, Group, Event

app = create_app()


@app.shell_context_processor
def make_shell_context():
    from app import db
    return {'Session': db.Session, 'User': User, 'Group': Group, 'Event': Event}