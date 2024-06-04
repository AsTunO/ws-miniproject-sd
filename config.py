import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
