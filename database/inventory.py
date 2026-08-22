import sqlite3


DATABASE = "inventory.db"


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_product(product_id, name, price, stock):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO inventory (id, name, price, stock)
        VALUES (?, ?, ?, ?)
        """,
        (product_id, name, price, stock)
    )

    conn.commit()
    conn.close()


def get_product(product_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM inventory WHERE id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    conn.close()

    return product


def get_all_products():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")

    products = cursor.fetchall()

    conn.close()

    return products


def deduct_stock(product_id, quantity):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT stock FROM inventory WHERE id = ?",
        (product_id,)
    )

    result = cursor.fetchone()

    if result is None:
        conn.close()
        return False, "Product not found"

    current_stock = result[0]

    if quantity <= 0:
        conn.close()
        return False, "Invalid quantity"

    if quantity > current_stock:
        conn.close()
        return False, "Not enough stock"

    new_stock = current_stock - quantity

    cursor.execute(
        """
        UPDATE inventory
        SET stock = ?
        WHERE id = ?
        """,
        (new_stock, product_id)
    )

    conn.commit()
    conn.close()

    return True, "Stock updated successfully"


create_database()