from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import SECRET_KEY
from db import db_users as user_db

bp = Blueprint('auth', __name__)

# 註冊 - 已停用
@bp.route('/api/register', methods=['POST'])
def register():
    return jsonify({'error': '註冊功能已停用'}), 403

# 登入 - 已停用
@bp.route('/api/login', methods=['POST'])
def login():
    return jsonify({'error': '登入功能已停用'}), 403 