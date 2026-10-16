import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
ASSETS = "/home/ashok/RSA Gym/assets"
OUT = "/home/ashok/RSA Gym/social_posts"
os.makedirs(OUT, exist_ok=True)

FONT_EB = "/usr/share/fonts/TTF/FiraSans-ExtraBold.ttf"
FONT_B = "/usr/share/fonts/TTF/FiraSans-Bold.ttf"
FONT_R = "/usr/share/fonts/TTF/FiraSans-Regular.ttf"

def get_font(path, size):
    return ImageFont.truetype(path, size)

def create_base_canvas(bg_image_path, overlay_opacity=0.78, top_gradient=True):
    canvas = Image.new("RGBA", (W, H), (10, 12, 18, 255))
    if os.path.exists(bg_image_path):
        bg = Image.open(bg_image_path).convert("RGBA")
        # Resize to cover
        ratio = max(W / bg.width, H / bg.height)
        new_size = (int(bg.width * ratio), int(bg.height * ratio))
        bg = bg.resize(new_size, Image.Resampling.LANCZOS)
        # Center crop
        left = (bg.width - W) // 2
        top = (bg.height - H) // 2
        bg = bg.crop((left, top, left + W, top + H))
        canvas.paste(bg, (0, 0))

    # Dark overlay with slight blur feel
    overlay = Image.new("RGBA", (W, H), (7, 8, 12, int(255 * overlay_opacity)))
    canvas = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(canvas)

    # Top & bottom gradients
    for y in range(250):
        alpha = int(220 * (1 - y / 250))
        draw.line([(0, y), (W, y)], fill=(5, 6, 9, alpha))
    for y in range(H - 220, H):
        alpha = int(240 * ((y - (H - 220)) / 220))
        draw.line([(0, y), (W, y)], fill=(5, 6, 9, alpha))

    # Outer border
    draw.rectangle([(20, 20), (W - 20, H - 20)], outline=(255, 42, 42, 60), width=2)
    return canvas, draw

def draw_header_and_footer(draw, category_text, is_navratri=False):
    # Top Logo Brand
    f_brand = get_font(FONT_EB, 36)
    f_sub = get_font(FONT_B, 18)
    f_cat = get_font(FONT_B, 20)
    f_foot = get_font(FONT_B, 20)

    # Brand Title
    draw.text((60, 60), "RSA", font=f_brand, fill=(255, 255, 255, 255))
    draw.text((135, 60), "PRO FITNESS", font=f_brand, fill=(255, 42, 42, 255))
    draw.text((60, 105), "ANAITH, ARA • PREMIER HEALTH CLUB", font=f_sub, fill=(180, 185, 200, 255))

    # Category Pill
    cat_bg = (245, 158, 11, 230) if is_navratri else (255, 42, 42, 230)
    cat_text_color = (0, 0, 0, 255) if is_navratri else (255, 255, 255, 255)
    
    # Calculate pill box
    bbox = f_cat.getbbox(category_text)
    pw = bbox[2] - bbox[0] + 36
    ph = 42
    px = W - 60 - pw
    py = 65
    draw.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=12, fill=cat_bg)
    draw.text((px + 18, py + 8), category_text, font=f_cat, fill=cat_text_color)

    # Footer Action Bar
    draw.line([(60, H - 120), (W - 60, H - 120)], fill=(255, 255, 255, 40), width=1)
    draw.text((60, H - 95), "📍 Deo Vihar, Near Bazaar Samiti Gate, Anaith, Ara", font=f_foot, fill=(200, 205, 220, 255))
    draw.text((W - 320, H - 95), "📲 DM @rsaprofitness 🔖", font=f_foot, fill=(255, 180, 40, 255))

