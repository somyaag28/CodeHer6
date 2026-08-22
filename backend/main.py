from fastapi import FastAPI, UploadFile, File, Form
from backend.matching import match_image
from billing.billing import generate_bill
from database.inventory import (
    add_product,
    get_product,
    get_all_products,
    deduct_stock
)
from ai_model import extract_embedding

import json
import os


app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "CodeHer6 API is running"
    }


@app.post("/identify")
def identify(image: UploadFile = File(...)):
    os.makedirs("images", exist_ok=True)

    image_path = f"images/scan_{image.filename}"

    with open(image_path, "wb") as file:
        file.write(image.file.read())

    product = match_image(image_path)

    return product


@app.post("/products")
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    gst_rate: float = Form(0),
    image: UploadFile = File(...)
):
    # Get the next product ID
    existing_products = get_all_products()

    if existing_products:
        product_id = max(product[0] for product in existing_products) + 1
    else:
        product_id = 101

    # Create images folder
    os.makedirs("images", exist_ok=True)

    # Save the uploaded image
    image_path = f"images/{product_id}_{image.filename}"

    with open(image_path, "wb") as file:
        file.write(image.file.read())

    # Create AI embedding from the image
    embedding = extract_embedding(image_path)

    # Convert embedding to text so SQLite can store it
    embedding_text = json.dumps(embedding)

    # Save product + embedding in database
    add_product(
        product_id=product_id,
        name=name,
        price=price,
        stock=stock,
        gst_rate=gst_rate,
        image_path=image_path,
        embedding=embedding_text
    )

    return {
        "message": "Product added successfully",
        "product_id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "gst_rate": gst_rate,
        "image_path": image_path,
        "embedding_created": True
    }


@app.post("/checkout")
def checkout(product_id: int, quantity: int = 1):
    # Find the product in the database
    product = get_product(product_id)

    if product is None:
        return {
            "error": "Product not found"
        }

    # Get product information
    name = product[1]
    price = product[2]
    stock = product[3]
    gst_rate = product[4]

    # Check stock
    if quantity <= 0:
        return {
            "error": "Invalid quantity"
        }

    if quantity > stock:
        return {
            "error": "Not enough stock"
        }

    # Create the billing item
    items = [
        {
            "name": name,
            "price": price,
            "quantity": quantity,
            "gst_rate": gst_rate
        }
    ]

    shop = {
        "name": "CodeHer6 Store",
        "gst_registered": True,
        "gstin": "TEST123"
    }

    # Generate bill
    bill = generate_bill(
        items,
        shop,
        payment_method="Cash"
    )

    # Deduct stock after successful billing
    success, message = deduct_stock(
        product_id,
        quantity
    )

    if not success:
        return {
            "error": message
        }

    return {
        "message": "Checkout successful",
        "product": name,
        "quantity": quantity,
        "bill": bill,
        "stock_update": message
    }

    return bill