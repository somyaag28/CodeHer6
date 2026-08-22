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
create_database()
