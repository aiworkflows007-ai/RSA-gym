import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
ASSETS = "/home/ashok/RSA Gym/assets"
OUT = "/home/ashok/RSA Gym/social_posts"
os.makedirs(OUT, exist_ok=True)

FONT_EB = "/usr/share/fonts/TTF/FiraSans-ExtraBold.ttf"
FONT_B = "/usr/share/fonts/TTF/FiraSans-Bold.ttf"
FONT_R = "/usr/share/fonts/TTF/FiraSans-Regular.ttf"

def f_eb(size): return ImageFont.truetype(FONT_EB, size)
def f_b(size): return ImageFont.truetype(FONT_B, size)
def f_r(size): return ImageFont.truetype(FONT_R, size)

def make_circle_crop(img_path, size, border_color=(255, 60, 0), border_width=10):
    """Crops an image into a smooth circle with a vibrant glowing border."""
    im = Image.open(img_path).convert("RGBA")
    # Crop to square
    min_dim = min(im.width, im.height)
    left = (im.width - min_dim) // 2
    top = (im.height - min_dim) // 2
    im = im.crop((left, top, left + min_dim, top + min_dim))
    im = im.resize((size, size), Image.Resampling.LANCZOS)

    # Circular mask with antialiasing
    mask = Image.new("L", (size * 2, size * 2), 0)
    draw_m = ImageDraw.Draw(mask)
    draw_m.ellipse((0, 0, size * 2 - 1, size * 2 - 1), fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)

    # Output with border
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)

    # Border ring
    draw_out = ImageDraw.Draw(out)
    for i in range(border_width):
        draw_out.ellipse((i, i, size - 1 - i, size - 1 - i), outline=border_color)

    return out

def draw_pill(draw, x, y, w, h, text, font, bg_color, text_color):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=h // 2, fill=bg_color)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = x + (w - tw) // 2
    ty = y + (h - th) // 2 - 2
    draw.text((tx, ty), text, font=font, fill=text_color)

