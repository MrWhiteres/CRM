from os import environ

from dotenv import load_dotenv

load_dotenv()

KEY = environ.get('SECRET_KEY')
GOOGLE_KEY = environ.get('GOOGLE_KEY')
