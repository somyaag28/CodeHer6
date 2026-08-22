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
            stock INTEGER NOT NULL,
            gst_rate REAL DEFAULT 0,
            image_path TEXT,
            embedding TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_product(
    product_id,
    name,
    price,
    stock,
    gst_rate=0,
    image_path=None,
    embedding=None
):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO inventory
        (id, name, price, stock, gst_rate, image_path, embedding)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            product_id,
            name,
            price,
            stock,
            gst_rate,
            image_path,
            embedding
        )
    )

    conn.commit()
    conn.close()


def get_product(product_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, price, stock, gst_rate, image_path, embedding
        FROM inventory
        WHERE id = ?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    conn.close()

    return product


def get_all_products():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, price, stock, gst_rate, image_path, embedding
        FROM inventory
        """
    )

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


def update_product_embedding(product_id, embedding, image_path=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if image_path is not None:
        cursor.execute(
            """
            UPDATE inventory
            SET embedding = ?, image_path = ?
            WHERE id = ?
            """,
            (embedding, image_path, product_id)
        )
    else:
        cursor.execute(
            """
            UPDATE inventory
            SET embedding = ?
            WHERE id = ?
            """,
            (embedding, product_id)
        )

    conn.commit()
    conn.close()


create_database()