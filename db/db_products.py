import uuid

def add_product(conn, product_id, name, quantity, volume, status="active"):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO products (id, name, quantity, current_quantity, volume, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (product_id, name, quantity, quantity, volume, status))
    conn.commit()
    return f"✅ 商品已新增: {name}（數量: {quantity}, 狀態: {status}）"

def update_product(conn, product_id, new_quantity=None, new_volume=None, new_status=None):
    cur = conn.cursor()
    fields = []
    values = []

    if new_quantity is not None:
        fields.append("quantity = %s")
        values.append(new_quantity)
    if new_volume is not None:
        fields.append("volume = %s")
        values.append(new_volume)
    if new_status is not None:
        fields.append("status = %s")
        values.append(new_status)

    if not fields:
        return "⚠️ 沒有要更新的欄位"

    values.append(product_id)
    sql = f"UPDATE products SET {', '.join(fields)} WHERE id = %s"
    cur.execute(sql, values)
    conn.commit()

    if new_quantity is not None:
        update_current_quantity(conn, product_id)

    return f"✅ 商品 {product_id} 已更新"

def delete_product(conn, product_id):
    cur = conn.cursor()
    cur.execute("UPDATE products SET status = 'inactive' WHERE id = %s", (product_id,))
    conn.commit()
    return f"🗑 已將商品 {product_id} 標記為 inactive"



def update_current_quantity(conn, product_id):
    cur = conn.cursor()
    # 計算此產品已被訂購的總數量
    cur.execute("""
        SELECT SUM(quantity) FROM order_items
        WHERE product_id = %s;
    """, (product_id,))
    total_ordered = cur.fetchone()[0] or 0

    # 取得原本商品總數量
    cur.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
    row = cur.fetchone()
    if not row:
        raise Exception("找不到該產品")
    total_quantity = row[0]

    # 計算目前剩餘數量
    current_quantity = max(total_quantity - total_ordered, 0)

    # 寫入 current_quantity
    cur.execute("""
        UPDATE products SET current_quantity = %s
        WHERE id = %s;
    """, (current_quantity, product_id))