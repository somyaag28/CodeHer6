from datetime import datetime

from billing.validation import (
    validate_items,
    validate_discount,
    validate_payment
)

from billing.receipt import (
    generate_receipt,
    generate_pdf_receipt
)

bill_counter = 1

def generate_bill_number():

    global bill_counter

    bill_number = f"INV-{bill_counter:04d}"

    bill_counter += 1

    return bill_number
def calculate_subtotal(items):

    subtotal = 0

    for item in items:
        subtotal += item["price"] * item["quantity"]

    return subtotal
def calculate_discount(subtotal, discount_type=None, discount_value=0):

    if discount_type == "percentage":

        discount = subtotal * discount_value / 100

    elif discount_type == "fixed":

        discount = discount_value

    else:

        discount = 0

    return discount
def calculate_gst(items, taxable_ratio, gst_registered):

    if not gst_registered:
        return 0

    total_gst = 0

    for item in items:

        item_amount = item["price"] * item["quantity"]

        taxable_amount = item_amount * taxable_ratio

        gst_rate = item.get("gst_rate", 0)

        total_gst += taxable_amount * gst_rate / 100

    return total_gst
def process_payment(total, payment_method, amount_paid):

    valid_methods = ["Cash", "UPI", "Card"]

    if payment_method not in valid_methods:
        raise ValueError(
            "Payment method must be Cash, UPI, or Card."
        )

    validate_payment(total, amount_paid)

    return amount_paid - total
def generate_bill(
    items,
    shop,
    discount_type=None,
    discount_value=0,
    payment_method="Cash",
    amount_paid=None
):

    validate_items(items)

    subtotal = calculate_subtotal(items)

    validate_discount(
        subtotal,
        discount_type,
        discount_value
    )

    discount = calculate_discount(
        subtotal,
        discount_type,
        discount_value
    )

    taxable_amount = subtotal - discount

    if subtotal > 0:
        taxable_ratio = taxable_amount / subtotal
    else:
        taxable_ratio = 0

    gst = calculate_gst(
        items,
        taxable_ratio,
        shop["gst_registered"]
    )

    total = taxable_amount + gst

    subtotal = round(subtotal, 2)
    discount = round(discount, 2)
    gst = round(gst, 2)
    total = round(total, 2)

    if amount_paid is None:
        amount_paid = total

    change = process_payment(
        total,
        payment_method,
        amount_paid
    )

    change = round(change, 2)

    bill_number = generate_bill_number()

    date_time = datetime.now().strftime(
        "%d-%m-%Y %I:%M:%S %p"
    )

    receipt = generate_receipt(
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
    )
    pdf_path = generate_pdf_receipt(
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
)

    return {
        "bill_number": bill_number,
        "date_time": date_time,
        "subtotal": subtotal,
        "discount": discount,
        "gst": gst,
        "total": total,
        "payment_method": payment_method,
        "amount_paid": amount_paid,
        "change": change,
        "receipt": receipt,
        "pdf_path": pdf_path
    }
