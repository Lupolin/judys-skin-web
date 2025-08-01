import uuid
from flask import Blueprint, request, jsonify
from db import *

backend = Blueprint("backend", __name__)

# 商品上架
@backend.route("/products", methods=["GET"])
def get_all_products():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)  # 使用字典格式
    cur.execute("SELECT id, name, quantity, current_quantity, volume, status FROM products")
    products = cur.fetchall()
    conn.close()
    return jsonify(products)

@backend.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, quantity, volume, status FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    conn.close()
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "找不到商品"}), 404
@backend.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    conn = get_connection()
    product_id = str(uuid.uuid4())
    result = add_product(
        conn,
        product_id,
        data["name"],
        data["quantity"],
        data["volume"],
        data.get("status", "active")
    )
    return jsonify({"message": result, "id": product_id}), 201

@backend.route("/products/<product_id>", methods=["PUT"])
def modify_product(product_id):
    data = request.get_json()
    conn = get_connection()
    result = update_product(
        conn,
        product_id,
        new_quantity=data.get("quantity"),
        new_volume=data.get("volume"),
        new_status=data.get("status")
    )
    return jsonify({"message": result})

# 商品狀態切換（上下架）
@backend.route("/products/<product_id>/status", methods=["PATCH"])
def change_product_status(product_id):
    data = request.get_json()
    new_status = data.get("status")
    if new_status not in ["active", "inactive"]:
        return jsonify({"error": "狀態必須為 active 或 inactive"}), 400
    conn = get_connection()
    result = update_product(conn, product_id, new_status=new_status)
    conn.close()
    return jsonify({"message": result})
@backend.route("/products/<product_id>", methods=["DELETE"])
def remove_product(product_id):
    conn = get_connection()
    result = delete_product(conn, product_id)
    return jsonify({"message": result})

# 訂單操作
@backend.route("/orders", methods=["GET"])
def get_all_orders():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, user_id, user_name, status, created_at, updated_at FROM orders")
    orders = []
    for order_row in cur.fetchall():
        order_id = order_row['id']
        # 查詢訂單明細
        cur.execute("SELECT product_id, product_name, quantity FROM order_items WHERE order_id = %s", (order_id,))
        items = cur.fetchall()
        order_data = order_row.copy()
        order_data['items'] = items
        orders.append(order_data)
    conn.close()
    return jsonify(orders)

@backend.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, user_id FROM orders WHERE id = %s", (order_id,))
    order_row = cur.fetchone()
    if not order_row:
        conn.close()
        return jsonify({"error": "找不到訂單"}), 404
    
    # 查詢訂單明細
    cur.execute("SELECT product_id, product_name, quantity FROM order_items WHERE order_id = %s", (order_id,))
    items = cur.fetchall()
    
    result = {
        "order_id": order_row['id'],
        "user_id": order_row['user_id'],
        "items": items
    }
    conn.close()
    return jsonify(result)
@backend.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    user_name = data.get("user_name") or user_id  # 若沒傳 user_name 則用 user_id
    items = data.get("items", [])

    if not user_id or not items:
        return jsonify({"error": "缺少 user_id 或 items"}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        order_id = str(uuid.uuid4())

        # 建立訂單，需寫入 user_id, user_name
        cur.execute("INSERT INTO orders (id, user_id, user_name) VALUES (%s, %s, %s)", (order_id, user_id, user_name))

        for item in items:
            item_id = str(uuid.uuid4())
            product_id = item["product_id"]
            quantity = item["quantity"]

            # 查出商品名稱
            cur.execute("SELECT name FROM products WHERE id = %s", (product_id,))
            row = cur.fetchone()
            if not row:
                raise Exception(f"❌ 找不到商品：{product_id}")
            product_name = row[0]

            # 寫入 order_items
            cur.execute("""
                INSERT INTO order_items (id, order_id, product_id, product_name, quantity)
                VALUES (%s, %s, %s, %s, %s)
            """, (item_id, order_id, product_id, product_name, quantity))

            # 更新商品庫存數量
            update_current_quantity(conn, product_id)

        conn.commit()
        return jsonify({"message": "✅ 訂單已建立", "order_id": order_id})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()

# 商品庫存查詢與調整
@backend.route("/products/<product_id>/stock", methods=["GET"])
def get_product_stock(product_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify({"product_id": product_id, "quantity": row[0]})
    else:
        return jsonify({"error": "找不到商品"}), 404

@backend.route("/products/<product_id>/stock", methods=["PATCH"])
def update_product_stock(product_id):
    data = request.get_json()
    new_quantity = data.get("quantity")
    if new_quantity is None or not isinstance(new_quantity, int):
        return jsonify({"error": "quantity 必須為整數"}), 400
    conn = get_connection()
    result = update_product(conn, product_id, new_quantity=new_quantity)
    conn.close()
    return jsonify({"message": result})