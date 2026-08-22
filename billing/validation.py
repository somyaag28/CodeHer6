def validate_items(items):
    if not items:
        raise ValueError("Bill cannot be empty.")

    for item in items:

        if "name" not in item:
            raise ValueError("Product name is missing.")

        if "price" not in item:
            raise ValueError(f"Price missing for {item['name']}.")

        if "quantity" not in item:
            raise ValueError(f"Quantity missing for {item['name']}.")

        if item["price"] < 0:
            raise ValueError(f"Invalid price for {item['name']}.")

        if item["quantity"] <= 0:
            raise ValueError(f"Invalid quantity for {item['name']}.")

        if item.get("gst_rate", 0) < 0 or item.get("gst_rate", 0) > 100:
            raise ValueError(f"Invalid GST rate for {item['name']}.")


def validate_discount(subtotal, discount_type, discount_value):

    if discount_value < 0:
        raise ValueError("Discount cannot be negative.")

    if discount_type == "percentage":

        if discount_value > 100:
            raise ValueError("Percentage discount cannot exceed 100%.")

    elif discount_type == "fixed":

        if discount_value > subtotal:
            raise ValueError("Discount cannot exceed subtotal.")

    elif discount_type is not None:

        raise ValueError("Invalid discount type.")


def validate_payment(total, amount_paid):

    if amount_paid < total:
        raise ValueError(
            f"Insufficient payment. Amount required: ₹{total:.2f}"
        )

    if amount_paid < 0:
        raise ValueError("Payment cannot be negative.")
