import os
from flask import Flask
from routes.frontend import frontend_bp
from routes.backend import backend
from routes.admin import admin
from routes.auth import bp as auth_bp
from dotenv import load_dotenv, find_dotenv

# 載入 .env 檔案
load_dotenv(find_dotenv(), override=True)

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 可搬到 config.py

# 註冊前台 Blueprint

app.register_blueprint(frontend_bp)
app.register_blueprint(backend)
# ✅ 註冊後台管理介面 Blueprint
app.register_blueprint(admin)
app.register_blueprint(auth_bp)

def main():
    print("✅ Running local Flask server")
    app.run(host="0.0.0.0", port=5004, debug=True)

# ✅ 若是本地執行，跑 main()（含 scheduler 與 app.run）
# ✅ 若是 Gunicorn，則由環境變數控制是否啟動 scheduler
if __name__ == "__main__":
    main()
elif os.environ.get("RUN_SCHEDULER") == "true":
    print("✅ Starting scheduler under Gunicorn")
