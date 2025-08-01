import os
from dotenv import load_dotenv, find_dotenv

# 載入 .env 檔案
load_dotenv(find_dotenv(), override=True)

SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

# AWS RDS MySQL 連線設定
MYSQL_CONFIG = {
    'host': os.getenv('RDS_HOST'),
    'user': os.getenv('RDS_USER'),
    'password': os.getenv('RDS_PASSWORD'),
    'database': os.getenv('RDS_DATABASE', 'judys-skin-db'),
    'port': int(os.getenv('RDS_PORT', 3306))
    # 'ssl_ca': os.getenv('RDS_SSL_CA'),  # 可選
    # 'ssl_verify_cert': os.getenv('RDS_SSL_VERIFY', 'true').lower() == 'true'  # 可選
}
