import os
from dotenv import load_dotenv
load_dotenv()


MYSQL_USER = os.environ.get('MYSQL_USER') or os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or os.getenv('MYSQL_PASSWORD')

MYSQL_HOST = "westeros-prateekgoyal6417-ea26.h.aivencloud.com"
MYSQL_PORT = 23140
MYSQL_DB = "defaultdb"
MYSQL_SSL_MODE = "REQUIRED"

SQL_INSTANCE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
SQLALCHEMY_TRACK_MODIFICATIONS = True

REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or os.getenv('REDIS_PASSWORD')
REDIS_USER = os.environ.get('REDIS_USER') or os.getenv('REDIS_USER')
