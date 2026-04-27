from db import get_connection


def show_all_products():
    query = """
        SELECT p.product_id, p.name, b.name as brand_name, p.price, p.category, i.quantity
        FROM products p
        JOIN brands b ON p.brand_id = b.brand_id
        LEFT JOIN inventory i ON p.product_id = i.product_id
    """
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()

        if not rows:
            print("\n📦 Товаров пока нет!")
            return

        print("\n" + "=" * 80)
        print(f"{'ID':<4} {'Название':<25} {'Бренд':<12} {'Цена':<10} {'Остаток':<8} {'Категория'}")
        print("-" * 80)
        for row in rows:
            print(f"{row['product_id']:<4} {row['name']:<25} {row['brand_name']:<12} "
                  f"{row['price']:<10.2f} {row['quantity'] if row['quantity'] else 0:<8} {row['category']}")
        print("=" * 80)


def show_low_stock(threshold=10):
    query = """
        SELECT p.name, b.name as brand_name, i.quantity
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        JOIN brands b ON p.brand_id = b.brand_id
        WHERE i.quantity < ?
    """
    with get_connection() as conn:
        rows = conn.execute(query, (threshold,)).fetchall()

        print("\n⚠️ ТОВАРЫ С НИЗКИМ ОСТАТКОМ ⚠️")
        print("=" * 50)
        if not rows:
            print("✅ Все товары в достаточном количестве!")
        for row in rows:
            print(f"{row['name']} - {row['brand_name']} - остаток: {row['quantity']} шт.")
        print("=" * 50)


def show_sales():
    query = """
        SELECT s.sale_id, p.name, s.quantity_sold, s.total_amount, s.sale_date, s.customer_name
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        ORDER BY s.sale_date DESC
    """
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()

        print("\n💰 ИСТОРИЯ ПРОДАЖ 💰")
        print("=" * 70)
        for row in rows:
            print(
                f"{row['sale_date']} | {row['name']} | {row['quantity_sold']} шт. | {row['total_amount']} руб. | {row['customer_name'] or 'Без имени'}")
        print("=" * 70)


def show_brands():
    query = "SELECT brand_id, name, country, established_year FROM brands"
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()

        print("\n🏷️ БРЕНДЫ")
        print("=" * 50)
        for row in rows:
            print(f"{row['brand_id']}. {row['name']} ({row['country']}, {row['established_year']})")
        print("=" * 50)