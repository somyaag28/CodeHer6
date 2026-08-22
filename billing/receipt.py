
import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm


# =================================================
# FONT SETUP
# =================================================

# DejaVu Sans supports the ₹ symbol.
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

pdfmetrics.registerFont(
    TTFont("DejaVu", font_path)
)

pdfmetrics.registerFont(
    TTFont("DejaVu-Bold", bold_font_path)
)


# =================================================
# TEXT RECEIPT
# =================================================

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

    receipt += (
        f"{'ITEM':<18}"
        f"{'QTY':>5}"
        f"{'RATE':>10}"
        f"{'AMOUNT':>12}\n"
    )

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

    receipt += (
        f"{'Subtotal':<33}"
        f"₹{subtotal:>10.2f}\n"
    )

    receipt += (
        f"{'Discount':<33}"
        f"₹{discount:>10.2f}\n"
    )

    if shop["gst_registered"]:

        receipt += (
            f"{'GST':<33}"
            f"₹{gst:>10.2f}\n"
        )

    receipt += "-" * 45 + "\n"

    receipt += (
        f"{'TOTAL':<33}"
        f"₹{total:>10.2f}\n"
    )

    receipt += "-" * 45 + "\n"

    receipt += f"Payment Method : {payment_method}\n"
    receipt += f"Amount Paid    : ₹{amount_paid:.2f}\n"
    receipt += f"Change         : ₹{change:.2f}\n"

    receipt += "=" * 45 + "\n"

    receipt += (
        f"{'Thank you for shopping with us!':^45}\n"
    )

    receipt += "=" * 45 + "\n"

    return receipt


