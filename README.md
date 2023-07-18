# GroupsAPI

The GroupsAPI application allows users to create groups and create events for these groups.

## Requirements

- Python3.11 installed
- Access to an PostgreSQL database

## Installation

Run below commands in the terminal from the project root.

### Create virtual environment  
`python3.11 -m venv venv`  
### Activate venv  
`source venv/bin/activate`  
### Install requirements
`pip install -r requirements.txt`

## Configuration

Create **.env** file with the same keys as **.env.example**:
- *POSTGRESQL_USER* - user with access to DB
- *POSTGRESQL_PASSWD* - user's password
- *POSTGRESQL_HOSTNAME* - host on which DB is running
- *POSTGRESQL_DB_NAME* - name of DB
- *FLASK_RUN_HOST* - host on which the app will run
- *FLASK_RUN_PORT* - port on which the app will run


## Running

With **venv active** in project root type `flask run` in the terminal.  
Application API will be exposed on host and port or defined in .env.