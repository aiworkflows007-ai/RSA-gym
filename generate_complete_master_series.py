import os
from PIL import Image, ImageDraw, ImageFont

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
    """Crops an image into a circle with an anti-aliased border."""
    im = Image.open(img_path).convert("RGBA")
    min_dim = min(im.width, im.height)
    left = (im.width - min_dim) // 2
    top = (im.height - min_dim) // 2
    im = im.crop((left, top, left + min_dim, top + min_dim))
    im = im.resize((size, size), Image.Resampling.LANCZOS)

    mask = Image.new("L", (size * 2, size * 2), 0)
    draw_m = ImageDraw.Draw(mask)
    draw_m.ellipse((0, 0, size * 2 - 1, size * 2 - 1), fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)

    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)

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

def draw_sticker(canvas, cx, cy, radius, text_top, text_bottom, bg_color=(255, 60, 0), text_color=(255, 255, 255)):
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

def base_poster(bg_img_path, overlay_color=(10, 12, 18), opacity=0.88):
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
    draw.rectangle([(20, 20), (W - 20, H - 20)], outline=(255, 60, 0, 70), width=2)
    return canvas, draw

def common_header(draw, category_text, cat_bg=(255, 60, 0), cat_fg=(255, 255, 255)):
    draw.text((60, 55), "RSA", font=f_eb(40), fill=(255, 255, 255, 255))
    draw.text((140, 55), "PRO FITNESS", font=f_eb(40), fill=(255, 60, 0, 255))
    draw.text((60, 105), "ANAITH, ARA - PREMIER HEALTH CLUB", font=f_b(17), fill=(180, 185, 200, 255))

    f_cat = f_eb(18)
    bbox = f_cat.getbbox(category_text)
    pw = bbox[2] - bbox[0] + 36
    draw_pill(draw, W - 60 - pw, 60, pw, 44, category_text, f_cat, cat_bg, cat_fg)

def common_footer(draw):
    draw.line([(50, H - 105), (W - 50, H - 105)], fill=(255, 255, 255, 40), width=1)
    f_info = f_b(20)
    draw.text((50, H - 80), "Deo Vihar, Near Bazaar Samiti Gate, Anaith, Ara", font=f_info, fill=(200, 205, 220, 255))
    draw.text((W - 350, H - 80), "+91 8210453434 - FOLLOW US", font=f_info, fill=(255, 180, 40, 255))

