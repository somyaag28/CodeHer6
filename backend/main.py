from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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


# =================================================
# CORS
# =================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =================================================
# SERVE GENERATED PDF RECEIPTS
# =================================================

os.makedirs("receipts", exist_ok=True)

app.mount(
    "/receipts",
    StaticFiles(directory="receipts"),
    name="receipts"
)


# =================================================
# HOME
# =================================================

@app.get("/")
def home():
    return {
        "message": "CodeHer6 API is running"
    }


# =================================================
# IDENTIFY PRODUCT
# =================================================

@app.post("/identify")
def identify(image: UploadFile = File(...)):

    os.makedirs("images", exist_ok=True)

    image_path = f"images/scan_{image.filename}"

    with open(image_path, "wb") as file:
        file.write(image.file.read())

    product = match_image(image_path)

    return product


# =================================================
# ADD PRODUCT
# =================================================

@app.post("/products")
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    gst_rate: float = Form(0),
    image: UploadFile = File(...)
):

    existing_products = get_all_products()

    if existing_products:
        product_id = max(
            product[0]
            for product in existing_products
        ) + 1
    else:
        product_id = 101

    os.makedirs("images", exist_ok=True)

    image_path = f"images/{product_id}_{image.filename}"

    with open(image_path, "wb") as file:
        file.write(image.file.read())

    embedding = extract_embedding(image_path)

    embedding_text = json.dumps(embedding)

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


# =================================================
# INVENTORY
# =================================================

@app.get("/inventory")
def inventory():

    products = get_all_products()

    result = []

    for product in products:

        result.append({
            "id": product[0],
            "name": product[1],
            "price": product[2],
            "stock": product[3],
            "gst_rate": product[4],
            "image_path": product[5]
        })

    return result


# =================================================
# CHECKOUT
# =================================================

@app.post("/checkout")
def checkout(
    product_id: int,
    quantity: int = 1
):

    # ---------------------------------------------
    # Find product
    # ---------------------------------------------

    product = get_product(product_id)

    if product is None:
        return {
            "error": "Product not found"
        }

    name = product[1]
    price = product[2]
    stock = product[3]
    gst_rate = product[4]

    # ---------------------------------------------
    # Validate quantity
    # ---------------------------------------------

    if quantity <= 0:
        return {
            "error": "Invalid quantity"
        }

    if quantity > stock:
        return {
            "error": "Not enough stock"
        }

    # ---------------------------------------------
    # Create billing item
    # ---------------------------------------------

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

    # ---------------------------------------------
    # USE SAN'S BILLING SYSTEM
    # ---------------------------------------------

    bill = generate_bill(
        items,
        shop,
        payment_method="Cash"
    )

    # ---------------------------------------------
    # Deduct stock
    # ---------------------------------------------

    success, message = deduct_stock(
        product_id,
        quantity
    )

    if not success:
        return {
            "error": message
        }

    # ---------------------------------------------
    # PDF URL
    # ---------------------------------------------

    pdf_filename = os.path.basename(
        bill["pdf_path"]
    )

    pdf_url = f"/receipts/{pdf_filename}"

    # ---------------------------------------------
    # Return everything to frontend
    # ---------------------------------------------

    return {
        "message": "Checkout successful",

        "product": {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity,
            "remaining_stock": stock - quantity
        },

        "bill": bill,

        "pdf_url": pdf_url,

        "stock_update": message
    }