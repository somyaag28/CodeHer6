"""
test_database.py

Tests the inventory database module.
"""

from inventory import (
    create_database,
    add_product,
    get_product,
    get_all_products,
    deduct_stock
)


print("===================================")
print("DATABASE MODULE TEST")
print("===================================")


# Create database
create_database()
print("\nDatabase created successfully.")


# Add a test product
print("\n1. Adding test product...")

try:
    add_product(999, "Test Product", 100, 10)
    print("SUCCESS: Product added.")
except Exception as e:
    print("FAILED:", e)


# Find the test product
print("\n2. Finding test product...")

product = get_product(999)

if product is not None:
    print("SUCCESS: Product found.")
    print("Product:", product)
else:
    print("FAILED: Product not found.")


# Get all products
print("\n3. Getting all products...")

products = get_all_products()

print("SUCCESS: Inventory retrieved.")
print("Number of products:", len(products))


# Deduct stock
print("\n4. Deducting stock...")

success, message = deduct_stock(999, 2)

if success:
    print("SUCCESS:", message)

    updated_product = get_product(999)
    print("Updated product:", updated_product)
else:
    print("FAILED:", message)


# Test insufficient stock
print("\n5. Testing insufficient stock...")

success, message = deduct_stock(999, 100)

if not success:
    print("SUCCESS:", message)
else:
    print("FAILED: Stock should not have been deducted.")


# Test invalid quantity
print("\n6. Testing invalid quantity...")

success, message = deduct_stock(999, 0)

if not success:
    print("SUCCESS:", message)
else:
    print("FAILED: Zero quantity should be rejected.")


print("\n===================================")
print("TESTING COMPLETE")
print("===================================")
