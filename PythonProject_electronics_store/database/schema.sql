PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS brands;

CREATE TABLE brands (
    brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    country TEXT NOT NULL,
    established_year INTEGER
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand_id INTEGER NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    category TEXT NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE
);

CREATE TABLE inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL UNIQUE,
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    last_updated DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL CHECK (quantity_sold > 0),
    sale_date DATE DEFAULT CURRENT_DATE,
    total_amount REAL NOT NULL CHECK (total_amount >= 0),
    customer_name TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ========== БРЕНДЫ ==========
INSERT INTO brands (name, country, established_year) VALUES
('ARDOR GAMING', 'China', 2015),
('Maono', 'China', 2018);

-- ========== ТОВАРЫ (НОВЫЕ) ==========
INSERT INTO products (name, brand_id, price, category) VALUES
('Мышь', 1, 1599, 'Периферия'),
('Наушники', 1, 3199, 'Аудио'),
('Микрофон', 2, 4799, 'Аудио'),
('Веб-камера', 1, 5299, 'Периферия');

-- ========== СКЛАД (ОСТАТКИ) ==========
INSERT INTO inventory (product_id, quantity, last_updated) VALUES
(1, 50, date('now')),
(2, 35, date('now')),
(3, 20, date('now')),
(4, 15, date('now'));

-- ========== ПРОДАЖИ (ПРИМЕРЫ) ==========
INSERT INTO sales (product_id, quantity_sold, sale_date, total_amount, customer_name) VALUES
(1, 2, date('now', '-2 days'), 3198, 'Иван Петров'),
(2, 1, date('now', '-1 days'), 3199, 'Мария Сидорова'),
(3, 1, date('now'), 4799, 'Алексей Иванов');