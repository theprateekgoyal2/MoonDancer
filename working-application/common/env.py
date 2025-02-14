import os

# SQL_DBUSER = os.environ.get('SQL_DBUSER')
# SQL_DBPASS = os.environ.get('SQL_DBPASS')

SQL_DBUSER = 'romulus'
SQL_DBPASS = 'your_password'

SQL_INSTANCE_URI = f'mysql+pymysql://{SQL_DBUSER}:{SQL_DBPASS}@localhost/nymeria'
SQLALCHEMY_TRACK_MODIFICATIONS = True
