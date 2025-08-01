from flask import Blueprint, render_template
from db import get_connection

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, volume, current_quantity FROM products WHERE status = 'active'")
    rows = cur.fetchall()
    
    # 轉換為前台頁面期望的元組格式
    products = []
    for row in rows:
        if isinstance(row, dict):
            # 如果是字典格式，轉換為元組
            products.append((
                row['id'],
                row['name'],
                row['volume'],
                row['current_quantity']
            ))
        else:
            # 如果已經是元組格式，直接使用
            products.append(row)
    
    conn.close()
    return render_template("frontend/frontend.html", products=products)

@frontend_bp.route('/login')
def login_page():
    return render_template('frontend/login.html')

@frontend_bp.route('/register')
def register_page():
    return render_template('frontend/register.html')
