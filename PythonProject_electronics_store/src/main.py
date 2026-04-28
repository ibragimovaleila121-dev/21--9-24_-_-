import sys
from db import init_db
from services import add_product, add_brand, sell_product, update_stock, update_product_price, delete_product, \
    search_products
from reports import show_all_products, show_low_stock, show_sales, show_brands


def main():
    init_db()

    while True:
        print("\n" + "=" * 50)
        print("🏪 МАГАЗИН ЭЛЕКТРОНИКИ")
        print("=" * 50)
        print("1. Показать все товары")
        print("2. Показать бренды")
        print("3. Показать продажи")
        print("4. Товары с низким остатком")
        print("5. Поиск товаров")
        print("6. Добавить товар")
        print("7. Добавить бренд")
        print("8. Оформить продажу")
        print("9. Пополнить склад")
        print("10. Изменить цену")
        print("11. Удалить товар")
        print("0. Выход")
        print("=" * 50)

        choice = input("👉 Ваш выбор: ")

        if choice == "1":
            show_all_products()
        elif choice == "2":
            show_brands()
        elif choice == "3":
            show_sales()
        elif choice == "4":
            show_low_stock()
        elif choice == "5":
            term = input("Введите название или категорию: ")
            results = search_products(term)
            print(f"\n🔍 Найдено {len(results)} товаров:")
            for r in results:
                print(f"   {r['product_id']}. {r['name']} - {r['price']} руб. ({r['category']})")
        elif choice == "6":
            name = input("Название товара: ")
            show_brands()
            brand_id = int(input("ID бренда: "))
            price = float(input("Цена: "))
            category = input("Категория: ")
            add_product(name, brand_id, price, category)
        elif choice == "7":
            name = input("Название бренда: ")
            country = input("Страна: ")
            year = int(input("Год основания: "))
            add_brand(name, country, year)
        elif choice == "8":
            show_all_products()
            product_id = int(input("ID товара: "))
            qty = int(input("Количество: "))
            customer = input("Имя покупателя (Enter - пропустить): ")
            sell_product(product_id, qty, customer if customer else None)
        elif choice == "9":
            show_all_products()
            product_id = int(input("ID товара: "))
            qty = int(input("Количество для добавления: "))
            update_stock(product_id, qty)
        elif choice == "10":
            show_all_products()
            product_id = int(input("ID товара: "))
            new_price = float(input("Новая цена: "))
            update_product_price(product_id, new_price)
        elif choice == "11":
            show_all_products()
            product_id = int(input("ID товара для удаления: "))
            delete_product(product_id)
        elif choice == "0":
            print("👋 До свидания!")
            sys.exit()
        else:
            print("❌ Неверный выбор!")

        input("\nНажмите Enter...")


if __name__ == "__main__":
    main()