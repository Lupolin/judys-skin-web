from flask import Blueprint, render_template
admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
def admin_dashboard():
    return render_template('backend/dashboard.html')