import os

from dotenv import load_dotenv
from models import *

load_dotenv()
database_path = "postgresql://{}:{}@{}/{}".format(
    os.environ.get('DB_USER'),
    os.environ.get('DB_PASSWORD'),
    os.environ.get('DB_HOST'),
    'library'
)