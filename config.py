"""Configuração via variáveis de ambiente; sem senhas no repositório."""
import os

DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "app")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "cartoes_db")
API_KEY_BANDEIRA = os.getenv("API_KEY_BANDEIRA")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "/tmp/uploads")
