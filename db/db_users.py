import pymysql
import uuid
from datetime import datetime
from config import MYSQL_CONFIG

def get_connection():
    return pymysql.connect(
        host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        database=MYSQL_CONFIG['database'],
        port=MYSQL_CONFIG['port'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_user_by_email(email):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            return cursor.fetchone()
    finally:
        conn.close()

def create_user(email, password_hash, user_name, phone):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            user_id = str(uuid.uuid4())
            sql = """
                INSERT INTO users (id, email, password_hash, user_name, phone, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, email, password_hash, user_name, phone, 'active', now, now))
        conn.commit()
    finally:
        conn.close()
