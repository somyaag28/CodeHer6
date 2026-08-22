def generate_receipt(
    items,
    shop,
    bill_number,
    subtotal,
    discount,
    gst,
    total,
    payment_method,
    amount_paid,
    change,
    date_time
):

    receipt = ""

    receipt += "=" * 45 + "\n"
    receipt += f"{shop['name']:^45}\n"
    receipt += "=" * 45 + "\n"

    receipt += f"Bill No : {bill_number}\n"
    receipt += f"Date    : {date_time}\n"

    if shop["gst_registered"]:
        receipt += f"GSTIN   : {shop.get('gstin', 'Not Provided')}\n"

    receipt += "-" * 45 + "\n"

    receipt += f"{'ITEM':<18}{'QTY':>5}{'RATE':>10}{'AMOUNT':>12}\n"
    receipt += "-" * 45 + "\n"

    for item in items:

        amount = item["price"] * item["quantity"]

        name = item["name"][:18]

        receipt += (
            f"{name:<18}"
            f"{item['quantity']:>5}"
            f"{item['price']:>10.2f}"
            f"{amount:>12.2f}\n"
        )

    receipt += "-" * 45 + "\n"

    receipt += f"{'Subtotal':<33}₹{subtotal:>10.2f}\n"
    receipt += f"{'Discount':<33}₹{discount:>10.2f}\n"

    if shop["gst_registered"]:
        receipt += f"{'GST':<33}₹{gst:>10.2f}\n"

    receipt += "-" * 45 + "\n"
    receipt += f"{'TOTAL':<33}₹{total:>10.2f}\n"
    receipt += "-" * 45 + "\n"

    receipt += f"Payment Method : {payment_method}\n"
    receipt += f"Amount Paid    : ₹{amount_paid:.2f}\n"
    receipt += f"Change         : ₹{change:.2f}\n"

    receipt += "=" * 45 + "\n"
    receipt += f"{'Thank you for shopping with us!':^45}\n"
    receipt += "=" * 45 + "\n"

    return receipt
