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
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os


def generate_pdf_receipt(
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
    # Create a temporary receipts folder
    receipt_folder = "receipts"
    os.makedirs(receipt_folder, exist_ok=True)

    # File name
    file_path = os.path.join(
        receipt_folder,
        f"{bill_number}.pdf"
    )

    # Create PDF
    pdf = canvas.Canvas(file_path, pagesize=A4)

    width, height = A4

    # Starting position
    x = 20 * mm
    y = height - 20 * mm

    # Shop name
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(
        width / 2,
        y,
        shop["name"]
    )

    y -= 10 * mm

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        x,
        y,
        f"Bill No: {bill_number}"
    )

    y -= 6 * mm

    pdf.drawString(
        x,
        y,
        f"Date: {date_time}"
    )

    y -= 6 * mm

    if shop["gst_registered"]:
        pdf.drawString(
            x,
            y,
            f"GSTIN: {shop.get('gstin', 'Not Provided')}"
        )
        y -= 6 * mm

    # Line
    pdf.line(
        x,
        y,
        width - x,
        y
    )

    y -= 8 * mm

    # Table headings
    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawString(x, y, "ITEM")
    pdf.drawString(x + 75 * mm, y, "QTY")
    pdf.drawString(x + 95 * mm, y, "RATE")
    pdf.drawString(x + 125 * mm, y, "AMOUNT")

    y -= 5 * mm

    pdf.line(
        x,
        y,
        width - x,
        y
    )

    y -= 7 * mm

    # Items
    pdf.setFont("Helvetica", 10)

    for item in items:

        amount = item["price"] * item["quantity"]

        name = item["name"][:30]

        pdf.drawString(
            x,
            y,
            name
        )

        pdf.drawRightString(
            x + 90 * mm,
            y,
            str(item["quantity"])
        )

        pdf.drawRightString(
            x + 120 * mm,
            y,
            f"₹{item['price']:.2f}"
        )

        pdf.drawRightString(
            width - x,
            y,
            f"₹{amount:.2f}"
        )

        y -= 6 * mm

    # Summary
    y -= 5 * mm

    pdf.line(
        x,
        y,
        width - x,
        y
    )

    y -= 8 * mm

    pdf.drawRightString(
        width - x,
        y,
        f"Subtotal: ₹{subtotal:.2f}"
    )

    y -= 6 * mm

    pdf.drawRightString(
        width - x,
        y,
        f"Discount: ₹{discount:.2f}"
    )

    if shop["gst_registered"]:

        y -= 6 * mm

        pdf.drawRightString(
            width - x,
            y,
            f"GST: ₹{gst:.2f}"
        )

    y -= 8 * mm

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawRightString(
        width - x,
        y,
        f"TOTAL: ₹{total:.2f}"
    )

    y -= 10 * mm

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        x,
        y,
        f"Payment Method: {payment_method}"
    )

    y -= 6 * mm

    pdf.drawString(
        x,
        y,
        f"Amount Paid: ₹{amount_paid:.2f}"
    )

    y -= 6 * mm

    pdf.drawString(
        x,
        y,
        f"Change: ₹{change:.2f}"
    )

    # Footer
    y -= 15 * mm

    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawCentredString(
        width / 2,
        y,
        "Thank you for shopping with us!"
    )

    # Save PDF
    pdf.save()

    return file_path
