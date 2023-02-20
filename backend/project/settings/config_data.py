from dotenv import load_dotenv
from os import environ
load_dotenv()

KEY = environ.get('SECRET_KEY')

