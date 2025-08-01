from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import SECRET_KEY
from db import db_users as user_db

bp = Blueprint('auth', __name__)

# 註冊
@bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    print('收到註冊資料:', data)
    email = data.get('email')
    password = data.get('password')
    user_name = data.get('user_name')
    phone = data.get('phone')
    if not user_name or not password:
        print('缺少姓名或密碼')
        return jsonify({'error': '姓名與密碼必填'}), 400
    # 檢查是否已存在
    if user_db.get_user_by_email(email):
        print('用戶已存在:', email)
        return jsonify({'error': '用戶已存在'}), 400
    hashed = generate_password_hash(password)
    user_db.create_user(email, hashed, user_name, phone)
    print('註冊成功:', email)
    return jsonify({'msg': '註冊成功'})

# 登入
@bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    print('收到登入資料:', data)
    email = data.get('email')
    password = data.get('password')
    user = user_db.get_user_by_email(email)
    print('查詢到的user:', user)
    if not user or not check_password_hash(user['password_hash'], password):
        print('帳號或密碼錯誤')
        return jsonify({'error': '帳號或密碼錯誤'}), 401
    token = jwt.encode({
        'user_id': user['id'],
        'name': user['user_name'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token}) 