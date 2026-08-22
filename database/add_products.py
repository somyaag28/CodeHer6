"""
add_products.py

Adds the initial products to the inventory database.
"""

from inventory import add_product


products = [
    (101, "Coca Cola", 40, 20),
    (102, "Pepsi", 40, 15),
    (103, "Lays", 20, 30),
    (104, "Kurkure", 20, 18),
    (105, "Maggi", 15, 25),
    (106, "Oreo", 30, 12),
    (107, "Sprite", 40, 20),
    (108, "Dairy Milk", 50, 10)
]


for product in products:
    try:
        add_product(
            product[0],
            product[1],
            product[2],
            product[3]
        )

        print(f"Added: {product[1]}")

    except Exception as e:
        print(f"Could not add {product[1]}: {e}")
