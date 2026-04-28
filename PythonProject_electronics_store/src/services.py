import sqlite3
from db import get_connection
from datetime import date


def add_brand(name, country, established_year):
    query = "INSERT INTO brands (name, country, established_year) VALUES (?, ?, ?)"
    try:
        with get_connection() as conn:
            conn.execute(query, (name, country, established_year))
            conn.commit()
        print(f"✅ Бренд '{name}' добавлен!")
        return True
    except sqlite3.IntegrityError:
        print(f"❌ Бренд '{name}' уже существует!")
        return False


def add_product(name, brand_id, price, category):
    query = "INSERT INTO products (name, brand_id, price, category) VALUES (?, ?, ?, ?)"
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (name, brand_id, price, category))
            product_id = cursor.lastrowid
            cursor.execute("INSERT INTO inventory (product_id, quantity) VALUES (?, 0)", (product_id,))
            conn.commit()
        print(f"✅ Товар '{name}' добавлен!")
        return product_id
    except sqlite3.Error as e:
        print(f"❌ Ошибка: {e}")
        return None


def update_stock(product_id, quantity_change):
    query = "UPDATE inventory SET quantity = quantity + ?, last_updated = ? WHERE product_id = ?"
    try:
        with get_connection() as conn:
            conn.execute(query, (quantity_change, date.today(), product_id))
            conn.commit()
        print(f"✅ Склад обновлен!")
        return True
    except sqlite3.Error as e:
        print(f"❌ Ошибка: {e}")
        return False


def sell_product(product_id, quantity, customer_name=None):
    with get_connection() as conn:
        cursor = conn.cursor()

        product = cursor.execute("SELECT price, name FROM products WHERE product_id = ?", (product_id,)).fetchone()
        if not product:
            print("❌ Товар не найден!")
            return False

        stock = cursor.execute("SELECT quantity FROM inventory WHERE product_id = ?", (product_id,)).fetchone()
        if not stock or stock['quantity'] < quantity:
            print("❌ Недостаточно товара!")
            return False

        total = product['price'] * quantity

        cursor.execute("""
            INSERT INTO sales (product_id, quantity_sold, total_amount, customer_name)
            VALUES (?, ?, ?, ?)
        """, (product_id, quantity, total, customer_name))

        cursor.execute("UPDATE inventory SET quantity = quantity - ?, last_updated = ? WHERE product_id = ?",
                       (quantity, date.today(), product_id))
        conn.commit()

    print(f"💰 Продажа на {total} руб. оформлена!")
    return True


def update_product_price(product_id, new_price):
    query = "UPDATE products SET price = ? WHERE product_id = ?"
    try:
        with get_connection() as conn:
            conn.execute(query, (new_price, product_id))
            conn.commit()
        print(f"✅ Цена обновлена!")
        return True
    except sqlite3.Error as e:
        print(f"❌ Ошибка: {e}")
        return False


def delete_product(product_id):
    query = "DELETE FROM products WHERE product_id = ?"
    try:
        with get_connection() as conn:
            conn.execute(query, (product_id,))
            conn.commit()
        print(f"✅ Товар удален!")
        return True
    except sqlite3.Error as e:
        print(f"❌ Ошибка: {e}")
        return False


def search_products(search_term):
    query = """
        SELECT p.product_id, p.name, b.name as brand_name, p.price, p.category, i.quantity
        FROM products p
        JOIN brands b ON p.brand_id = b.brand_id
        LEFT JOIN inventory i ON p.product_id = i.product_id
        WHERE p.name LIKE ? OR p.category LIKE ?
    """
    search = f"%{search_term}%"
    with get_connection() as conn:
        return conn.execute(query, (search, search)).fetchall()