# GroupsAPI

The GroupsAPI application allows users to create groups and create events for these groups.

## Requirements

- Python3.11 installed
- Access to two PostgreSQL databases: dev+test
- Account(e.g. Gmail) for sending emails using SMPT

## Installation

Run below commands in the terminal from the project root.

### Create virtual environment  
`python3.11 -m venv venv`  
### Activate venv  
`source venv/bin/activate`  
### Install requirements
`pip install -r requirements.txt`

## Configuration

Create **.env** and **.env.test** files with the same keys as **.env.example**:
- *POSTGRESQL_USER* - user with access to DB
- *POSTGRESQL_PASSWD* - user's password
- *POSTGRESQL_HOSTNAME* - host on which DB is running
- *POSTGRESQL_DB_NAME* - name of DB
- *SMTP_PORT* - port on which smtp server is running
- *SMTP_SERVER* - hostname of smtp server
- *SMTP_SENDER_EMAIL* - email that app will use
- *SMTP_SENDER_PASSWD* - password for account
- *SECRET_KEY_ITSDANGEROUS* - key used for itsdangerous email verification
- *SECRET_KEY_JWT* - key used for signing json web tokens
- *EXPIRATION_JWT_SECONDS* - how long is seconds will json web tokens be valid
- *FLASK_RUN_HOST* - host on which the app will run
- *FLASK_RUN_PORT* - port on which the app will run


## Running

With **venv active** in project root type `flask run` in the terminal.  
Application API will be exposed on host and port or defined in .env.