from billing import generate_bill
shop = {
    "name": "ABC Kirana Store",
    "gst_registered": True,
    "gstin": "09ABCDE1234F1Z5"
}

items = [
    {
        "name": "Maggi",
        "price": 14,
        "quantity": 2,
        "gst_rate": 5
    },
    {
        "name": "Aashirvaad Atta",
        "price": 280,
        "quantity": 1,
        "gst_rate": 5
    },
    {
        "name": "Dove Soap",
        "price": 55,
        "quantity": 1,
        "gst_rate": 18
    }
]
bill = generate_bill(
    items=items,
    shop=shop,
    discount_type="percentage",
    discount_value=10,
    payment_method="Cash",
    amount_paid=400
)

print(bill["receipt"])
print("PDF saved at:", bill["pdf_path"])
