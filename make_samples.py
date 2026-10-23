import os
from PIL import Image, ImageDraw, ImageFont

def get_tamil_font(size=18):
    try:
        font_path = "C:\\Windows\\Fonts\\Nirmala.ttc"
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
    except Exception:
        pass
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

def create_sample_memo_image(output_path, memo_no, date_str, veh_no, driver_name, route_from, route_to, freight, diesel, toll, food, loading, unloading, adv, other, is_tamil=False, has_mismatch=False):
    width, height = 820, 1080
    img = Image.new('RGB', (width, height), color='#FFFDF8')  # Realistic off-white paper
    draw = ImageDraw.Draw(img)

    font_title = get_tamil_font(24)
    font_header = get_tamil_font(18)
    font_body = get_tamil_font(16)
    font_small = get_tamil_font(14)
    font_bold = get_tamil_font(17)

    # Outer border
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline='#1E293B', width=3)
    draw.rectangle([(25, 25), (width - 25, height - 25)], outline='#64748B', width=1)

    # Header
    if is_tamil:
        draw.text((width // 2 - 210, 45), "ஸ்ரீ வெங்கடேஸ்வரா ரோட்வேஸ்", fill='#0F172A', font=font_title)
        draw.text((width // 2 - 160, 80), "லாரி டிரிப் மெமோ / வழி ரசீது", fill='#0369A1', font=font_header)
        draw.text((width // 2 - 190, 110), "தினசரி சரக்கு போக்குவரத்து: தமிழ்நாடு, கேரளா", fill='#475569', font=font_small)
    else:
        draw.text((width // 2 - 190, 45), "SRI VENKATESWARA ROADWAYS", fill='#0F172A', font=font_title)
        draw.text((width // 2 - 140, 80), "TRIP MEMO / LORRY WAY BILL", fill='#0369A1', font=font_header)
        draw.text((width // 2 - 210, 110), "Daily Goods Service: Tamil Nadu, Karnataka & Kerala", fill='#475569', font=font_small)

    draw.line([(35, 140), (width - 35, 140)], fill='#0F172A', width=2)

    # Details Grid
    y = 160
    if is_tamil:
        draw.text((50, y), f"மெமோ எண் (MEMO NO): {memo_no}", fill='#0F172A', font=font_bold)
        draw.text((500, y), f"தேதி (DATE): {date_str}", fill='#0F172A', font=font_bold)
        y += 40
        draw.text((50, y), f"வண்டி எண் (VEHICLE): {veh_no}", fill='#0F172A', font=font_bold)
        draw.text((500, y), f"ஓட்டுநர் (DRIVER): {driver_name}", fill='#0F172A', font=font_bold)
        y += 40
        draw.text((50, y), f"புறப்படும் இடம் (FROM): {route_from}", fill='#0F172A', font=font_bold)
        draw.text((500, y), f"செல்லும் இடம் (TO): {route_to}", fill='#0F172A', font=font_bold)
    else:
        draw.text((50, y), f"MEMO NO: {memo_no}", fill='#0F172A', font=font_bold)
        draw.text((500, y), f"DATE: {date_str}", fill='#0F172A', font=font_bold)
        y += 40
        draw.text((50, y), f"VEHICLE NO: {veh_no}", fill='#0F172A', font=font_bold)
        draw.text((500, y), f"DRIVER: {driver_name}", fill='#0F172A', font=font_bold)
        y += 40
        draw.text((50, y), f"FROM (SOURCE): {route_from}", fill='#0F172A', font=font_bold)
        draw.text((500, y), f"TO (DESTINATION): {route_to}", fill='#0F172A', font=font_bold)

    y += 45
    draw.line([(35, y), (width - 35, y)], fill='#94A3B8', width=1)

    # Freight Header
    y += 20
    draw.rectangle([(45, y), (width - 45, y + 40)], fill='#F1F5F9', outline='#CBD5E1')
    if is_tamil:
        draw.text((60, y + 10), "வாடகை விவரம் (FREIGHT & INCOME)", fill='#0F172A', font=font_bold)
        draw.text((550, y + 10), "தொகை (INR)", fill='#0F172A', font=font_bold)
    else:
        draw.text((60, y + 10), "FREIGHT & INCOME DETAILS", fill='#0F172A', font=font_bold)
        draw.text((550, y + 10), "AMOUNT (INR)", fill='#0F172A', font=font_bold)

    y += 50
    if is_tamil:
        draw.text((60, y), "லாரி வாடகை (Agreed Freight):", fill='#334155', font=font_body)
        draw.text((550, y), f"Rs. {freight:,.2f}", fill='#0F172A', font=font_bold)
        y += 35
        draw.text((60, y), "கழித்தல்: முன்பணம் (Driver Advance):", fill='#334155', font=font_body)
        draw.text((550, y), f"Rs. {adv:,.2f}", fill='#DC2626', font=font_bold)
    else:
        draw.text((60, y), "Trip Agreed Freight Amount:", fill='#334155', font=font_body)
        draw.text((550, y), f"Rs. {freight:,.2f}", fill='#0F172A', font=font_bold)
        y += 35
        draw.text((60, y), "Less: Advance Received by Driver:", fill='#334155', font=font_body)
        draw.text((550, y), f"Rs. {adv:,.2f}", fill='#DC2626', font=font_bold)

    # Operating Expenses Particulars
    y += 55
    draw.rectangle([(45, y), (width - 45, y + 40)], fill='#E2E8F0', outline='#94A3B8')
    if is_tamil:
        draw.text((60, y + 10), "பயண செலவு விவரங்கள் (TRIP EXPENSES)", fill='#0F172A', font=font_bold)
        draw.text((550, y + 10), "தொகை (INR)", fill='#0F172A', font=font_bold)
    else:
        draw.text((60, y + 10), "TRIP OPERATING EXPENSES PARTICULARS", fill='#0F172A', font=font_bold)
        draw.text((550, y + 10), "AMOUNT (INR)", fill='#0F172A', font=font_bold)

    if is_tamil:
        expenses = [
            ("டீசல் செலவு (Diesel Expense)", diesel),
            ("சுங்கம் / டோல் (Toll Plaza / Fastag)", toll),
            ("ஓட்டுநர் படி / சாப்பாடு (Driver Food & Bata)", food),
            ("ஏற்று கூலி (Loading Coolie Charges)", loading),
            ("இறக்கு கூலி (Unloading Hamali Charges)", unloading),
            ("இதர செலவு (Other / Maintenance / Weighbridge)", other)
        ]
    else:
        expenses = [
            ("Diesel Expense (Diecel / HSD)", diesel),
            ("Toll Plaza / Fastag", toll),
            ("Driver Food & Bata Allowance", food),
            ("Loading Coolie Charges", loading),
            ("Unloading / Hamali Charges", unloading),
            ("Other / Maintenance / Weighbridge", other)
        ]

    calculated_total = sum(e[1] for e in expenses)
    # If testing math mismatch, perturb handwritten total
    handwritten_total = (calculated_total + 1500.0) if has_mismatch else calculated_total

    y += 50
    for label, amt in expenses:
        draw.text((60, y), f"- {label}", fill='#334155', font=font_body)
        draw.text((550, y), f"Rs. {amt:,.2f}", fill='#0F172A', font=font_bold)
        draw.line([(55, y + 25), (width - 55, y + 25)], fill='#F1F5F9', width=1)
        y += 35

    # Total Expenses Box
    y += 15
    draw.rectangle([(45, y), (width - 45, y + 45)], fill='#FEF2F2', outline='#F87171')
    total_label = "மொத்த செலவு (TOTAL TRIP EXPENSES):" if is_tamil else "TOTAL TRIP EXPENSES:"
    draw.text((60, y + 12), total_label, fill='#991B1B', font=font_bold)
    draw.text((550, y + 12), f"Rs. {handwritten_total:,.2f}", fill='#991B1B', font=font_bold)

    # Net Profit Calculation Box
    profit = freight - calculated_total
    y += 65
    box_color = '#ECFDF5' if profit >= 0 else '#FEF2F2'
    border_color = '#10B981' if profit >= 0 else '#EF4444'
    text_color = '#065F46' if profit >= 0 else '#991B1B'

    draw.rectangle([(45, y), (width - 45, y + 55)], fill=box_color, outline=border_color, width=2)
    profit_label = "நிகர லாபம் (ESTIMATED NET PROFIT):" if is_tamil else "NET ESTIMATED PROFIT:"
    draw.text((60, y + 16), profit_label, fill=text_color, font=font_bold)
    draw.text((550, y + 16), f"Rs. {profit:,.2f}", fill=text_color, font=font_bold)

    # Signatures
    y = height - 120
    draw.line([(60, y), (250, y)], fill='#64748B', width=1)
    draw.text((80, y + 10), "Driver Signature" if not is_tamil else "ஓட்டுநர் கையொப்பம்", fill='#475569', font=font_small)

    draw.line([(width - 260, y), (width - 60, y)], fill='#64748B', width=1)
    draw.text((width - 230, y + 10), "Authorized Signatory", fill='#475569', font=font_small)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Generated sample memo: {output_path}")

def create_sample_fuel_receipt(output_path, station, bill_no, date_str, time_str, veh_no, qty, rate, total):
    width, height = 450, 750
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    draw.rectangle([(10, 10), (width - 10, height - 10)], outline='#CBD5E1', width=1)

    y = 35
    draw.text((width // 2 - 80, y), station.upper(), fill='#0F172A')
    y += 25
    draw.text((width // 2 - 110, y), "HIGHWAY EXPRESS FUEL STATION", fill='#475569')
    y += 20
    draw.text((width // 2 - 90, y), "GSTIN: 33AABCS1234F1Z8", fill='#64748B')
    y += 25
    draw.line([(25, y), (width - 25, y)], fill='#0F172A', width=1)

    y += 20
    draw.text((35, y), f"INVOICE NO: {bill_no}", fill='#0F172A')
    y += 25
    draw.text((35, y), f"DATE: {date_str}   TIME: {time_str}", fill='#0F172A')
    y += 25
    draw.text((35, y), f"VEHICLE NO: {veh_no}", fill='#0F172A')
    y += 25
    draw.text((35, y), f"PRODUCT: DIESEL (HSD)", fill='#0F172A')

    y += 30
    draw.line([(25, y), (width - 25, y)], fill='#CBD5E1', width=1)

    y += 20
    draw.text((35, y), "RATE / LTR:", fill='#334155')
    draw.text((280, y), f"Rs. {rate:.2f}", fill='#0F172A')

    y += 30
    draw.text((35, y), "VOLUME (QTY):", fill='#334155')
    draw.text((280, y), f"{qty:.2f} LTR", fill='#0F172A')

    y += 35
    draw.line([(25, y), (width - 25, y)], fill='#0F172A', width=2)

    y += 20
    draw.text((35, y), "TOTAL AMOUNT:", fill='#0F172A')
    draw.text((280, y), f"Rs. {total:,.2f}", fill='#0F172A')

    y += 35
    draw.line([(25, y), (width - 25, y)], fill='#0F172A', width=2)

    y += 40
    draw.text((width // 2 - 70, y), "MODE: CASH / CARD", fill='#475569')
    y += 25
    draw.text((width // 2 - 85, y), "THANK YOU! VISIT AGAIN", fill='#64748B')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Generated sample fuel bill: {output_path}")

if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "static", "sample_memos")
    
    # 1. English Memo (Ariyalur -> Chennai Harbour)
    create_sample_memo_image(
        os.path.join(base, "sample_memo_1.png"),
        "MEMO-2026-001", "12/08/2026", "TN 28 AB 1234", "Murugan Selvam",
        "Ariyalur", "Chennai Harbour", 48000.0, 21500.0, 3200.0, 2200.0, 3000.0, 2000.0, 15000.0, 500.0
    )
    # 2. Tamil Memo (Salem -> Coimbatore)
    create_sample_memo_image(
        os.path.join(base, "sample_memo_2.png"),
        "MEMO-2026-002", "19/08/2026", "TN 28 AB 1234", "குமார் (Kumar)",
        "சேலம் (Salem)", "கோவை (Coimbatore)", 26000.0, 12500.0, 1600.0, 1400.0, 1500.0, 1200.0, 8000.0, 300.0,
        is_tamil=True
    )
    # 3. Mixed Tanglish Memo (Hosur -> Tuticorin)
    create_sample_memo_image(
        os.path.join(base, "sample_memo_3.png"),
        "MEMO-2026-003", "22/08/2026", "TN 30 CD 5678", "Karthik Pandian",
        "Hosur", "Tuticorin", 42000.0, 31000.0, 4800.0, 2800.0, 3200.0, 2600.0, 10000.0, 800.0
    )
    # Fuel Bills
    create_sample_fuel_receipt(
        os.path.join(base, "sample_fuel_bill_1.png"),
        "INDIAN OIL", "IOCL-B7721", "12/08/2026", "14:35", "TN 28 AB 1234", 180.0, 95.5, 17190.0
    )
    create_sample_fuel_receipt(
        os.path.join(base, "sample_fuel_bill_2.png"),
        "BHARAT PETROLEUM", "BPCL-99014", "13/08/2026", "09:15", "TN 28 AB 1234", 45.0, 95.8, 4311.0
    )
    create_sample_fuel_receipt(
        os.path.join(base, "sample_fuel_bill_3.png"),
        "HINDUSTAN PETROLEUM", "HPCL-6652", "22/08/2026", "18:20", "TN 30 CD 5678", 320.0, 96.0, 30720.0
    )