# ==========================================
# 1. NAVRATRI POST 1: Fasting & Muscle Loss
# ==========================================
def build_post_1():
    img_path = f"{ASSETS}/indian_athlete_festive_fitness.jpg"
    canvas, draw = create_base_canvas(img_path, overlay_opacity=0.76)
    draw_header_and_footer(draw, "🕉️ NAVRATRI SPECIAL", is_navratri=True)

    # Headline
    f_hook = get_font(FONT_EB, 58)
    f_title = get_font(FONT_EB, 50)
    f_body_b = get_font(FONT_B, 26)
    f_body = get_font(FONT_R, 23)

    draw.text((60, 200), "NAVRATRI FASTING MEIN", font=f_hook, fill=(255, 190, 40, 255))
    draw.text((60, 270), "MUSCLE LOSS KAISE ROKEIN?", font=f_title, fill=(255, 255, 255, 255))

    # Translucent Content Card
    card = Image.new("RGBA", (W - 120, 680), (18, 22, 34, 215))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle([(0, 0), (W - 120, 680)], radius=24, outline=(245, 158, 11, 100), width=2)
    canvas.paste(card, (60, 370), card)

    # Bullets inside Card
    tips = [
        ("1. Prioritize Satvik Protein Sources", "Vrat me Paneer (cottage cheese), Curd (dahi), roasted Makhana aur Peanuts zaroor include karein. Ye muscles ko catabolic state se bachate hain."),
        ("2. Shift Workout Timing to Post-Falahar", "Khaali pet heavy exercise na karein. Falahar ya fruits khane ke 60-90 mins baad shaam ko moderate workout karein."),
        ("3. Hydration & Sendha Namak Balance", "Water retention aur energy drop se bachne ke liye nariyal pani ya nimbu-pani me sendha namak lein. Dehydration se muscle cramps aate hain."),
        ("4. Keep Intensity Moderate (12-15 Reps)", "Vrat ke dauran 1-rep max PRs try na karein. Light to moderate weights ke sath consistency maintain karein.")
    ]

    y_cur = 410
    for title, desc in tips:
        draw.text((95, y_cur), title, font=f_body_b, fill=(255, 190, 40, 255))
        # Word wrap desc
        words = desc.split()
        lines = []
        cur_l = ""
        for w in words:
            if len(cur_l + " " + w) < 68:
                cur_l += " " + w
            else:
                lines.append(cur_l.strip())
                cur_l = w
        if cur_l:
            lines.append(cur_l.strip())
        
        y_text = y_cur + 38
        for line in lines:
            draw.text((95, y_text), line, font=f_body, fill=(225, 230, 240, 255))
            y_text += 32
        y_cur = y_text + 25

    # Save button badge
    draw.rounded_rectangle([(60, 1090), (W - 60, 1170)], radius=18, fill=(255, 42, 42, 235))
    f_btn = get_font(FONT_EB, 26)
    draw.text((120, 1115), "FREE NAVRATRI DIET PLAN CHAHIYE? COMMENT 'VRAT' 👇", font=f_btn, fill=(255, 255, 255, 255))

    canvas.convert("RGB").save(f"{OUT}/post_01_navratri_fasting_muscle.jpg", "JPEG", quality=90)
    print("Post 1 created")

# ==========================================
# 2. NAVRATRI POST 2: Satvik Diet Chart
# ==========================================
def build_post_2():
    img_path = f"{ASSETS}/navratri_satvik_fitness_food.jpg"
    canvas, draw = create_base_canvas(img_path, overlay_opacity=0.76)
    draw_header_and_footer(draw, "🕉️ NUTRITION GUIDE", is_navratri=True)

    f_hook = get_font(FONT_EB, 56)
    f_title = get_font(FONT_EB, 44)
    f_item_b = get_font(FONT_EB, 26)
    f_item = get_font(FONT_R, 22)
    f_macro = get_font(FONT_B, 22)

    draw.text((60, 200), "HIGH PROTEIN NAVRATRI", font=f_hook, fill=(255, 190, 40, 255))
    draw.text((60, 270), "SATVIK DIET BLUEPRINT", font=f_title, fill=(255, 255, 255, 255))

    card = Image.new("RGBA", (W - 120, 680), (16, 20, 30, 220))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle([(0, 0), (W - 120, 680)], radius=24, outline=(245, 158, 11, 100), width=2)
    canvas.paste(card, (60, 370), card)

    meals = [
        ("🌅 MORNING (Breakfast):", "1 Glass Milk / Badam Shake + 1 Banana + Handful of soaked almonds & walnuts", "12g Protein"),
        ("☀️ MID-DAY (Lunch / Falahar):", "100g Fresh Paneer (raw or lightly tossed in ghee with jeera) + 1 Bowl Thick Curd (Dahi)", "26g Protein"),
        ("🌆 PRE-WORKOUT (Evening Snack):", "Roasted Makhana (1 bowl) + Handful Roasted Peanuts + Coconut Water", "14g Protein"),
        ("🌙 POST-WORKOUT / DINNER:", "Kuttu / Singhara Atta Rotis (2) + Boiled Aloo or Pumpkin Sabzi + Paneer Bhurji / Curd", "20g Protein"),
    ]

    y_cur = 410
    for label, desc, macro in meals:
        draw.text((95, y_cur), label, font=f_item_b, fill=(255, 190, 40, 255))
        draw.text((W - 270, y_cur), macro, font=f_macro, fill=(74, 222, 128, 255))

        words = desc.split()
        lines = []
        cur_l = ""
        for w in words:
            if len(cur_l + " " + w) < 68:
                cur_l += " " + w
            else:
                lines.append(cur_l.strip())
                cur_l = w
        if cur_l:
            lines.append(cur_l.strip())

        y_text = y_cur + 38
        for line in lines:
            draw.text((95, y_text), line, font=f_item, fill=(225, 230, 240, 255))
            y_text += 30
        y_cur = y_text + 30

    draw.rounded_rectangle([(60, 1090), (W - 60, 1170)], radius=18, fill=(245, 158, 11, 235))
    f_btn = get_font(FONT_EB, 26)
    draw.text((100, 1115), "TOTAL PROTEIN: ~72g+ DAILY SATVIK INTAKE 🥗", font=f_btn, fill=(0, 0, 0, 255))

    canvas.convert("RGB").save(f"{OUT}/post_02_navratri_satvik_diet_chart.jpg", "JPEG", quality=90)
    print("Post 2 created")