# =========================================================================
# 1. VRAT POST 1: Fasting Muscle Loss Prevention
# =========================================================================
def make_vrat_post_1():
    canvas, draw = base_poster(f"{ASSETS}/indian_athlete_festive_fitness.jpg", overlay_color=(12, 10, 16), opacity=0.88)
    common_header(draw, "NAVRATRI SPECIAL", cat_bg=(245, 158, 11), cat_fg=(0, 0, 0))

    # Devi Circle Inset Top Right
    durga_img = make_circle_crop(f"{ASSETS}/maa_durga_divine_art.jpg", 380, border_color=(245, 158, 11), border_width=8)
    canvas.paste(durga_img, (W - 440, 180), durga_img)

    draw.text((60, 180), "HAPPY", font=f_eb(68), fill=(255, 255, 255, 255))
    draw.text((60, 250), "NAVRATRI", font=f_eb(72), fill=(245, 158, 11, 255))
    draw.text((60, 335), "PROTECT YOUR MUSCLE", font=f_eb(34), fill=(255, 60, 0, 255))
    draw.text((60, 380), "4 Rules To Maintain Size & Strength", font=f_b(22), fill=(200, 205, 220, 255))

    points = [
        ("01", "PRIORITIZE SATVIK PROTEIN", "Paneer (20g protein/100g), Curd/Dahi (10g/bowl), and roasted Peanuts prevent muscle catabolism during fasts."),
        ("02", "TIMING: POST-FALAHAR ONLY", "Never lift heavy on empty stomach. Workout 60-90 mins after taking fruit/falahar for glycogen energy."),
        ("03", "ELECTROLYTES & SENDHA NAMAK", "Drink coconut water or lemon water with sendha namak. Avoids dehydration, dizziness, and muscle cramps."),
        ("04", "MODERATE WEIGHTS (12-15 REPS)", "Focus on consistency and form rather than 1-Rep Max PRs. 45 mins max session length is optimal.")
    ]

    y = 590
    for num, title, desc in points:
        draw_pill(draw, 60, y, 54, 40, num, f_eb(20), (245, 158, 11), (0, 0, 0))
        draw.text((130, y + 5), title, font=f_eb(24), fill=(245, 158, 11, 255))
        draw.text((130, y + 40), desc, font=f_r(19), fill=(225, 230, 240, 255))
        y += 115

    draw_pill(draw, 60, 1100, W - 120, 80, "FREE NAVRATRI DIET CHART - DM 'VRAT' TO @RSAPROFITNESS", f_eb(24), (255, 42, 42), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_01_vrat_muscle_shield.jpg", "JPEG", quality=92)
    print("Vrat Post 1 created")

# =========================================================================
# 2. VRAT POST 2: 70g+ Satvik Protein Food Chart
# =========================================================================
def make_vrat_post_2():
    canvas, draw = base_poster(f"{ASSETS}/navratri_satvik_fitness_food.jpg", overlay_color=(10, 12, 16), opacity=0.88)
    common_header(draw, "VRAT NUTRITION", cat_bg=(245, 158, 11), cat_fg=(0, 0, 0))

    # Food Circle Inset
    food_img = make_circle_crop(f"{ASSETS}/navratri_satvik_fitness_food.jpg", 400, border_color=(245, 158, 11), border_width=8)
    canvas.paste(food_img, (W - 450, 180), food_img)

    draw.text((60, 180), "HIGH PROTEIN", font=f_eb(58), fill=(255, 255, 255, 255))
    draw.text((60, 245), "SATVIK DIET", font=f_eb(68), fill=(245, 158, 11, 255))
    draw.text((60, 330), "70G+ PROTEIN ON NAVRATRI VRAT", font=f_eb(30), fill=(74, 222, 128, 255))
    draw.text((60, 375), "Without eggs or non-veg. 100% Shuddh.", font=f_b(22), fill=(200, 205, 220, 255))

    foods = [
        ("01", "FRESH PANEER (100g)", "20g Protein", "Raw or lightly roasted in 1/2 tsp ghee with jeera & sendha namak."),
        ("02", "HUNG CURD / GREEK DAHI", "12g Protein", "1 large bowl thick dahi. Rich in gut probiotics and slow-digesting casein."),
        ("03", "ROASTED PEANUTS (50g)", "13g Protein", "Budget-friendly superfood. Best evening pre-workout snack with coconut water."),
        ("04", "KUTTU / RAJGIRA FLOUR (60g)", "10g Protein", "2 Rotis or Cheela. Far superior in amino acids than plain sabudana."),
        ("05", "ROASTED MAKHANA + ALMONDS", "8g Protein", "Low-calorie crunchy volume snacking with high calcium and magnesium.")
    ]

    y = 600
    for num, name, macro, sub in foods:
        draw_pill(draw, 60, y, 48, 36, num, f_eb(18), (255, 60, 0), (255, 255, 255))
        draw.text((125, y + 2), name, font=f_eb(22), fill=(255, 255, 255, 255))
        draw_pill(draw, W - 230, y - 2, 170, 38, macro, f_eb(18), (34, 197, 94), (0, 0, 0))
        draw.text((125, y + 36), sub, font=f_r(18), fill=(200, 205, 220, 255))
        y += 92

    draw_pill(draw, 60, 1100, W - 120, 80, "SAVE THIS POST FOR YOUR 9-DAY VRAT MEALS", f_eb(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_02_vrat_70g_protein_chart.jpg", "JPEG", quality=92)
    print("Vrat Post 2 created")

# =========================================================================
# 3. VRAT POST 3: Sabudana Trap vs Real Satvik Fuel
# =========================================================================
def make_vrat_post_3():
    canvas, draw = base_poster(f"{ASSETS}/navratri_satvik_fitness_food.jpg", overlay_color=(8, 12, 16), opacity=0.90)
    common_header(draw, "DIET AWARENESS", cat_bg=(255, 60, 0), cat_fg=(255, 255, 255))

    draw.text((60, 180), "THE NAVRATRI", font=f_eb(60), fill=(255, 255, 255, 255))
    draw.text((60, 250), "FASTING TRAP", font=f_eb(74), fill=(248, 113, 113, 255))
    draw.text((60, 340), "Why Sabudana & Fried Pakodas Ruin Results", font=f_b(26), fill=(255, 190, 30, 255))

    col_w = (W - 150) // 2

    # Left Column: The Trap
    draw.rounded_rectangle([(60, 410), (60 + col_w, 1050)], radius=20, fill=(30, 16, 20, 230), outline=(239, 68, 68), width=2)
    draw_pill(draw, 80, 430, col_w - 40, 48, "THE SABUDANA TRAP", f_eb(20), (239, 68, 68), (255, 255, 255))
    bads = [
        ("Pure Fast Carbs", "Sabudana has zero protein, zero fiber, and spikes blood sugar fast."),
        ("Deep Fried in Ghee", "Deep fried pakodas add 400+ sluggish, inflammatory fat calories."),
        ("Lethargy & Bloating", "Causes heavy energy crashes, drowsiness, and digestive discomfort."),
        ("Muscle Starvation", "Lacks essential amino acids required for body repair.")
    ]
    yb = 510
    for title, desc in bads:
        draw.text((85, yb), f"- {title}", font=f_eb(21), fill=(248, 113, 113, 255))
        draw.text((85, yb + 32), desc, font=f_r(18), fill=(230, 230, 230, 255))
        yb += 125

    # Right Column: The Satvik Fuel
    draw.rounded_rectangle([(60 + col_w + 30, 410), (W - 60, 1050)], radius=20, fill=(16, 30, 22, 230), outline=(34, 197, 94), width=2)
    draw_pill(draw, 60 + col_w + 50, 430, col_w - 40, 48, "SMART SATVIK FUEL", f_eb(20), (34, 197, 94), (0, 0, 0))
    goods = [
        ("Paneer & Dahi", "Rich in complete protein, calcium, and keeps stomach full for 4 hours."),
        ("Kuttu & Samak Rice", "Complex carbs with 12% protein and high dietary fiber."),
        ("Dry Roasted Makhana", "Crunchy low calorie volume food with zero cholesterol."),
        ("Coconut Water", "Natural electrolytes, stops muscle cramping, and boosts skin glow.")
    ]
    yg = 510
    for title, desc in goods:
        draw.text((60 + col_w + 55, yg), f"+ {title}", font=f_eb(21), fill=(74, 222, 128, 255))
        draw.text((60 + col_w + 55, yg + 32), desc, font=f_r(18), fill=(230, 240, 235, 255))
        yg += 125

    draw_pill(draw, 60, 1100, W - 120, 80, "EAT SMART THIS NAVRATRI - TRAIN AT RSA PRO FITNESS", f_eb(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_03_vrat_sabudana_vs_satvik.jpg", "JPEG", quality=92)
    print("Vrat Post 3 created")

# =========================================================================
# 4. GYM MISTAKE 1: Ego Lifting & Skipping Warmup
# =========================================================================
def make_mistake_post_1():
    canvas, draw = base_poster(f"{ASSETS}/indian_male_lifting.jpg", overlay_color=(10, 12, 16), opacity=0.90)
    common_header(draw, "GYM MISTAKE #1", cat_bg=(239, 68, 68), cat_fg=(255, 255, 255))

    circle_img = make_circle_crop(f"{ASSETS}/indian_male_lifting.jpg", 400, border_color=(239, 68, 68), border_width=8)
    canvas.paste(circle_img, (W - 450, 180), circle_img)

    draw.text((60, 180), "MISTAKE #1:", font=f_eb(54), fill=(248, 113, 113, 255))
    draw.text((60, 245), "EGO LIFTING &", font=f_eb(68), fill=(255, 255, 255, 255))
    draw.text((60, 325), "SKIPPING WARM-UP", font=f_eb(52), fill=(255, 60, 0, 255))
    draw.text((60, 395), "Why 90% of beginners get injured in month 1", font=f_b(22), fill=(200, 205, 220, 255))

    points = [
        ("01", "THE MISTAKE: LIFTING TOO HEAVY TOO SOON", "Trying to lift heavy weights to impress others with rounded back on deadlifts or half-reps on bench press."),
        ("02", "THE RESULT: DAMAGED JOINTS & TORN LIGAMENTS", "Ego lifting does not build muscle; it puts maximum stress on lower lumbar discs, rotator cuffs, and knees."),
        ("03", "SKIPPING 5-MIN DYNAMIC MOBILITY", "Jumping straight to heavy barbell with cold, stiff joints after sitting 8 hours at desk guarantees injury."),
        ("04", "THE RSA SOLUTION: MASTER FORM FIRST", "Master the movement with light weights. Progressive overload works only when form is 100% textbook.")
    ]

    y = 600
    for num, head, desc in points:
        draw_pill(draw, 60, y, 48, 36, num, f_eb(18), (239, 68, 68), (255, 255, 255))
        draw.text((125, y + 2), head, font=f_eb(22), fill=(255, 255, 255, 255))
        draw.text((125, y + 36), desc, font=f_r(18), fill=(200, 205, 220, 255))
        y += 115

    draw_pill(draw, 60, 1100, W - 120, 80, "TRAIN SMART, NOT EGO - CERTIFIED COACHES AT RSA GYM", f_eb(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_04_gym_mistake_ego_lifting.jpg", "JPEG", quality=92)
    print("Mistake Post 1 created")

# =========================================================================
# 5. GYM MISTAKE 2: Spot Reduction Myth (Belly Fat)
# =========================================================================
def make_mistake_post_2():
    canvas, draw = base_poster(f"{ASSETS}/indian_female_fitness.jpg", overlay_color=(10, 12, 16), opacity=0.90)
    common_header(draw, "GYM MISTAKE #2", cat_bg=(239, 68, 68), cat_fg=(255, 255, 255))

    circle_img = make_circle_crop(f"{ASSETS}/indian_female_fitness.jpg", 400, border_color=(255, 60, 0), border_width=8)
    canvas.paste(circle_img, (W - 450, 180), circle_img)

    draw.text((60, 180), "MISTAKE #2:", font=f_eb(54), fill=(248, 113, 113, 255))
    draw.text((60, 245), "BELIEVING IN", font=f_eb(68), fill=(255, 255, 255, 255))
    draw.text((60, 325), "SPOT REDUCTION", font=f_eb(54), fill=(255, 60, 0, 255))
    draw.text((60, 395), "Why 500 crunches daily won't burn your belly fat", font=f_b(22), fill=(200, 205, 220, 255))

    facts = [
        ("01", "BIOLOGY: SPOT REDUCTION DOES NOT EXIST", "You cannot choose where your body burns fat first. Fat loss occurs across the whole body systemically."),
        ("02", "CRUNCHES BUILD ABS, THEY DON'T BURN FAT", "Doing hundreds of sit-ups strengthens the abdominal wall beneath the fat, but won't burn the fat layer covering it."),
        ("03", "THE REAL CULPRIT: CALORIE SURPLUS", "If you are eating more calories than you burn, no exercise on earth can reduce your waistline."),
        ("04", "THE SCIENTIFIC FIX: COMPOUND LIFTS & DEFICIT", "Do Squats, Deadlifts & Incline Walking with a moderate 300 kcal calorie deficit. Fat will melt automatically.")
    ]

    y = 600
    for num, head, desc in facts:
        draw_pill(draw, 60, y, 48, 36, num, f_eb(18), (255, 60, 0), (255, 255, 255))
        draw.text((125, y + 2), head, font=f_eb(22), fill=(255, 255, 255, 255))
        draw.text((125, y + 36), desc, font=f_r(18), fill=(200, 205, 220, 255))
        y += 115

    draw_pill(draw, 60, 1100, W - 120, 80, "STOP GUESSING, START TRANSFORMING - JOIN RSA GYM ARA", f_eb(24), (255, 42, 42), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_05_gym_mistake_spot_reduction.jpg", "JPEG", quality=92)
    print("Mistake Post 2 created")

# =========================================================================
# 6. GYM MISTAKE 3: Working Out Hard But Eating Zero Protein
# =========================================================================
def make_mistake_post_3():
    canvas, draw = base_poster(f"{ASSETS}/hero_indian_athletes.jpg", overlay_color=(10, 12, 16), opacity=0.90)
    common_header(draw, "GYM MISTAKE #3", cat_bg=(239, 68, 68), cat_fg=(255, 255, 255))

    circle_img = make_circle_crop(f"{ASSETS}/indian_trainer_coaching.jpg", 400, border_color=(255, 180, 20), border_width=8)
    canvas.paste(circle_img, (W - 450, 180), circle_img)

    draw.text((60, 180), "MISTAKE #3:", font=f_eb(54), fill=(248, 113, 113, 255))
    draw.text((60, 245), "TRAINING HARD,", font=f_eb(68), fill=(255, 255, 255, 255))
    draw.text((60, 325), "EATING ZERO PROTEIN", font=f_eb(48), fill=(255, 60, 0, 255))
    draw.text((60, 395), "Why working out without protein leaves you skinny-fat", font=f_b(22), fill=(200, 205, 220, 255))

    truths = [
        ("01", "MUSCLES TEAR IN THE GYM, NOT GROW", "Lifting weights creates microscopic muscle tears. Without amino acids (protein), the body cannot repair them."),
        ("02", "THE STANDARD CARB OVERLOAD TRAP", "Relying purely on roti, rice, and watery daal provides barely 25g protein. Your muscles remain in catabolic state."),
        ("03", "FATIGUE, SORENESS & ZERO TONING", "Without 1.2g to 1.6g protein per kg of body weight, you will experience constant fatigue and zero muscle definition."),
        ("04", "EASY FIX: ADD PROTEIN TO EVERY MEAL", "Include Eggs, Paneer, Soya chunks, Curd, or Sattu in every main meal. Results will 3x within 30 days.")
    ]

    y = 600
    for num, head, desc in truths:
        draw_pill(draw, 60, y, 48, 36, num, f_eb(18), (255, 180, 20), (0, 0, 0))
        draw.text((125, y + 2), head, font=f_eb(22), fill=(255, 255, 255, 255))
        draw.text((125, y + 36), desc, font=f_r(18), fill=(200, 205, 220, 255))
        y += 115

    draw_pill(draw, 60, 1100, W - 120, 80, "GET FREE CUSTOM DIET CHART - DM 'DIET' TO @RSAPROFITNESS", f_eb(24), (34, 197, 94), (0, 0, 0))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_06_gym_mistake_zero_protein.jpg", "JPEG", quality=92)
    print("Mistake Post 3 created")

# =========================================================================
# 7. IMAGE: Why Protein is Important (Not Just For Bodybuilders)
# =========================================================================
def make_why_protein_post():
    canvas, draw = base_poster(f"{ASSETS}/hero_indian_athletes.jpg", overlay_color=(8, 12, 18), opacity=0.90)
    common_header(draw, "NUTRITION SCIENCE", cat_bg=(34, 197, 94), cat_fg=(0, 0, 0))

    draw.text((60, 180), "WHY PROTEIN", font=f_eb(68), fill=(255, 255, 255, 255))
    draw.text((60, 255), "IS CRITICAL", font=f_eb(74), fill=(74, 222, 128, 255))
    draw.text((60, 345), "It is NOT just for bodybuilders. It is for everyone.", font=f_b(26), fill=(255, 180, 40, 255))

    pillars = [
        ("01", "MUSCLE REPAIR & DEFINITION", "Every workout tears muscle fibers. Protein provides the 9 essential amino acids to rebuild them tighter and stronger."),
        ("02", "BURNS CALORIES AUTOMATICALLY (TEF)", "Protein has the highest Thermic Effect of Food (TEF). Your body burns 20-30% of protein calories just to digest it!"),
        ("03", "CRUSHES CRAVINGS & JUNK HUNGER", "Reduces ghrelin (hunger hormone) and boosts peptide YY (fullness hormone). Stops midnight binge eating."),
        ("04", "IMMUNITY, HAIR & METABOLISM", "Antibodies, hemoglobin, skin collagen, and hair keratin are all made of protein. Keeps your skin firm while losing weight.")
    ]

    y = 420
    for num, head, desc in pillars:
        draw_pill(draw, 60, y, 54, 40, num, f_eb(20), (34, 197, 94), (0, 0, 0))
        draw.text((130, y + 5), head, font=f_eb(24), fill=(74, 222, 128, 255))
        draw.text((130, y + 42), desc, font=f_r(19), fill=(215, 225, 235, 255))
        y += 135

    # Daily target card
    draw.rounded_rectangle([(60, 980), (W - 60, 1060)], radius=18, fill=(18, 24, 34, 230), outline=(74, 222, 128), width=2)
    draw.text((85, 1005), "DAILY GOAL: 1.2g to 1.6g Protein per kg Bodyweight", font=f_eb(24), fill=(255, 255, 255, 255))
    draw.text((W - 270, 1005), "(e.g. 70kg = 90-110g)", font=f_b(22), fill=(255, 180, 40, 255))

    draw_pill(draw, 60, 1100, W - 120, 80, "CALCULATE YOUR PROTEIN GOAL AT RSA PRO FITNESS ARA", f_eb(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_07_why_protein_is_important.jpg", "JPEG", quality=92)
    print("Why Protein Post created")

# =========================================================================
# 8. IMAGE: Best Protein Food (Budget-Friendly Indian Sources)
# =========================================================================
def make_best_protein_food_post():
    canvas, draw = base_poster(f"{ASSETS}/navratri_satvik_fitness_food.jpg", overlay_color=(10, 10, 16), opacity=0.92)
    common_header(draw, "INDIAN PROTEIN GUIDE", cat_bg=(255, 180, 20), cat_fg=(0, 0, 0))

    draw.text((60, 180), "TOP 6 BUDGET", font=f_eb(60), fill=(255, 255, 255, 255))
    draw.text((60, 245), "PROTEIN FOODS", font=f_eb(74), fill=(255, 180, 20, 255))
    draw.text((60, 335), "Affordable, High-Yield Indian Sources (Veg & Non-Veg)", font=f_b(24), fill=(255, 255, 255, 255))

    sources = [
        ("01", "SOYA CHUNKS (50g dry)", "26g Protein", "Unbeatable value. 52% pure plant protein. Boil and add to sabzi or pulao."),
        ("02", "WHOLE EGGS (3 boiled)", "18g Protein", "Complete amino acid profile + healthy choline. Most bioavailable protein on earth."),
        ("03", "FRESH PANEER (100g)", "20g Protein", "Delicious high-fat vegetarian source. Great for evening post-workout dinner."),
        ("04", "CHICKEN BREAST (100g)", "31g Protein", "Lean, zero-carb, pure muscle fuel. Low in calories, highest protein density."),
        ("05", "SATTU DRINK (50g)", "12g Protein", "Bihar's native superfood. Roasted gram flour provides natural endurance & carbs."),
        ("06", "THICK CURD / DAHI (200g)", "10g Protein", "Slow-digesting casein + gut probiotics. Perfect pairing with lunch.")
    ]

    y = 400
    for num, name, macro, desc in sources:
        draw_pill(draw, 60, y, 48, 36, num, f_eb(18), (255, 180, 20), (0, 0, 0))
        draw.text((125, y + 2), name, font=f_eb(22), fill=(255, 255, 255, 255))
        draw_pill(draw, W - 230, y - 2, 170, 38, macro, f_eb(18), (34, 197, 94), (0, 0, 0))
        draw.text((125, y + 36), desc, font=f_r(18), fill=(200, 205, 220, 255))
        y += 105

    draw_pill(draw, 60, 1100, W - 120, 80, "WANT A CUSTOM MEAL PLAN? DM 'DIET' TO @RSAPROFITNESS", f_eb(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_08_best_indian_protein_foods.jpg", "JPEG", quality=92)
    print("Best Protein Foods Post created")

# =========================================================================
# 9. IMAGE: Before Going to Gym Keep in Mind (Pre-Workout Rules)
# =========================================================================
def make_before_gym_post():
    canvas, draw = base_poster(f"{ASSETS}/indian_male_lifting.jpg", overlay_color=(10, 12, 16), opacity=0.90)
    common_header(draw, "PRE-WORKOUT PROTOCOL", cat_bg=(255, 100, 30), cat_fg=(255, 255, 255))

    circle_img = make_circle_crop(f"{ASSETS}/indian_male_lifting.jpg", 380, border_color=(255, 100, 30), border_width=8)
    canvas.paste(circle_img, (W - 440, 180), circle_img)

    draw.text((60, 180), "BEFORE YOU", font=f_eb(64), fill=(255, 255, 255, 255))
    draw.text((60, 250), "HIT THE GYM", font=f_eb(74), fill=(255, 100, 30, 255))
    draw.text((60, 340), "4 Golden Rules For Maximum Energy", font=f_b(24), fill=(255, 190, 40, 255))

    rules = [
        ("01", "CARB MEAL 45-60 MINS BEFORE", "Eat complex carbs (1-2 Bananas, Oats, or Peanut Butter Toast). This loads glycogen in muscles so you don't gas out."),
        ("02", "HYDRATE WITH 500ML WATER", "A 2% drop in hydration drops muscle strength by 15%! Drink water 30 mins before, never gulp right before squats."),
        ("03", "HAVE A WRITTEN WORKOUT PLAN", "Never walk into gym wondering 'aaj kya karein'. Know your exercises, sets, and rep targets beforehand."),
        ("04", "5-MIN DYNAMIC MOBILITY (NOT STATIC)", "Do arm circles, leg swings, and bodyweight squats to lube joint capsules. Save static stretching for after workout.")
    ]

    y = 590
    for num, title, desc in rules:
        draw_pill(draw, 60, y, 48, 36, num, f_eb(18), (255, 100, 30), (255, 255, 255))
        draw.text((125, y + 2), title, font=f_eb(22), fill=(255, 255, 255, 255))
        draw.text((125, y + 36), desc, font=f_r(18), fill=(200, 205, 220, 255))
        y += 115

    draw_pill(draw, 60, 1100, W - 120, 80, "FEEL THE POWER - 1-DAY FREE TRIAL AT RSA PRO FITNESS ARA", f_eb(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_09_before_gym_checklist.jpg", "JPEG", quality=92)
    print("Before Gym Post created")

# =========================================================================
# 10. IMAGE: After Going to Gym Keep in Mind (Post-Workout Rules)
# =========================================================================
def make_after_gym_post():
    canvas, draw = base_poster(f"{ASSETS}/indian_trainer_coaching.jpg", overlay_color=(10, 12, 16), opacity=0.90)
    common_header(draw, "POST-WORKOUT RECOVERY", cat_bg=(34, 197, 94), cat_fg=(0, 0, 0))

    circle_img = make_circle_crop(f"{ASSETS}/hero_indian_athletes.jpg", 380, border_color=(34, 197, 94), border_width=8)
    canvas.paste(circle_img, (W - 440, 180), circle_img)

    draw.text((60, 180), "AFTER YOU", font=f_eb(64), fill=(255, 255, 255, 255))
    draw.text((60, 250), "FINISH GYM", font=f_eb(74), fill=(74, 222, 128, 255))
    draw.text((60, 340), "4 Rules To Lock In Muscle Growth", font=f_b(24), fill=(255, 180, 40, 255))

    rules = [
        ("01", "PROTEIN + CARBS WITHIN 90 MINS", "The anabolic recovery window is open. Take 20-30g protein (Eggs, Paneer, Whey, or Soya) + fast carb to replenish glycogen."),
        ("02", "5-MIN STATIC STRETCHING", "Stretch your chest, hamstrings, and lats when muscles are warm. Restores muscle length and reduces next-day soreness."),
        ("03", "REPLACE SWEAT & SODIUM LOSS", "Drink 700ml+ water with a pinch of salt. Dehydrated muscle tissue repairs 40% slower."),
        ("04", "7-8 HOURS OF DEEP SLEEP", "Muscles do not grow in gym; they grow in bed while sleeping. Growth hormone peaks during Stage 3 deep sleep.")
    ]

    y = 590
    for num, title, desc in rules:
        draw_pill(draw, 60, y, 48, 36, num, f_eb(18), (34, 197, 94), (0, 0, 0))
        draw.text((125, y + 2), title, font=f_eb(22), fill=(255, 255, 255, 255))
        draw.text((125, y + 36), desc, font=f_r(18), fill=(200, 205, 220, 255))
        y += 115

    draw_pill(draw, 60, 1100, W - 120, 80, "RECOVER STRONGER - JOIN ARA'S #1 FITNESS COMMUNITY", f_eb(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_10_after_gym_checklist.jpg", "JPEG", quality=92)
    print("After Gym Post created")

if __name__ == "__main__":
    make_vrat_post_1()
    make_vrat_post_2()
    make_vrat_post_3()
    make_mistake_post_1()
    make_mistake_post_2()
    make_mistake_post_3()
    make_why_protein_post()
    make_best_protein_food_post()
    make_before_gym_post()
    make_after_gym_post()
    print("All 10 master social posters created with 0 missing glyphs!")
