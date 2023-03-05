from os import environ

from dotenv import load_dotenv

load_dotenv()

KEY = environ.get('SECRET_KEY')
GOOGLE_KEY = environ.get('GOOGLE_KEY')
SECOND_KEY = environ.get("GOOGLE_SECOND_KEY")
EMAIL_SERVER = environ.get("EMAIL_SERVER")
EMAIL_PASSWORD = environ.get("EMAIL_PASSWORD")
URL_FRONTEND = environ.get("URL_FRONTEND")
