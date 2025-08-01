import uuid
from datetime import datetime

def create_order(conn, user_id, items):
    order_id = str(uuid.uuid4())
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO orders (id, user_id, created_at) VALUES (%s, %s, %s)
    ''', (order_id, user_id, datetime.now()))

    for item in items:
        item_id = str(uuid.uuid4())
        product_id = item["product_id"]
        quantity = item["quantity"]

        cur.execute('''
            INSERT INTO order_items (id, order_id, product_id, quantity)
            VALUES (%s, %s, %s, %s)
        ''', (item_id, order_id, product_id, quantity))

        update_current_quantity(conn, product_id)

    conn.commit()
    return order_id

def update_current_quantity(conn, product_id):
    cur = conn.cursor()
    cur.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
    total_quantity = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(quantity), 0) FROM order_items WHERE product_id = %s", (product_id,))
    ordered_quantity = cur.fetchone()[0]

    current_quantity = total_quantity - ordered_quantity
    cur.execute("UPDATE products SET current_quantity = %s WHERE id = %s", (current_quantity, product_id))
    conn.commit()
