import os
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
# Przechowywanie ścieżki do pliku dotenv
env_file = base_dir / '.env'
load_dotenv(env_file)  # załadowanie ustawień z pliku


# Klasa odpowiedzialna za przechowywanie ustawień aplikacji
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 5
    JWT_EXPIRED_MINUTES = 30


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///' + str(base_dir / 'development.db'))


class TestingConfig(Config):
    DB_FILE_PATH = base_dir / 'tests' / 'test.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE_PATH}'
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'production_db')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