# =================================================
# PDF RECEIPT
# =================================================

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

    # ---------------------------------------------
    # Create receipt folder
    # ---------------------------------------------

    receipt_folder = "receipts"

    os.makedirs(
        receipt_folder,
        exist_ok=True
    )

    # PDF filename

    file_path = os.path.join(
        receipt_folder,
        f"{bill_number}.pdf"
    )

    # ---------------------------------------------
    # Create PDF
    # ---------------------------------------------

    pdf = canvas.Canvas(
        file_path,
        pagesize=A4
    )

    width, height = A4

    # ---------------------------------------------
    # Colors
    # ---------------------------------------------

    green = colors.HexColor("#187A3D")
    light_green = colors.HexColor("#EAF5EC")
    grey = colors.HexColor("#666666")
    light_grey = colors.HexColor("#DDDDDD")

    left = 20 * mm
    right = width - 20 * mm

    # ---------------------------------------------
    # HEADER
    # ---------------------------------------------

    y = height - 25 * mm

    pdf.setFillColor(green)

    pdf.setFont(
        "DejaVu-Bold",
        22
    )

    pdf.drawCentredString(
        width / 2,
        y,
        shop["name"].upper()
    )

    y -= 8 * mm

    pdf.setFillColor(grey)

    pdf.setFont(
        "DejaVu",
        10
    )

    pdf.drawCentredString(
        width / 2,
        y,
        "Your Everyday Essentials"
    )

    y -= 10 * mm

    pdf.setStrokeColor(green)

    pdf.line(
        left,
        y,
        right,
        y
    )

    # ---------------------------------------------
    # BILL INFORMATION
    # ---------------------------------------------

    y -= 10 * mm

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "DejaVu-Bold",
        10
    )

    pdf.drawString(
        left,
        y,
        "Invoice No."
    )

    pdf.setFont(
        "DejaVu",
        10
    )

    pdf.drawString(
        left + 30 * mm,
        y,
        f":  {bill_number}"
    )

    y -= 6 * mm

    pdf.setFont(
        "DejaVu-Bold",
        10
    )

    pdf.drawString(
        left,
        y,
        "Date"
    )

    pdf.setFont(
        "DejaVu",
        10
    )

    pdf.drawString(
        left + 30 * mm,
        y,
        f":  {date_time}"
    )

    if shop["gst_registered"]:

        y -= 6 * mm

        pdf.setFont(
            "DejaVu-Bold",
            10
        )

        pdf.drawString(
            left,
            y,
            "GSTIN"
        )

        pdf.setFont(
            "DejaVu",
            10
        )

        pdf.drawString(
            left + 30 * mm,
            y,
            f":  {shop.get('gstin', 'Not Provided')}"
        )

    y -= 8 * mm

    pdf.setStrokeColor(green)

    pdf.line(
        left,
        y,
        right,
        y
    )

    # ---------------------------------------------
    # ITEM TABLE HEADER
    # ---------------------------------------------

    y -= 10 * mm

    pdf.setFillColor(green)

    pdf.roundRect(
        left,
        y - 7 * mm,
        right - left,
        9 * mm,
        2 * mm,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(colors.white)

    pdf.setFont(
        "DejaVu-Bold",
        10
    )

    pdf.drawString(
        left + 5 * mm,
        y - 4 * mm,
        "ITEM"
    )

    pdf.drawCentredString(
        left + 105 * mm,
        y - 4 * mm,
        "QTY"
    )

    pdf.drawRightString(
        left + 145 * mm,
        y - 4 * mm,
        "RATE (₹)"
    )

    pdf.drawRightString(
        right - 5 * mm,
        y - 4 * mm,
        "AMOUNT (₹)"
    )

    # ---------------------------------------------
    # ITEMS
    # ---------------------------------------------

    y -= 15 * mm

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "DejaVu",
        10
    )

    for item in items:

        amount = (
            item["price"]
            * item["quantity"]
        )

        pdf.drawString(
            left + 5 * mm,
            y,
            item["name"][:35]
        )

        pdf.drawCentredString(
            left + 105 * mm,
            y,
            str(item["quantity"])
        )

        pdf.drawRightString(
            left + 145 * mm,
            y,
            f"{item['price']:.2f}"
        )

        pdf.drawRightString(
            right - 5 * mm,
            y,
            f"{amount:.2f}"
        )

        y -= 4 * mm

        pdf.setStrokeColor(light_grey)

        pdf.line(
            left,
            y,
            right,
            y
        )

        y -= 7 * mm

    # ---------------------------------------------
    # SUMMARY
    # ---------------------------------------------

    y -= 5 * mm

    summary_x = width - 85 * mm

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "DejaVu",
        10
    )

    pdf.drawString(
        summary_x,
        y,
        "Subtotal"
    )

    pdf.drawRightString(
        right,
        y,
        f"₹{subtotal:.2f}"
    )

    y -= 7 * mm

    pdf.drawString(
        summary_x,
        y,
        "Discount"
    )

    pdf.drawRightString(
        right,
        y,
        f"₹{discount:.2f}"
    )

    # ---------------------------------------------
    # GST BREAKDOWN
    # ---------------------------------------------

    if shop["gst_registered"]:

        y -= 8 * mm

        pdf.setFont(
            "DejaVu-Bold",
            10
        )

        pdf.drawString(
            summary_x,
            y,
            "GST"
        )

        pdf.setFont(
            "DejaVu",
            9
        )

        gst_by_rate = {}

        subtotal_before_discount = 0

        for item in items:

            amount = (
                item["price"]
                * item["quantity"]
            )

            subtotal_before_discount += amount

            rate = item.get(
                "gst_rate",
                0
            )

            gst_by_rate.setdefault(
                rate,
                0
            )

            gst_by_rate[rate] += amount

        if subtotal_before_discount > 0:

            taxable_ratio = (
                subtotal_before_discount - discount
            ) / subtotal_before_discount

        else:

            taxable_ratio = 0

        gst_y = y

        for rate in sorted(gst_by_rate):

            taxable_amount = (
                gst_by_rate[rate]
                * taxable_ratio
            )

            rate_gst = (
                taxable_amount
                * rate
                / 100
            )

            gst_y -= 6 * mm

            pdf.drawString(
                summary_x + 15 * mm,
                gst_y,
                f"{rate}% GST"
            )

            pdf.drawRightString(
                right,
                gst_y,
                f"₹{rate_gst:.2f}"
            )

        y = gst_y

        y -= 7 * mm

        pdf.setStrokeColor(light_grey)

        pdf.line(
            summary_x,
            y,
            right,
            y
        )

        y -= 7 * mm

        pdf.setFont(
            "DejaVu-Bold",
            10
        )

        pdf.drawString(
            summary_x + 15 * mm,
            y,
            "Total GST"
        )

        pdf.drawRightString(
            right,
            y,
            f"₹{gst:.2f}"
        )

    # ---------------------------------------------
    # TOTAL
    # ---------------------------------------------

    y -= 10 * mm

    pdf.setStrokeColor(green)

    pdf.line(
        summary_x - 5 * mm,
        y,
        right,
        y
    )

    y -= 9 * mm

    pdf.setFillColor(green)

    pdf.setFont(
        "DejaVu-Bold",
        15
    )

    pdf.drawString(
        summary_x,
        y,
        "TOTAL"
    )

    pdf.drawRightString(
        right,
        y,
        f"₹{total:.2f}"
    )

    # ---------------------------------------------
    # PAYMENT DETAILS
    # ---------------------------------------------

    y -= 15 * mm

    box_height = 28 * mm

    pdf.setFillColor(light_green)

    pdf.roundRect(
        left,
        y - box_height,
        right - left,
        box_height,
        3 * mm,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(green)

    pdf.setFont(
        "DejaVu-Bold",
        11
    )

    pdf.drawString(
        left + 6 * mm,
        y - 7 * mm,
        "PAYMENT DETAILS"
    )

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "DejaVu",
        9
    )

    pdf.drawString(
        left + 6 * mm,
        y - 16 * mm,
        "Method"
    )

    pdf.setFont(
        "DejaVu-Bold",
        10
    )

    pdf.drawString(
        left + 6 * mm,
        y - 22 * mm,
        payment_method
    )

    pdf.setFont(
        "DejaVu",
        9
    )

    pdf.drawString(
        left + 75 * mm,
        y - 16 * mm,
        "Amount Paid"
    )

    pdf.setFont(
        "DejaVu-Bold",
        10
    )

    pdf.drawString(
        left + 75 * mm,
        y - 22 * mm,
        f"₹{amount_paid:.2f}"
    )

    pdf.setFont(
        "DejaVu",
        9
    )

    pdf.drawString(
        left + 135 * mm,
        y - 16 * mm,
        "Change"
    )

    pdf.setFont(
        "DejaVu-Bold",
        10
    )

    pdf.drawString(
        left + 135 * mm,
        y - 22 * mm,
        f"₹{change:.2f}"
    )

    # ---------------------------------------------
    # FOOTER
    # ---------------------------------------------

    y -= box_height + 18 * mm

    pdf.setStrokeColor(green)

    pdf.line(
        width / 2 - 35 * mm,
        y,
        width / 2 + 35 * mm,
        y
    )

    y -= 8 * mm

    pdf.setFillColor(green)

    pdf.setFont(
        "DejaVu-Bold",
        12
    )

    pdf.drawCentredString(
        width / 2,
        y,
        "Thank you for shopping with us!"
    )

    # ---------------------------------------------
    # SAVE PDF
    # ---------------------------------------------

    pdf.save()

    return file_path
