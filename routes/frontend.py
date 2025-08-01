from flask import Blueprint, render_template
from db import get_connection

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, volume, current_quantity FROM products WHERE status = 'active'")
    products = cur.fetchall()
    conn.close()
    return render_template("frontend/frontend.html", products=products)

@frontend_bp.route('/login')
def login_page():
    return render_template('frontend/login.html')

@frontend_bp.route('/register')
def register_page():
    return render_template('frontend/register.html')
