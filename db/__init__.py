import mysql.connector
from config import MYSQL_CONFIG

def get_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

from .db_products import *
from .db_orders import *
from .db_users import *