# ==========================================
# 3. NAVRATRI POST 3: Workout Rules (Do's & Don'ts)
# ==========================================
def build_post_3():
    img_path = f"{ASSETS}/hero_indian_athletes.jpg"
    canvas, draw = create_base_canvas(img_path, overlay_opacity=0.82)
    draw_header_and_footer(draw, "🕉️ VRAT WORKOUT RULES", is_navratri=True)

    f_hook = get_font(FONT_EB, 56)
    f_title = get_font(FONT_EB, 44)
    f_col_h = get_font(FONT_EB, 32)
    f_item = get_font(FONT_B, 21)

    draw.text((60, 200), "NAVRATRI WORKOUT GUIDE", font=f_hook, fill=(255, 190, 40, 255))
    draw.text((60, 270), "DO'S vs DON'TS IN THE GYM", font=f_title, fill=(255, 255, 255, 255))

    # Two Column Cards
    col_w = (W - 150) // 2
    # Do's Card (Left)
    do_card = Image.new("RGBA", (col_w, 680), (16, 32, 22, 220))
    do_draw = ImageDraw.Draw(do_card)
    do_draw.rounded_rectangle([(0, 0), (col_w, 680)], radius=20, outline=(74, 222, 128, 150), width=2)
    canvas.paste(do_card, (60, 370), do_card)

    # Don'ts Card (Right)
    dont_card = Image.new("RGBA", (col_w, 680), (32, 16, 20, 220))
    dont_draw = ImageDraw.Draw(dont_card)
    dont_draw.rounded_rectangle([(0, 0), (col_w, 680)], radius=20, outline=(239, 68, 68, 150), width=2)
    canvas.paste(dont_card, (60 + col_w + 30, 370), dont_card)

    # Headers
    draw.text((90, 400), "✅ DO THIS (Sahi Tarika)", font=f_col_h, fill=(74, 222, 128, 255))
    draw.text((60 + col_w + 60, 400), "❌ AVOID THIS (Galtiyan)", font=f_col_h, fill=(248, 113, 113, 255))

    dos = [
        "Workout 45-50 mins max",
        "Keep 12 to 15 reps per set",
        "Drink Nariyal Pani / Nimbu water",
        "Focus on light cardio & stretching",
        "Eat banana / dates 45m before gym",
        "Get 7-8 hours deep sleep"
    ]
    donts = [
        "Do NOT lift 1-Rep Heavy Max",
        "Never workout on empty stomach",
        "Avoid 1-hour intense HIIT cardio",
        "Don't binge on deep-fried pakodas",
        "Don't ignore dizziness or nausea",
        "Do not skip sendha namak minerals"
    ]

    y_d = 470
    for d in dos:
        draw.text((90, y_d), f"• {d}", font=f_item, fill=(230, 245, 235, 255))
        y_d += 65

    y_dn = 470
    for dn in donts:
        draw.text((60 + col_w + 60, y_dn), f"• {dn}", font=f_item, fill=(255, 230, 230, 255))
        y_dn += 65

    draw.rounded_rectangle([(60, 1090), (W - 60, 1170)], radius=18, fill=(255, 42, 42, 235))
    f_btn = get_font(FONT_EB, 26)
    draw.text((110, 1115), "NAVRATRI MEIN BHI WORKOUT CONTINUE RAKHIYE! 💪", font=f_btn, fill=(255, 255, 255, 255))

    canvas.convert("RGB").save(f"{OUT}/post_03_navratri_workout_rules.jpg", "JPEG", quality=90)
    print("Post 3 created")