def draw_sticker(canvas, cx, cy, radius, text_top, text_bottom, bg_color=(255, 42, 42), text_color=(255, 255, 255)):
    """Draws a round promotional sticker badge like 'SAVE 30% OFF'."""
    sticker = Image.new("RGBA", (radius * 2, radius * 2), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sticker)
    s_draw.ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=bg_color)
    s_draw.ellipse((4, 4, radius * 2 - 5, radius * 2 - 5), outline=(255, 255, 255, 200), width=3)

    f1 = f_eb(int(radius * 0.34))
    f2 = f_eb(int(radius * 0.42))

    b1 = f1.getbbox(text_top)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    b2 = f2.getbbox(text_bottom)
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]

    s_draw.text((radius - w1 // 2, radius - h1 - 8), text_top, font=f1, fill=text_color)
    s_draw.text((radius - w2 // 2, radius + 2), text_bottom, font=f2, fill=text_color)

    canvas.paste(sticker, (cx - radius, cy - radius), sticker)

def base_poster(bg_img_path, overlay_color=(12, 14, 20), opacity=0.82):
    canvas = Image.new("RGBA", (W, H), (10, 12, 18, 255))
    if os.path.exists(bg_img_path):
        bg = Image.open(bg_img_path).convert("RGBA")
        ratio = max(W / bg.width, H / bg.height)
        new_size = (int(bg.width * ratio), int(bg.height * ratio))
        bg = bg.resize(new_size, Image.Resampling.LANCZOS)
        left = (bg.width - W) // 2
        top = (bg.height - H) // 2
        canvas.paste(bg.crop((left, top, left + W, top + H)), (0, 0))

    overlay = Image.new("RGBA", (W, H), (*overlay_color, int(255 * opacity)))
    canvas = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(canvas)

    # Outer neon border
    draw.rectangle([(20, 20), (W - 20, H - 20)], outline=(255, 60, 0, 70), width=2)
    return canvas, draw

def common_footer(draw, is_navratri=False):
    draw.line([(50, H - 110), (W - 50, H - 110)], fill=(255, 255, 255, 40), width=1)
    f_info = f_b(20)
    draw.text((50, H - 85), "📍 Deo Vihar, Near Bazaar Samiti Gate, Anaith, Ara", font=f_info, fill=(200, 205, 220, 255))
    draw.text((W - 350, H - 85), "📲 +91 8210453434 • FOLLOW US", font=f_info, fill=(255, 180, 40, 255))

# =========================================================================
# 🕉️ NAVRATRI POST 1: SHUBH NAVRATRI & INNER SHAKTI (With Devi Image Inset)
# =========================================================================
def create_navratri_post_1():
    bg_img = f"{ASSETS}/indian_athlete_festive_fitness.jpg"
    canvas, draw = base_poster(bg_img, overlay_color=(10, 8, 14), opacity=0.75)

    # Top Brand Header
    draw.text((60, 55), "RSA", font=f_eb(40), fill=(255, 255, 255, 255))
    draw.text((140, 55), "PRO FITNESS", font=f_eb(40), fill=(255, 60, 0, 255))
    draw.text((60, 105), "ANAITH, ARA • PREMIER HEALTH CLUB", font=f_b(18), fill=(180, 185, 200, 255))

    # Top Festive Badge
    draw_pill(draw, W - 360, 60, 300, 46, "🕉️ SHUBH NAVRATRI", f_eb(20), (255, 180, 20, 240), (0, 0, 0, 255))

    # Inset 1: Powerful Goddess Durga circular frame with golden glowing ring
    durga_circle = make_circle_crop(f"{ASSETS}/maa_durga_divine_art.jpg", 460, border_color=(255, 190, 20), border_width=10)
    canvas.paste(durga_circle, (W - 500, 220), durga_circle)

    # Inset 2: Indian Athlete circular frame overlapping
    athlete_circle = make_circle_crop(f"{ASSETS}/indian_athlete_festive_fitness.jpg", 300, border_color=(255, 60, 0), border_width=8)
    canvas.paste(athlete_circle, (W - 360, 560), athlete_circle)

    # Bold Left Typography
    draw.text((60, 220), "HAPPY", font=f_eb(74), fill=(255, 255, 255, 255))
    draw.text((60, 300), "NAVRATRI", font=f_eb(80), fill=(255, 190, 30, 255))
    draw.text((60, 395), "INVOKE YOUR", font=f_eb(46), fill=(255, 255, 255, 255))
    draw.text((60, 450), "INNER SHAKTI", font=f_eb(52), fill=(255, 60, 0, 255))

    # Short Motivational Bullet Points
    bullets = [
        "✨ Discipline • Devotion • Strength",
        "🏋️‍♂️ Maintain Muscle During 9 Days Vrat",
        "🥗 Pure High-Protein Satvik Nutrition"
    ]
    yb = 550
    for b in bullets:
        draw.text((60, yb), b, font=f_b(24), fill=(230, 235, 245, 255))
        yb += 45

    # Horizontal Pills (Inspired by Reference Image)
    pill_w = (W - 140) // 3
    draw_pill(draw, 60, 920, pill_w, 60, "SATVIK ENERGY", f_eb(20), (255, 180, 20, 220), (0, 0, 0, 255))
    draw_pill(draw, 60 + pill_w + 10, 920, pill_w, 60, "ACTIVE VRAT", f_eb(20), (255, 60, 0, 220), (255, 255, 255, 255))
    draw_pill(draw, 60 + (pill_w + 10) * 2, 920, pill_w, 60, "STRENGTH & GRIT", f_eb(20), (255, 180, 20, 220), (0, 0, 0, 255))

    # Big CTA Bar
    draw_pill(draw, 60, 1020, W - 120, 80, "CLAIM YOUR 1-DAY FREE TRIAL • FOLLOW @RSAPROFITNESS", f_eb(26), (255, 42, 42, 245), (255, 255, 255, 255))

    common_footer(draw, is_navratri=True)
    canvas.convert("RGB").save(f"{OUT}/post_01_navratri_shakti_fitness.jpg", "JPEG", quality=92)
    print("Navratri Post 1 generated")

# =========================================================================
# 🕉️ NAVRATRI POST 2: SATVIK POWER DIET (Maa Durga + Food Inset)
# =========================================================================
def create_navratri_post_2():
    bg_img = f"{ASSETS}/navratri_satvik_fitness_food.jpg"
    canvas, draw = base_poster(bg_img, overlay_color=(12, 10, 16), opacity=0.82)

    # Brand Header
    draw.text((60, 55), "RSA", font=f_eb(40), fill=(255, 255, 255, 255))
    draw.text((140, 55), "PRO FITNESS", font=f_eb(40), fill=(255, 60, 0, 255))
    draw_pill(draw, W - 360, 60, 300, 46, "🕉️ NAVRATRI DIET", f_eb(20), (255, 180, 20, 240), (0, 0, 0, 255))

    # Large Center Food Circular Inset
    food_circle = make_circle_crop(f"{ASSETS}/navratri_satvik_fitness_food.jpg", 520, border_color=(255, 180, 20), border_width=10)
    canvas.paste(food_circle, (W - 560, 280), food_circle)

    # Inset Durga Small Icon / Stamp on top-left of circle
    durga_stamp = make_circle_crop(f"{ASSETS}/maa_durga_divine_art.jpg", 180, border_color=(255, 42, 42), border_width=6)
    canvas.paste(durga_stamp, (W - 220, 230), durga_stamp)

    # Headline on Left
    draw.text((60, 200), "FUEL YOUR", font=f_eb(64), fill=(255, 255, 255, 255))
    draw.text((60, 275), "VRAT FAST", font=f_eb(74), fill=(255, 190, 30, 255))
    draw.text((60, 370), "70G+ SATVIK PROTEIN", font=f_eb(34), fill=(74, 222, 128, 255))
    draw.text((60, 415), "Zero Muscle Loss • High Energy", font=f_b(22), fill=(200, 205, 220, 255))

    # 4 Macro Cards on Left & Bottom
    macros = [
        ("🧀 PANEER (100g)", "26g Pure Protein"),
        ("🥣 THICK CURD (Dahi)", "12g Protein + Probiotics"),
        ("🥜 MAKHANA & NUTS", "14g Healthy Fats & Protein"),
        ("🥔 KUTTU & BANANA", "Clean Complex Carbs")
    ]
    ym = 480
    for name, desc in macros:
        draw_pill(draw, 60, ym, 420, 64, name, f_eb(22), (26, 30, 42, 240), (255, 190, 30, 255))
        draw.text((75, ym + 70), desc, font=f_b(18), fill=(220, 225, 240, 255))
        ym += 110

    # Discount / Bonus Sticker
    draw_sticker(canvas, 140, 970, 75, "100%", "FREE", bg_color=(34, 197, 94), text_color=(0, 0, 0))

    # Bottom CTA Box
    draw_pill(draw, 240, 930, W - 300, 80, "DM 'VRAT' TO GET FULL DIET CHART 📲", f_eb(25), (255, 60, 0, 240), (255, 255, 255, 255))

    common_footer(draw, is_navratri=True)
    canvas.convert("RGB").save(f"{OUT}/post_02_navratri_power_diet.jpg", "JPEG", quality=92)
    print("Navratri Post 2 generated")

# =========================================================================
# 🕉️ NAVRATRI POST 3: TIME TO GET FIT (Direct clone of Reference 2)
# =========================================================================
def create_navratri_post_3():
    bg_img = f"{ASSETS}/indian_athlete_festive_fitness.jpg"
    canvas, draw = base_poster(bg_img, overlay_color=(8, 10, 16), opacity=0.88)

    # Header
    draw.text((60, 55), "RSA", font=f_eb(40), fill=(255, 255, 255, 255))
    draw.text((140, 55), "PRO FITNESS", font=f_eb(40), fill=(255, 60, 0, 255))
    draw_pill(draw, W - 360, 60, 300, 46, "🕉️ FESTIVE SPECIAL", f_eb(20), (255, 180, 20, 240), (0, 0, 0, 255))

    # Huge Left Headline (Matches "TIME TO GET FIT" in reference)
    draw.text((60, 200), "TIME", font=f_eb(80), fill=(255, 100, 30, 255))
    draw.text((60, 280), "TO GET", font=f_eb(74), fill=(255, 100, 30, 255))
    draw.text((60, 360), "FIT.", font=f_eb(95), fill=(255, 255, 255, 255))

    # Big Circular Inset Frame on Right (Matches Reference 2 Circle Cutout)
    circle_frame = make_circle_crop(f"{ASSETS}/indian_male_lifting.jpg", 500, border_color=(255, 90, 0), border_width=12)
    canvas.paste(circle_frame, (W - 540, 220), circle_frame)

    # Inset Durga Emblem inside the circle
    devi_stamp = make_circle_crop(f"{ASSETS}/maa_durga_divine_art.jpg", 160, border_color=(255, 190, 30), border_width=5)
    canvas.paste(devi_stamp, (W - 200, 190), devi_stamp)

    # Middle Banner (Membership Sale)
    draw.line([(60, 520), (450, 520)], fill=(255, 255, 255, 60), width=2)
    draw.text((60, 545), "FESTIVE MEMBERSHIP SALE", font=f_eb(28), fill=(255, 255, 255, 255))
    draw.text((60, 590), "UPTO 30% OFF ON 3-MONTH BUNDLE", font=f_eb(26), fill=(255, 190, 30, 255))
    draw.line([(60, 640), (450, 640)], fill=(255, 255, 255, 60), width=2)

    # 4 Horizontal Pill Badges
    p_w = (W - 150) // 2
    draw_pill(draw, 60, 780, p_w, 65, "FREE DIET BLUEPRINT", f_eb(21), (255, 100, 30, 220), (255, 255, 255, 255))
    draw_pill(draw, 60 + p_w + 30, 780, p_w, 65, "LADIES SPECIAL BATCH", f_eb(21), (255, 180, 20, 220), (0, 0, 0, 255))
    draw_pill(draw, 60, 865, p_w, 65, "1-DAY FREE TRIAL", f_eb(21), (34, 197, 94, 220), (0, 0, 0, 255))
    draw_pill(draw, 60 + p_w + 30, 865, p_w, 65, "CERTIFIED TRAINERS", f_eb(21), (255, 100, 30, 220), (255, 255, 255, 255))

    # Bottom CTA Box
    draw_pill(draw, 60, 990, W - 120, 80, "CLAIM YOUR PASS ON WHATSAPP: +91 8210453434 🎟️", f_eb(25), (255, 42, 42, 245), (255, 255, 255, 255))

    common_footer(draw, is_navratri=True)
    canvas.convert("RGB").save(f"{OUT}/post_03_navratri_festive_sale.jpg", "JPEG", quality=92)
    print("Navratri Post 3 generated")

# =========================================================================
# 💡 AWARENESS POST 4: GET FIT, FEEL GREAT (Direct clone of Reference 1)
# =========================================================================
def create_awareness_post_4():
    bg_img = f"{ASSETS}/hero_indian_athletes.jpg"
    canvas, draw = base_poster(bg_img, overlay_color=(10, 12, 16), opacity=0.88)

    # Top Brand
    draw.text((60, 55), "RSA", font=f_eb(40), fill=(255, 255, 255, 255))
    draw.text((140, 55), "PRO FITNESS", font=f_eb(40), fill=(255, 60, 0, 255))
    draw_pill(draw, W - 330, 60, 270, 46, "🔥 JOIN THE ELITE", f_eb(20), (255, 60, 0, 240), (255, 255, 255, 255))

    # Massive Headline (Matches Reference 1)
    draw.text((60, 180), "GET", font=f_eb(92), fill=(255, 255, 255, 255))
    draw.text((60, 270), "FIT,", font=f_eb(92), fill=(255, 255, 255, 255))
    draw.text((60, 360), "FEEL GREAT.", font=f_eb(80), fill=(255, 150, 0, 255))

    # Athlete Inset Circle Frame on Right
    athlete_frame = make_circle_crop(f"{ASSETS}/indian_male_lifting.jpg", 480, border_color=(255, 150, 0), border_width=10)
    canvas.paste(athlete_frame, (W - 520, 200), athlete_frame)

    # 4 Horizontal Rounded Badges (Exact 2x2 grid from Reference 1)
    p_w = (W - 150) // 2
    draw_pill(draw, 60, 680, p_w, 65, "PERSONAL TRAINING", f_eb(22), (255, 150, 0, 230), (0, 0, 0, 255))
    draw_pill(draw, 60 + p_w + 30, 680, p_w, 65, "GROUP SESSIONS", f_eb(22), (255, 150, 0, 230), (0, 0, 0, 255))
    draw_pill(draw, 60, 765, p_w, 65, "CARDIO THEATER", f_eb(22), (255, 150, 0, 230), (0, 0, 0, 255))
    draw_pill(draw, 60 + p_w + 30, 765, p_w, 65, "FREE WEIGHT ZONE", f_eb(22), (255, 150, 0, 230), (0, 0, 0, 255))

    # Round Sticker Badge (Matches Reference)
    draw_sticker(canvas, W - 140, 660, 70, "1-DAY", "FREE", bg_color=(255, 42, 42), text_color=(255, 255, 255))

    # Bottom Lead Magnet Box
    draw_pill(draw, 60, 890, W - 120, 85, "COMMENT 'TRIAL' TO GET 1-DAY FREE PASS 🎟️", f_eb(26), (255, 42, 42, 245), (255, 255, 255, 255))

    # Subtitle Info
    draw.text((60, 1010), "Looking to transform your body with zero intimidation?", font=f_b(24), fill=(255, 255, 255, 255))
    draw.text((60, 1050), "Join Ara's cleanest, fully equipped fitness center today.", font=f_r(22), fill=(180, 185, 200, 255))

    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_04_get_fit_feel_great.jpg", "JPEG", quality=92)
    print("Awareness Post 4 generated")

# =========================================================================
# 💡 AWARENESS POST 5: GET IN SHAPE (Direct clone of Reference 3)
# =========================================================================
def create_awareness_post_5():
    bg_img = f"{ASSETS}/indian_male_lifting.jpg"
    canvas, draw = base_poster(bg_img, overlay_color=(8, 10, 14), opacity=0.88)

    # Top Brand
    draw.text((60, 55), "RSA", font=f_eb(40), fill=(255, 255, 255, 255))
    draw.text((140, 55), "PRO FITNESS", font=f_eb(40), fill=(255, 60, 0, 255))

    # Top Sticker (Matches "SAVE 30% OFF" in Reference 3)
    draw_sticker(canvas, 130, 220, 75, "SAVE", "30%", bg_color=(255, 60, 0), text_color=(255, 255, 255))

    # Huge Headline
    draw.text((230, 180), "GET IN", font=f_eb(76), fill=(255, 255, 255, 255))
    draw.text((230, 255), "SHAPE.", font=f_eb(85), fill=(255, 60, 0, 255))

    # Dual Picture-in-Picture Inset Cards
    card_w = (W - 150) // 2
    # Inset 1: Lifting
    in1 = Image.open(f"{ASSETS}/indian_male_lifting.jpg").convert("RGBA")
    in1 = in1.resize((card_w, 360), Image.Resampling.LANCZOS)
    canvas.paste(in1, (60, 390))
    draw.rectangle([(60, 390), (60 + card_w, 750)], outline=(255, 60, 0), width=4)
    draw_pill(draw, 75, 405, card_w - 30, 42, "STRENGTH TRAINING", f_eb(18), (0, 0, 0, 220), (255, 255, 255, 255))

    # Inset 2: Female Fitness
    in2 = Image.open(f"{ASSETS}/indian_female_fitness.jpg").convert("RGBA")
    in2 = in2.resize((card_w, 360), Image.Resampling.LANCZOS)
    canvas.paste(in2, (60 + card_w + 30, 390))
    draw.rectangle([(60 + card_w + 30, 390), (W - 60, 750)], outline=(255, 180, 20), width=4)
    draw_pill(draw, 60 + card_w + 45, 405, card_w - 30, 42, "CARDIO & TONING", f_eb(18), (0, 0, 0, 220), (255, 255, 255, 255))

    # 3 High-Impact Features
    feats = [
        ("✅ 100% IMPORTED MACHINES", "Smooth bio-mechanics, zero joint pain"),
        ("✅ CERTIFIED FLOOR TRAINERS", "Personalized posture and form guidance"),
        ("✅ ZERO INTIMIDATION ENVIRONMENT", "Friendly, respectful, and motivating")
    ]
    yf = 790
    for h_txt, sub in feats:
        draw.text((60, yf), h_txt, font=f_eb(24), fill=(255, 180, 20, 255))
        draw.text((60, yf + 32), sub, font=f_r(20), fill=(200, 205, 220, 255))
        yf += 70

    # Bottom Contact Bar (Matches Reference 3)
    draw_pill(draw, 60, 1020, W - 120, 75, "CALL FOR MEMBERSHIP OFFER: +91 8210453434 📞", f_eb(24), (255, 42, 42, 245), (255, 255, 255, 255))

    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_05_get_in_shape_sale.jpg", "JPEG", quality=92)
    print("Awareness Post 5 generated")

# =========================================================================
# 💡 AWARENESS POST 6: STRONG, TONED, CONFIDENT (Women's Special)
# =========================================================================
def create_awareness_post_6():
    bg_img = f"{ASSETS}/indian_female_fitness.jpg"
    canvas, draw = base_poster(bg_img, overlay_color=(16, 10, 18), opacity=0.84)

    # Top Brand
    draw.text((60, 55), "RSA", font=f_eb(40), fill=(255, 255, 255, 255))
    draw.text((140, 55), "PRO FITNESS", font=f_eb(40), fill=(244, 114, 182, 255))
    draw_pill(draw, W - 360, 60, 300, 46, "🌸 LADIES EXCLUSIVE", f_eb(20), (244, 114, 182, 240), (0, 0, 0, 255))

    # Circular Frame of Indian Female Athlete with Glowing Pink Ring
    women_circle = make_circle_crop(f"{ASSETS}/indian_female_fitness.jpg", 500, border_color=(244, 114, 182), border_width=10)
    canvas.paste(women_circle, (W - 540, 220), women_circle)

    # Bold Typography on Left
    draw.text((60, 200), "STRONG.", font=f_eb(74), fill=(255, 255, 255, 255))
    draw.text((60, 280), "TONED.", font=f_eb(74), fill=(244, 114, 182, 255))
    draw.text((60, 360), "CONFIDENT.", font=f_eb(68), fill=(255, 190, 30, 255))

    # Ladies Batch Timing Box
    draw.line([(60, 490), (460, 490)], fill=(255, 255, 255, 60), width=2)
    draw.text((60, 515), "DEDICATED LADIES BATCH", font=f_eb(28), fill=(255, 255, 255, 255))
    draw.text((60, 555), "⏰ 10:30 AM – 12:30 PM (MON-SAT)", font=f_eb(24), fill=(244, 114, 182, 255))
    draw.line([(60, 600), (460, 600)], fill=(255, 255, 255, 60), width=2)

    # 4 Rounded Badges
    p_w = (W - 150) // 2
    draw_pill(draw, 60, 750, p_w, 65, "100% PRIVACY", f_eb(22), (244, 114, 182, 220), (0, 0, 0, 255))
    draw_pill(draw, 60 + p_w + 30, 750, p_w, 65, "ZERO MALE ENTRY", f_eb(22), (255, 180, 20, 220), (0, 0, 0, 255))
    draw_pill(draw, 60, 835, p_w, 65, "FULL BODY TONING", f_eb(22), (244, 114, 182, 220), (0, 0, 0, 255))
    draw_pill(draw, 60 + p_w + 30, 835, p_w, 65, "CARDIO & WEIGHTS", f_eb(22), (255, 180, 20, 220), (0, 0, 0, 255))

    # Bottom CTA Box
    draw_pill(draw, 60, 970, W - 120, 85, "BOOK YOUR FREE LADIES BATCH PASS 🎟️", f_eb(25), (219, 39, 119, 245), (255, 255, 255, 255))

    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_06_women_fitness_exclusive.jpg", "JPEG", quality=92)
    print("Awareness Post 6 generated")

# =========================================================================
# 💡 AWARENESS POST 7: CRACK YOUR PHYSICAL TEST (Defense & Police Aspirants)
# =========================================================================
def create_awareness_post_7():
    bg_img = f"{ASSETS}/indian_trainer_coaching.jpg"
    canvas, draw = base_poster(bg_img, overlay_color=(10, 14, 18), opacity=0.86)

    # Top Brand
    draw.text((60, 55), "RSA", font=f_eb(40), fill=(255, 255, 255, 255))
    draw.text((140, 55), "PRO FITNESS", font=f_eb(40), fill=(255, 60, 0, 255))
    draw_pill(draw, W - 380, 60, 320, 46, "🎖️ DEFENSE ASPIRANTS", f_eb(20), (245, 158, 11, 240), (0, 0, 0, 255))

    # Round Sticker: "SPECIAL DISCOUNT"
    draw_sticker(canvas, 130, 220, 75, "STUDENT", "DISCOUNT", bg_color=(234, 88, 12), text_color=(255, 255, 255))

    # Huge Headline
    draw.text((230, 180), "CRACK YOUR", font=f_eb(70), fill=(255, 255, 255, 255))
    draw.text((230, 255), "PHYSICAL TEST.", font=f_eb(74), fill=(245, 158, 11, 255))

    # Center Inset Picture Frame with Trainer Coaching Pullups
    coach_circle = make_circle_crop(f"{ASSETS}/indian_trainer_coaching.jpg", 500, border_color=(245, 158, 11), border_width=10)
    canvas.paste(coach_circle, (W - 540, 360), coach_circle)

    # 3 High-Impact Target Badges
    targets = [
        ("🎯 10+ PULL-UPS", "Dead Hangs & Eccentric Lats Training"),
        ("🎯 HIGH JUMP EXPLOSION", "Weighted Squats & Ankle Conditioning"),
        ("🎯 1600M RUNNING STAMINA", "Cardio Incline & Lung Capacity Drills")
    ]
    yt = 380
    for t_head, t_sub in targets:
        draw_pill(draw, 60, yt, 420, 58, t_head, f_eb(22), (245, 158, 11, 230), (0, 0, 0, 255))
        draw.text((65, yt + 68), t_sub, font=f_b(18), fill=(220, 225, 240, 255))
        yt += 120

    # Target Exams
    draw.text((60, 780), "FOR: BIHAR POLICE SI • CONSTABLE • ARMY AGNIVEER", font=f_eb(26), fill=(255, 255, 255, 255))
    draw.text((60, 820), "Don't let 1 physical mark stop your selection. Train right in Ara.", font=f_r(22), fill=(180, 185, 200, 255))

    # Bottom CTA Box
    draw_pill(draw, 60, 920, W - 120, 85, "CLAIM STUDENT & DEFENSE DISCOUNT AT RSA GYM 🇮🇳", f_eb(25), (255, 60, 0, 245), (255, 255, 255, 255))

    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_07_defense_physical_prep.jpg", "JPEG", quality=92)
    print("Awareness Post 7 generated")

if __name__ == "__main__":
    create_navratri_post_1()
    create_navratri_post_2()
    create_navratri_post_3()
    create_awareness_post_4()
    create_awareness_post_5()
    create_awareness_post_6()
    create_awareness_post_7()
    print("All 7 high-impact poster flyers created!")
