import pymysql
import os
from dotenv import load_dotenv, find_dotenv

# 載入 .env 檔案
load_dotenv(find_dotenv(), override=True)

# 讀取環境變數
RDS_HOST = os.getenv("RDS_HOST")
RDS_PORT = os.getenv("RDS_PORT", "3306")
RDS_USER = os.getenv("RDS_USER")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_DATABASE = os.getenv("RDS_DATABASE")

# 印出所有參數（遮蔽密碼）
print("[DEBUG] RDS_HOST:", RDS_HOST)
print("[DEBUG] RDS_PORT:", RDS_PORT)
print("[DEBUG] RDS_USER:", RDS_USER)
print("[DEBUG] RDS_PASSWORD:", '****' if RDS_PASSWORD else '(None)')
print("[DEBUG] RDS_DATABASE:", RDS_DATABASE)

# 若任何參數為 None，提前警告
missing = [name for name, value in {
    "RDS_HOST": RDS_HOST,
    "RDS_USER": RDS_USER,
    "RDS_PASSWORD": RDS_PASSWORD,
    "RDS_DATABASE": RDS_DATABASE
}.items() if not value]

if missing:
    print("❗缺少必要的環境變數：", ", ".join(missing))
    exit(1)

# 嘗試連線
try:
    conn = pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DATABASE,
        port=int(RDS_PORT),
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ 成功連線到資料庫")

    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        results = cursor.fetchall()
        print("📋 Tables:", results)

except Exception as e:
    print("❌ 錯誤：", e)

finally:
    if 'conn' in locals():
        conn.close()