# ==========================================
# 4. AWARENESS POST 4: Free Diet Blueprint Lead Magnet
# ==========================================
def build_post_4():
    img_path = f"{ASSETS}/navratri_satvik_fitness_food.jpg"
    canvas, draw = create_base_canvas(img_path, overlay_opacity=0.82)
    draw_header_and_footer(draw, "🎁 FOLLOWER SPECIAL", is_navratri=False)

    f_hook = get_font(FONT_EB, 58)
    f_title = get_font(FONT_EB, 46)
    f_sub = get_font(FONT_B, 28)
    f_step_h = get_font(FONT_EB, 30)
    f_step = get_font(FONT_R, 23)

    draw.text((60, 200), "FREE INDIAN DIET PLAN", font=f_hook, fill=(255, 42, 42, 255))
    draw.text((60, 270), "FOR FAT LOSS & MUSCLE GAIN", font=f_title, fill=(255, 255, 255, 255))
    draw.text((60, 335), "Customized for Vegetarian & Non-Veg Diet in Bihar", font=f_sub, fill=(255, 190, 40, 255))

    card = Image.new("RGBA", (W - 120, 680), (18, 22, 34, 225))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle([(0, 0), (W - 120, 680)], radius=24, outline=(255, 42, 42, 100), width=2)
    canvas.paste(card, (60, 390), card)

    steps = [
        ("Step 1: Follow @rsaprofitness", "Hamare page ko follow karein for daily verified gym tips in Ara."),
        ("Step 2: Comment 'DIET' Below", "Comment section me 'DIET' likhiye."),
        ("Step 3: Instant WhatsApp / DM Blueprint", "Hamari team aapko direct complete Meal Timetable, Calorie Breakdown aur Grocery List send karegi!"),
        ("Bonus Included:", "✅ Vegetarian high-protein options (Soya, Paneer, Dahi, Daal)\n✅ Student-friendly budget meal ideas\n✅ Zero starving • 100% realistic Indian food")
    ]

    y_s = 430
    for s_title, s_desc in steps:
        draw.text((95, y_s), s_title, font=f_step_h, fill=(255, 190, 40, 255))
        y_text = y_s + 42
        for line in s_desc.split("\n"):
            draw.text((95, y_text), line, font=f_step, fill=(225, 230, 240, 255))
            y_text += 32
        y_s = y_text + 25

    draw.rounded_rectangle([(60, 1110), (W - 60, 1180)], radius=18, fill=(34, 197, 94, 235))
    f_btn = get_font(FONT_EB, 26)
    draw.text((120, 1130), "CLAIM YOUR FREE DIET PLAN TODAY • LIMITED TIME 📲", font=f_btn, fill=(255, 255, 255, 255))

    canvas.convert("RGB").save(f"{OUT}/post_04_free_custom_diet_blueprint.jpg", "JPEG", quality=90)
    print("Post 4 created")

