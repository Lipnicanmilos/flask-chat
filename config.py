import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Nikdy nedávaj skutočný SECRET_KEY natvrdo do kódu - vždy z .env
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-me')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