# ==========================================
# 5. AWARENESS POST 5: 3 Fitness Myths Busted in Ara
# ==========================================
def build_post_5():
    img_path = f"{ASSETS}/indian_male_lifting.jpg"
    canvas, draw = create_base_canvas(img_path, overlay_opacity=0.82)
    draw_header_and_footer(draw, "💡 FITNESS MYTH BUSTER", is_navratri=False)

    f_hook = get_font(FONT_EB, 56)
    f_title = get_font(FONT_EB, 44)
    f_myth_h = get_font(FONT_EB, 26)
    f_myth = get_font(FONT_R, 22)

    draw.text((60, 200), "3 BIGGEST FITNESS MYTHS", font=f_hook, fill=(255, 42, 42, 255))
    draw.text((60, 270), "STOPPING RESULTS IN ARA", font=f_title, fill=(255, 255, 255, 255))

    card = Image.new("RGBA", (W - 120, 680), (18, 22, 34, 225))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle([(0, 0), (W - 120, 680)], radius=24, outline=(255, 42, 42, 100), width=2)
    canvas.paste(card, (60, 370), card)

    myths = [
        ("MYTH 1: 'Roti aur Chawal chhodne se hi pet kam hoga'", "REALITY: Weight loss overall calorie deficit se hota hai, roti-chawal chhodne se nahi. Portion control karein aur protein intake badhayein."),
        ("MYTH 2: 'Gym chhodte hi body latak jayegi / motapa aayega'", "REALITY: Ye tab hota hai jab gym chhodne ke baad diet bigad jati hai aur physical activity zero ho jati hai. Muscle fat me convert nahi hota!"),
        ("MYTH 3: 'Sirf Cardio karne se belly fat jaldi kam hoga'", "REALITY: Sirf running se stamina badhega, lekin shape weight training se aati hai. Weight training rest ke dauran bhi calories burn karti hai.")
    ]

    y_m = 410
    for m_title, m_desc in myths:
        draw.text((95, y_m), m_title, font=f_myth_h, fill=(248, 113, 113, 255))
        
        words = m_desc.split()
        lines = []
        cur_l = ""
        for w in words:
            if len(cur_l + " " + w) < 66:
                cur_l += " " + w
            else:
                lines.append(cur_l.strip())
                cur_l = w
        if cur_l:
            lines.append(cur_l.strip())

        y_text = y_m + 38
        for line in lines:
            draw.text((95, y_text), line, font=f_myth, fill=(225, 230, 240, 255))
            y_text += 32
        y_m = y_text + 35

    draw.rounded_rectangle([(60, 1090), (W - 60, 1170)], radius=18, fill=(255, 42, 42, 235))
    f_btn = get_font(FONT_EB, 26)
    draw.text((110, 1115), "RIGHT SCIENCE = REAL RESULTS • JOIN RSA GYM ARA 💪", font=f_btn, fill=(255, 255, 255, 255))

    canvas.convert("RGB").save(f"{OUT}/post_05_fitness_myths_busted.jpg", "JPEG", quality=90)
    print("Post 5 created")

# ==========================================
# 6. AWARENESS POST 6: Women Weightlifting Facts
# ==========================================
def build_post_6():
    img_path = f"{ASSETS}/indian_female_fitness.jpg"
    canvas, draw = create_base_canvas(img_path, overlay_opacity=0.78)
    draw_header_and_footer(draw, "🌸 WOMEN'S FITNESS", is_navratri=False)

    f_hook = get_font(FONT_EB, 54)
    f_title = get_font(FONT_EB, 44)
    f_h = get_font(FONT_EB, 26)
    f_body = get_font(FONT_R, 22)

    draw.text((60, 200), "DEAR ARA WOMEN:", font=f_hook, fill=(244, 114, 182, 255))
    draw.text((60, 265), "WEIGHT LIFTING WON'T MAKE YOU BULKY!", font=f_title, fill=(255, 255, 255, 255))

    card = Image.new("RGBA", (W - 120, 680), (24, 18, 30, 225))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle([(0, 0), (W - 120, 680)], radius=24, outline=(244, 114, 182, 120), width=2)
    canvas.paste(card, (60, 360), card)

    facts = [
        ("1. Women Lack Testosterone", "Female body me testosterone bohot kam hota hai, isliye weights uthane se mardana muscles nahi bante, balki toned aur slim shape aati hai."),
        ("2. Faster Belly & Thigh Fat Loss", "Resistance training metabolic rate ko tez karta hai, jisse body workout ke baad bhi stubborn fat burn karti rehti hai."),
        ("3. Stronger Bones & Joint Health", "Age badhne par women me calcium loss aur back pain common hota hai. Weight training bones aur posture ko majboot banata hai."),
        ("4. Exclusive Ladies Batch at RSA Gym", "⏰ 10:30 AM to 12:30 PM: 100% Privacy, zero male entry, clean washrooms, and female comfort priority in Ara.")
    ]

    y_f = 400
    for f_head, f_desc in facts:
        draw.text((95, y_f), f_head, font=f_h, fill=(244, 114, 182, 255))
        words = f_desc.split()
        lines = []
        cur_l = ""
        for w in words:
            if len(cur_l + " " + w) < 66:
                cur_l += " " + w
            else:
                lines.append(cur_l.strip())
                cur_l = w
        if cur_l:
            lines.append(cur_l.strip())

        y_text = y_f + 36
        for line in lines:
            draw.text((95, y_text), line, font=f_body, fill=(235, 235, 245, 255))
            y_text += 30
        y_f = y_text + 25

    draw.rounded_rectangle([(60, 1080), (W - 60, 1160)], radius=18, fill=(219, 39, 119, 235))
    f_btn = get_font(FONT_EB, 26)
    draw.text((120, 1105), "JOIN OUR LADIES SPECIAL BATCH • 1-DAY FREE TRIAL 🎟️", font=f_btn, fill=(255, 255, 255, 255))

    canvas.convert("RGB").save(f"{OUT}/post_06_women_weightlifting_facts.jpg", "JPEG", quality=90)
    print("Post 6 created")

# ==========================================
# 7. AWARENESS POST 7: Police & Army Physical Prep
# ==========================================
def build_post_7():
    img_path = f"{ASSETS}/indian_trainer_coaching.jpg"
    canvas, draw = create_base_canvas(img_path, overlay_opacity=0.82)
    draw_header_and_footer(draw, "🎖️ DEFENSE ASPIRANTS", is_navratri=False)

    f_hook = get_font(FONT_EB, 54)
    f_title = get_font(FONT_EB, 44)
    f_h = get_font(FONT_EB, 26)
    f_desc = get_font(FONT_R, 22)

    draw.text((60, 200), "BIHAR POLICE & ARMY ASPIRANTS:", font=f_hook, fill=(245, 158, 11, 255))
    draw.text((60, 265), "HOW TO HIT 10+ PULL-UPS & HIGH JUMP", font=f_title, fill=(255, 255, 255, 255))

    card = Image.new("RGBA", (W - 120, 680), (18, 24, 32, 225))
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle([(0, 0), (W - 120, 680)], radius=24, outline=(245, 158, 11, 100), width=2)
    canvas.paste(card, (60, 360), card)

    drills = [
        ("1. Dead Hangs (Grip Strength)", "Roz workout ke end me 45-60 seconds bar par latkein. Strong grip ke bina pull-ups count kabhi nahi badhega."),
        ("2. Negative Pull-ups (Eccentric Strength)", "Jump karke chin bar ke upar le jayein aur 5 seconds tak dheere-dheere neeche aayein. Ye back lats ko fast develop karta hai."),
        ("3. Explosive Squats & Calf Raises", "High Jump aur 1600m running speed ke liye quadriceps aur calves me explosive power zaroori hai."),
        ("4. Special Student & Physical Exam Discount", "Bihar Police SI/Constable aur Army exam aspirants ke liye RSA Gym me special batch aur discount uplabdh hai!")
    ]

    y_d = 400
    for h_txt, b_txt in drills:
        draw.text((95, y_d), h_txt, font=f_h, fill=(245, 158, 11, 255))
        words = b_txt.split()
        lines = []
        cur_l = ""
        for w in words:
            if len(cur_l + " " + w) < 66:
                cur_l += " " + w
            else:
                lines.append(cur_l.strip())
                cur_l = w
        if cur_l:
            lines.append(cur_l.strip())

        y_text = y_d + 36
        for line in lines:
            draw.text((95, y_text), line, font=f_desc, fill=(230, 235, 245, 255))
            y_text += 30
        y_d = y_text + 25

    draw.rounded_rectangle([(60, 1080), (W - 60, 1160)], radius=18, fill=(234, 88, 12, 235))
    f_btn = get_font(FONT_EB, 26)
    draw.text((110, 1105), "PRACTICE AT RSA GYM • DEO VIHAR, ANAITH, ARA 🇮🇳", font=f_btn, fill=(255, 255, 255, 255))

    canvas.convert("RGB").save(f"{OUT}/post_07_police_army_pullup_guide.jpg", "JPEG", quality=90)
    print("Post 7 created")

if __name__ == "__main__":
    build_post_1()
    build_post_2()
    build_post_3()
    build_post_4()
    build_post_5()
    build_post_6()
    build_post_7()
    print("All 7 social graphics created successfully!")
