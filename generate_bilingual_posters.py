import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
ASSETS = "/home/ashok/RSA Gym/assets"
OUT = "/home/ashok/RSA Gym/social_posts"
os.makedirs(OUT, exist_ok=True)

# Unified Bilingual Fonts (Mukta - Google Font supporting both English Latin + Hindi Devanagari)
FONT_EB = f"{ASSETS}/Mukta-ExtraBold.ttf"
FONT_B  = f"{ASSETS}/Mukta-Bold.ttf"
FONT_SB = f"{ASSETS}/Mukta-SemiBold.ttf"
FONT_M  = f"{ASSETS}/Mukta-Medium.ttf"
FONT_R  = f"{ASSETS}/Mukta-Regular.ttf"

def fe_eb(size): return ImageFont.truetype(FONT_EB, size)
def fe_b(size): return ImageFont.truetype(FONT_B, size)
def fe_r(size): return ImageFont.truetype(FONT_R, size)

def fh_b(size): return ImageFont.truetype(FONT_B, size)
def fh_m(size): return ImageFont.truetype(FONT_M, size)

def make_circle_crop(img_path, size, border_color=(255, 60, 0), border_width=10):
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

def common_header(draw, en_category, hi_category, cat_bg=(255, 60, 0), cat_fg=(255, 255, 255)):
    # Logo
    draw.text((60, 50), "RSA", font=fe_eb(38), fill=(255, 255, 255, 255))
    draw.text((135, 50), "PRO FITNESS", font=fe_eb(38), fill=(255, 60, 0, 255))
    draw.text((60, 98), "ANAITH, ARA - PREMIER HEALTH CLUB", font=fe_b(16), fill=(180, 185, 200, 255))

    # Bilingual Badge
    badge_txt = f"{en_category} | {hi_category}"
    f_cat = fh_b(17)
    bbox = f_cat.getbbox(badge_txt)
    pw = bbox[2] - bbox[0] + 36
    draw_pill(draw, W - 60 - pw, 55, pw, 44, badge_txt, f_cat, cat_bg, cat_fg)

def common_footer(draw):
    draw.line([(50, H - 105), (W - 50, H - 105)], fill=(255, 255, 255, 40), width=1)
    draw.text((50, H - 80), "Deo Vihar, Near Bazaar Samiti Gate, Anaith, Ara", font=fe_b(19), fill=(200, 205, 220, 255))
    draw.text((W - 350, H - 80), "+91 8210453434 - FOLLOW US", font=fe_b(19), fill=(255, 180, 40, 255))

# =========================================================================
# 1. VRAT POST 1: Fasting Muscle Loss (Bilingual)
# =========================================================================
def make_vrat_post_1():
    canvas, draw = base_poster(f"{ASSETS}/indian_athlete_festive_fitness.jpg", overlay_color=(12, 10, 16), opacity=0.88)
    common_header(draw, "NAVRATRI SPECIAL", "नवरात्रि स्पेशल", cat_bg=(245, 158, 11), cat_fg=(0, 0, 0))

    # Devi Circle Inset Top Right
    durga_img = make_circle_crop(f"{ASSETS}/maa_durga_divine_art.jpg", 370, border_color=(245, 158, 11), border_width=8)
    canvas.paste(durga_img, (W - 430, 170), durga_img)

    # Headline
    draw.text((60, 165), "HAPPY NAVRATRI", font=fe_eb(56), fill=(255, 255, 255, 255))
    draw.text((60, 230), "शुभ नवरात्रि - शक्ति और फिटनेस", font=fh_b(36), fill=(245, 158, 11, 255))
    draw.text((60, 290), "PROTECT YOUR MUSCLE DURING FAST", font=fe_eb(28), fill=(255, 60, 0, 255))
    draw.text((60, 335), "व्रत में मसल लॉस रोकने के 4 जरूरी नियम", font=fh_b(24), fill=(210, 215, 230, 255))

    points = [
        ("01", "SATVIK PROTEIN FIRST (सात्विक प्रोटीन)", "Paneer (20g/100g), Curd/Dahi (12g), and roasted Peanuts prevent muscle loss.\nपनीर, गाढ़ा दही और भुनी मूंगफली फलाहार में रोज शामिल करें।"),
        ("02", "POST-FALAHAR WORKOUT (वर्कआउट का सही समय)", "Never lift heavy on empty stomach. Workout 60-90m after eating fruits/falahar.\nखाली पेट भारी कसरत न करें। फलाहार के 1-1.5 घंटे बाद ही वर्कआउट करें।"),
        ("03", "HYDRATION & SENDHA NAMAK (सेंधा नमक पानी)", "Drink coconut water or lemon water with sendha namak to stop dizziness.\nनारियल पानी या नींबू-सेंधा नमक पानी पिएं ताकि कमजोरी और चक्कर न आएं।"),
        ("04", "MODERATE WEIGHTS 12-15 REPS (हल्का वजन)", "Focus on consistency. Avoid heavy 1-Rep Max PRs. 45 mins session is optimal.\nव्रत में बहुत भारी वजन न उठाएं। 12-15 रैप्स और 45 मिनट वर्कआउट काफी है।")
    ]

    y = 575
    for num, title, desc in points:
        draw_pill(draw, 60, y, 48, 36, num, fe_eb(18), (245, 158, 11), (0, 0, 0))
        draw.text((125, y + 2), title, font=fh_b(22), fill=(245, 158, 11, 255))
        d_lines = desc.split("\n")
        draw.text((125, y + 34), d_lines[0], font=fe_r(17), fill=(230, 235, 245, 255))
        draw.text((125, y + 58), d_lines[1], font=fh_m(17), fill=(190, 220, 240, 255))
        y += 125

    draw_pill(draw, 60, 1100, W - 120, 80, "FREE NAVRATRI DIET CHART - फ्री डाइट चार्ट के लिए DM करें", fh_b(24), (255, 42, 42), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_01_vrat_muscle_shield.jpg", "JPEG", quality=92)
    print("Post 1 (Bilingual) created")

# =========================================================================
# 2. VRAT POST 2: 70g+ Satvik Protein Chart (Bilingual)
# =========================================================================
def make_vrat_post_2():
    canvas, draw = base_poster(f"{ASSETS}/navratri_satvik_fitness_food.jpg", overlay_color=(10, 12, 16), opacity=0.88)
    common_header(draw, "VRAT NUTRITION", "व्रत डाइट", cat_bg=(245, 158, 11), cat_fg=(0, 0, 0))

    food_img = make_circle_crop(f"{ASSETS}/navratri_satvik_fitness_food.jpg", 390, border_color=(245, 158, 11), border_width=8)
    canvas.paste(food_img, (W - 440, 170), food_img)

    draw.text((60, 165), "HIGH PROTEIN", font=fe_eb(56), fill=(255, 255, 255, 255))
    draw.text((60, 225), "सात्विक डाइट चार्ट", font=fh_b(42), fill=(245, 158, 11, 255))
    draw.text((60, 290), "70G+ PROTEIN ON NAVRATRI VRAT", font=fe_eb(28), fill=(74, 222, 128, 255))
    draw.text((60, 335), "बिना अंडे या नॉन-वेज 70 ग्राम से ज्यादा शुद्ध प्रोटीन", font=fh_b(22), fill=(210, 215, 230, 255))

    foods = [
        ("01", "FRESH PANEER (100g) / ताजा पनीर", "20g Protein", "Raw or ghee-tossed with jeera & sendha namak. (कच्चा या 1/2 चम्मच घी में रोस्ट)"),
        ("02", "HUNG CURD (200g) / गाढ़ा ताजा दही", "12g Protein", "Rich in gut probiotics and slow-digesting casein. (पाचन के लिए बेस्ट प्रोबायोटिक)"),
        ("03", "ROASTED PEANUTS (50g) / भुनी मूंगफली", "13g Protein", "Budget superfood + healthy fats. (सस्ता और सबसे असरदार देसी सुपरफूड)"),
        ("04", "KUTTU / RAJGIRA ROTI (60g)", "10g Protein", "2 Rotis or Cheela. Far superior to sabudana. (कुट्टू या राजगिरा की 2 रोटी या चीला)"),
        ("05", "ROASTED MAKHANA & NUTS (मखाना-बादाम)", "8g Protein", "Crunchy volume snack with high calcium. (कैल्शियम और मैग्नीशियम से भरपूर)")
    ]

    y = 590
    for num, name, macro, sub in foods:
        draw_pill(draw, 60, y, 48, 36, num, fe_eb(18), (255, 60, 0), (255, 255, 255))
        draw.text((125, y + 2), name, font=fh_b(21), fill=(255, 255, 255, 255))
        draw_pill(draw, W - 230, y - 2, 170, 38, macro, fe_eb(18), (34, 197, 94), (0, 0, 0))
        draw.text((125, y + 36), sub, font=fh_m(16), fill=(200, 215, 230, 255))
        y += 98

    draw_pill(draw, 60, 1100, W - 120, 80, "SAVE THIS POST FOR YOUR VRAT MEALS - यह पोस्ट सेव करें", fh_b(23), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_02_vrat_70g_protein_chart.jpg", "JPEG", quality=92)
    print("Post 2 (Bilingual) created")

# =========================================================================
# 3. VRAT POST 3: Sabudana vs Satvik (Bilingual)
# =========================================================================
def make_vrat_post_3():
    canvas, draw = base_poster(f"{ASSETS}/navratri_satvik_fitness_food.jpg", overlay_color=(8, 12, 16), opacity=0.90)
    common_header(draw, "DIET AWARENESS", "डाइट अवेयरनेस", cat_bg=(255, 60, 0), cat_fg=(255, 255, 255))

    draw.text((60, 165), "THE NAVRATRI FASTING TRAP", font=fe_eb(52), fill=(255, 255, 255, 255))
    draw.text((60, 225), "साबूदाना पकौड़ा या सही सात्विक डाइट?", font=fh_b(38), fill=(248, 113, 113, 255))
    draw.text((60, 290), "Why Deep-Fried Fast Food Ruines Your Fitness Results", font=fe_b(24), fill=(255, 190, 30, 255))

    col_w = (W - 150) // 2

    # Left: Sabudana Trap
    draw.rounded_rectangle([(60, 370), (60 + col_w, 1050)], radius=20, fill=(30, 16, 20, 235), outline=(239, 68, 68), width=2)
    draw_pill(draw, 80, 390, col_w - 40, 48, "SABUDANA TRAP (गलत तरीका)", fh_b(18), (239, 68, 68), (255, 255, 255))
    bads = [
        ("0% Protein (शून्य प्रोटीन)", "Sabudana has zero protein, only starch.\nसाबूदाना में प्रोटीन 0 होता है, सिर्फ स्टार्च है।"),
        ("Deep Fried (तले हुए पकौड़े)", "Adds 400+ sluggish inflammatory calories.\nघी-तेल में तलने से 400+ अनहेल्दी कैलोरी मिलती है।"),
        ("Lethargy & Sugar Crash (सुस्ती)", "Causes heavy insulin spike and sleepiness.\nब्लड शुगर तेजी से बढ़ता है और भारी थकान आती है।"),
        ("Muscle Starvation (मसल कमजोरी)", "Zero amino acids to repair your muscles.\nमांसपेशियों की रिकवरी के लिए कोई पोषण नहीं मिलता।")
    ]
    yb = 465
    for title, desc in bads:
        draw.text((85, yb), f"- {title}", font=fh_b(19), fill=(248, 113, 113, 255))
        d_l = desc.split("\n")
        draw.text((85, yb + 28), d_l[0], font=fe_r(16), fill=(230, 230, 230, 255))
        draw.text((85, yb + 50), d_l[1], font=fh_m(15), fill=(200, 200, 200, 255))
        yb += 140

    # Right: Satvik Fuel
    draw.rounded_rectangle([(60 + col_w + 30, 370), (W - 60, 1050)], radius=20, fill=(16, 30, 22, 235), outline=(34, 197, 94), width=2)
    draw_pill(draw, 60 + col_w + 50, 390, col_w - 40, 48, "SATVIK FUEL (सही तरीका)", fh_b(18), (34, 197, 94), (0, 0, 0))
    goods = [
        ("Paneer & Dahi (पनीर-दही)", "Complete protein, stays in stomach 4 hours.\nपूरा प्रोटीन मिलता है, 4 घंटे तक भूख नहीं लगती।"),
        ("Samak & Kuttu (कुट्टू रोटी)", "Complex carbs with 12% natural protein.\nनेचुरल फाइबर और कॉम्प्लेक्स कार्ब्स जो एनर्जी दें।"),
        ("Roasted Makhana (मखाना)", "Crunchy low calorie volume food.\nकम कैलोरी और बिना कोलेस्ट्रॉल का सुपर स्नैक।"),
        ("Coconut Water (नारियल पानी)", "Natural electrolytes, stops muscle cramps.\nनेचुरल इलेक्ट्रोलाइट्स जो डिहाइड्रेशन रोकते हैं।")
    ]
    yg = 465
    for title, desc in goods:
        draw.text((60 + col_w + 55, yg), f"+ {title}", font=fh_b(19), fill=(74, 222, 128, 255))
        d_l = desc.split("\n")
        draw.text((60 + col_w + 55, yg + 28), d_l[0], font=fe_r(16), fill=(230, 240, 235, 255))
        draw.text((60 + col_w + 55, yg + 50), d_l[1], font=fh_m(15), fill=(190, 220, 200, 255))
        yg += 140

    draw_pill(draw, 60, 1100, W - 120, 80, "EAT SMART THIS NAVRATRI - सही सात्विक डाइट अपनाएं", fh_b(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_03_vrat_sabudana_vs_satvik.jpg", "JPEG", quality=92)
    print("Post 3 (Bilingual) created")

# =========================================================================
# 4. GYM MISTAKE 1: Ego Lifting (Bilingual)
# =========================================================================
def make_mistake_post_1():
    canvas, draw = base_poster(f"{ASSETS}/indian_male_lifting.jpg", overlay_color=(10, 12, 16), opacity=0.90)
    common_header(draw, "MISTAKE #1", "जिम की गलती #1", cat_bg=(239, 68, 68), cat_fg=(255, 255, 255))

    circle_img = make_circle_crop(f"{ASSETS}/indian_male_lifting.jpg", 390, border_color=(239, 68, 68), border_width=8)
    canvas.paste(circle_img, (W - 440, 170), circle_img)

    draw.text((60, 165), "GYM MISTAKE #1", font=fe_eb(52), fill=(248, 113, 113, 255))
    draw.text((60, 225), "ईगो लिफ्टिंग और बिना वार्म-अप वजन", font=fh_b(36), fill=(255, 255, 255, 255))
    draw.text((60, 290), "EGO LIFTING & SKIPPING WARM-UPS", font=fe_eb(28), fill=(255, 60, 0, 255))
    draw.text((60, 335), "Why 90% beginners get injured in Month 1", font=fe_b(22), fill=(200, 205, 220, 255))

    points = [
        ("01", "LIFTING TOO HEAVY (क्षमता से ज्यादा वजन)", "Trying to impress others with rounded back on deadlifts.\nदूसरों को दिखाने के लिए कमर मोड़कर डेडलिफ्ट या बेंच लगाना।"),
        ("02", "INJURY RISK (नसों और रीढ़ की हड्डी पर जोर)", "Ego lifting does not build muscle; it tears joints and discs.\nभारी वजन बिना फॉर्म के उठाने से स्लिप डिस्क और कंधे की चोट होती है।"),
        ("03", "SKIPPING MOBILITY (बिना वार्म-अप रॉड पकड़ना)", "Jumping straight to heavy barbell with cold, stiff joints.\nदिनभर बैठने के बाद सीधे भारी रॉड उठाना सबसे खतरनाक है।"),
        ("04", "MASTER FORM FIRST (पहले सही पोस्चर सीखें)", "Progressive overload works only when form is 100% textbook.\nपहले हल्के वजन से सही फॉर्म सीखें। वजन अपने आप बढ़ेगा।")
    ]

    y = 585
    for num, title, desc in points:
        draw_pill(draw, 60, y, 48, 36, num, fe_eb(18), (239, 68, 68), (255, 255, 255))
        draw.text((125, y + 2), title, font=fh_b(22), fill=(255, 255, 255, 255))
        d_l = desc.split("\n")
        draw.text((125, y + 34), d_l[0], font=fe_r(17), fill=(230, 235, 245, 255))
        draw.text((125, y + 58), d_l[1], font=fh_m(17), fill=(248, 180, 180, 255))
        y += 122

    draw_pill(draw, 60, 1100, W - 120, 80, "TRAIN SMART, NOT EGO - सही कोच के साथ वर्कआउट करें", fh_b(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_04_gym_mistake_ego_lifting.jpg", "JPEG", quality=92)
    print("Post 4 (Bilingual) created")

# =========================================================================
# 5. GYM MISTAKE 2: Spot Reduction (Bilingual)
# =========================================================================
def make_mistake_post_2():
    canvas, draw = base_poster(f"{ASSETS}/indian_female_fitness.jpg", overlay_color=(10, 12, 16), opacity=0.90)
    common_header(draw, "MISTAKE #2", "जिम की गलती #2", cat_bg=(239, 68, 68), cat_fg=(255, 255, 255))

    circle_img = make_circle_crop(f"{ASSETS}/indian_female_fitness.jpg", 390, border_color=(255, 60, 0), border_width=8)
    canvas.paste(circle_img, (W - 440, 170), circle_img)

    draw.text((60, 165), "GYM MISTAKE #2", font=fe_eb(52), fill=(248, 113, 113, 255))
    draw.text((60, 225), "सिर्फ पेट कम करने के लिए 500 क्रंचेस", font=fh_b(36), fill=(255, 255, 255, 255))
    draw.text((60, 290), "THE SPOT REDUCTION BELLY FAT MYTH", font=fe_eb(28), fill=(255, 60, 0, 255))
    draw.text((60, 335), "Why sit-ups alone will NEVER burn your belly fat", font=fe_b(22), fill=(200, 205, 220, 255))

    facts = [
        ("01", "NO SPOT REDUCTION (पेट से सिर्फ चर्बी नहीं घटती)", "You cannot choose where fat burns; it burns from whole body.\nशरीर किसी एक हिस्से से चर्बी नहीं घटाता, फैट पूरी बॉडी से घटता है।"),
        ("02", "CRUNCHES BUILD ABS (क्रंचेस से फैट नहीं गलता)", "Crunches strengthen muscle underneath, won't melt fat on top.\nक्रंचेस से पेट की मांसपेशी मजबूत होती है, लेकिन ऊपर का फैट नहीं जलता।"),
        ("03", "CALORIE DEFICIT (कैलोरी की कमी जरूरी है)", "If you eat in surplus, no exercise can shrink your waistline.\nजरूरत से ज्यादा खाएंगे तो कोई भी एक्सरसाइज पेट अंदर नहीं कर सकती।"),
        ("04", "THE REAL FIX (कंपाउंड लिफ्ट्स + डाइट)", "Squats, Deadlifts & 300 kcal deficit will melt fat automatically.\nस्क्वाट्स, डेडलिफ्ट और सही डाइट से पेट अपने आप अंदर होगा।")
    ]

    y = 585
    for num, title, desc in facts:
        draw_pill(draw, 60, y, 48, 36, num, fe_eb(18), (255, 60, 0), (255, 255, 255))
        draw.text((125, y + 2), title, font=fh_b(22), fill=(255, 255, 255, 255))
        d_l = desc.split("\n")
        draw.text((125, y + 34), d_l[0], font=fe_r(17), fill=(230, 235, 245, 255))
        draw.text((125, y + 58), d_l[1], font=fh_m(17), fill=(250, 200, 180, 255))
        y += 122

    draw_pill(draw, 60, 1100, W - 120, 80, "SCIENTIFIC FAT LOSS - सही साइंस अपनाएं, रिजल्ट पाएं", fh_b(24), (255, 42, 42), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_05_gym_mistake_spot_reduction.jpg", "JPEG", quality=92)
    print("Post 5 (Bilingual) created")

# =========================================================================
# 6. GYM MISTAKE 3: Zero Protein (Bilingual)
# =========================================================================
def make_mistake_post_3():
    canvas, draw = base_poster(f"{ASSETS}/hero_indian_athletes.jpg", overlay_color=(10, 12, 16), opacity=0.90)
    common_header(draw, "MISTAKE #3", "जिम की गलती #3", cat_bg=(239, 68, 68), cat_fg=(255, 255, 255))

    circle_img = make_circle_crop(f"{ASSETS}/indian_trainer_coaching.jpg", 390, border_color=(255, 180, 20), border_width=8)
    canvas.paste(circle_img, (W - 440, 170), circle_img)

    draw.text((60, 165), "GYM MISTAKE #3", font=fe_eb(52), fill=(248, 113, 113, 255))
    draw.text((60, 225), "पसीना 2 घंटे बहाना, लेकिन 0% प्रोटीन", font=fh_b(36), fill=(255, 255, 255, 255))
    draw.text((60, 290), "TRAINING HARD, EATING ZERO PROTEIN", font=fe_eb(28), fill=(255, 60, 0, 255))
    draw.text((60, 335), "Why working out without protein leads to skinny-fat", font=fe_b(22), fill=(200, 205, 220, 255))

    truths = [
        ("01", "MUSCLES TEAR IN GYM (जिम में मसल टूटती है)", "Lifting tears fibers. Without protein (amino acids), they can't repair.\nवजन उठाने से मसल में खिंचाव आता है, जिसे प्रोटीन ही जोड़ता है।"),
        ("02", "CARB OVERLOAD TRAP (सिर्फ रोटी और दाल)", "Pure roti, rice, and watery daal provides barely 25g protein.\nसाधारण दाल-रोटी से मुश्किल से 20-25g प्रोटीन मिलता है, जो नाकाफी है।"),
        ("03", "CONSTANT FATIGUE (लगातार थकान और कमजोरी)", "Without 1.2g-1.5g protein per kg, muscles remain weak.\nबिना प्रोटीन शरीर में रिकवरी नहीं होती और बदन दर्द बना रहता है।"),
        ("04", "EASY PROTEIN FIX (हर मील में प्रोटीन जोड़ें)", "Include Eggs, Paneer, Soya chunks, Curd, or Sattu in every meal.\nअंडा, पनीर, सोयाबीन, दही या सत्तू को अपनी हर डाइट में शामिल करें।")
    ]

    y = 585
    for num, title, desc in truths:
        draw_pill(draw, 60, y, 48, 36, num, fe_eb(18), (255, 180, 20), (0, 0, 0))
        draw.text((125, y + 2), title, font=fh_b(22), fill=(255, 255, 255, 255))
        d_l = desc.split("\n")
        draw.text((125, y + 34), d_l[0], font=fe_r(17), fill=(230, 235, 245, 255))
        draw.text((125, y + 58), d_l[1], font=fh_m(17), fill=(250, 220, 180, 255))
        y += 122

    draw_pill(draw, 60, 1100, W - 120, 80, "FREE CUSTOM DIET PLAN - फ्री डाइट प्लान के लिए DM करें", fh_b(24), (34, 197, 94), (0, 0, 0))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_06_gym_mistake_zero_protein.jpg", "JPEG", quality=92)
    print("Post 6 (Bilingual) created")

# =========================================================================
# 7. WHY PROTEIN IS IMPORTANT (Bilingual)
# =========================================================================
def make_why_protein_post():
    canvas, draw = base_poster(f"{ASSETS}/hero_indian_athletes.jpg", overlay_color=(8, 12, 18), opacity=0.90)
    common_header(draw, "NUTRITION SCIENCE", "पोषण विज्ञान", cat_bg=(34, 197, 94), cat_fg=(0, 0, 0))

    draw.text((60, 165), "WHY PROTEIN MATTERS", font=fe_eb(56), fill=(255, 255, 255, 255))
    draw.text((60, 225), "प्रोटीन क्यों जरूरी है? (सिर्फ बॉडीबिल्डर के लिए नहीं)", font=fh_b(36), fill=(74, 222, 128, 255))
    draw.text((60, 290), "4 Scientific Reasons Everyone Needs Daily Protein", font=fe_b(24), fill=(255, 180, 40, 255))

    pillars = [
        ("01", "MUSCLE REPAIR & DEFINITION (मांसपेशियों की मजबूती)", "Supplies essential amino acids to rebuild torn muscle fibers stronger.\nहर कसरत के बाद शरीर को मजबूत, टोंड और ताकतवर बनाने के लिए जरूरी।"),
        ("02", "BURNS CALORIES AUTOMATICALLY (30% कैलोरी खुद बर्न)", "Body burns up to 30% of protein calories just to digest it (TEF)!\nप्रोटीन पचाने में शरीर सबसे ज्यादा कैलोरी खर्च करता है (मेटाबॉलिज्म बूस्ट)।"),
        ("03", "CRUSHES CRAVINGS (भूख और मीठे की तलब खत्म)", "Suppresses hunger hormone ghrelin. Keeps stomach full for 4 hours.\nपेट 4 घंटे तक भरा रहता है, जिससे बार-बार भूख और ओवरईटिंग नहीं होती।"),
        ("04", "SKIN, HAIR & IMMUNITY (बाल और त्वचा की चमक)", "Collagen, antibodies, and hair keratin are all made of protein.\nबाल और स्किन का केराटिन और कोलेजन प्रोटीन से ही बनता है।")
    ]

    y = 380
    for num, title, desc in pillars:
        draw_pill(draw, 60, y, 54, 40, num, fe_eb(20), (34, 197, 94), (0, 0, 0))
        draw.text((130, y + 5), title, font=fh_b(23), fill=(74, 222, 128, 255))
        d_l = desc.split("\n")
        draw.text((130, y + 40), d_l[0], font=fe_r(18), fill=(215, 225, 235, 255))
        draw.text((130, y + 68), d_l[1], font=fh_m(18), fill=(190, 240, 200, 255))
        y += 140

    # Daily target card
    draw.rounded_rectangle([(60, 970), (W - 60, 1055)], radius=18, fill=(18, 24, 34, 235), outline=(74, 222, 128), width=2)
    draw.text((85, 985), "DAILY GOAL: Bodyweight (kg) x 1.4 = Daily Protein in grams", font=fe_eb(22), fill=(255, 255, 255, 255))
    draw.text((85, 1018), "दैनिक लक्ष्य: अपने वजन का 1.2 से 1.5 गुना ग्राम प्रोटीन रोज लें (जैसे 70kg = 90-100g)", font=fh_m(19), fill=(255, 180, 40, 255))

    draw_pill(draw, 60, 1100, W - 120, 80, "HEALTHY LIVING - अपनी सेहत को प्राथमिकता दें (RSA GYM)", fh_b(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_07_why_protein_is_important.jpg", "JPEG", quality=92)
    print("Post 7 (Bilingual) created")

# =========================================================================
# 8. BEST PROTEIN FOODS (Bilingual)
# =========================================================================
def make_best_protein_food_post():
    canvas, draw = base_poster(f"{ASSETS}/navratri_satvik_fitness_food.jpg", overlay_color=(10, 10, 16), opacity=0.92)
    common_header(draw, "INDIAN FOODS", "देसी प्रोटीन", cat_bg=(255, 180, 20), cat_fg=(0, 0, 0))

    draw.text((60, 165), "TOP 6 BUDGET PROTEIN FOODS", font=fe_eb(52), fill=(255, 255, 255, 255))
    draw.text((60, 225), "सस्ते और सबसे असरदार 6 हाई-प्रोटीन फूड्स", font=fh_b(36), fill=(255, 180, 20, 255))
    draw.text((60, 290), "Affordable, High-Yield Indian Sources (Veg & Non-Veg)", font=fe_b(24), fill=(255, 255, 255, 255))

    sources = [
        ("01", "SOYA CHUNKS (50g) / सोया चंक्स", "26g Protein", "52% pure plant protein. Unbeatable budget value. (सबसे सस्ता शाकाहारी प्रोटीन)"),
        ("02", "WHOLE EGGS (3 Boiled) / 3 उबले अंडे", "18g Protein", "Most bioavailable complete protein on earth. (पूरी दुनिया का सबसे शुद्ध प्रोटीन)"),
        ("03", "FRESH PANEER (100g) / ताजा पनीर", "20g Protein", "High quality vegetarian protein + healthy fats. (शाकाहारी लोगों के लिए बेस्ट)"),
        ("04", "CHICKEN BREAST (100g) / चिकन ब्रेस्ट", "31g Protein", "Lean, zero-carb, pure muscle fuel. (कम कैलोरी और सबसे ज्यादा लीन प्रोटीन)"),
        ("05", "CHANA SATTU (50g) / चना सत्तू ड्रिंक", "12g Protein", "Bihar's native superfood for stamina & energy. (बिहार का देसी सुपरफूड स्टैमिना के लिए)"),
        ("06", "THICK DAHI (200g) / ताजा गाढ़ा दही", "10g Protein", "Slow-digesting casein + gut probiotics. (पाचन के लिए बेस्ट और स्लो प्रोटीन)")
    ]

    y = 370
    for num, name, macro, desc in sources:
        draw_pill(draw, 60, y, 48, 36, num, fe_eb(18), (255, 180, 20), (0, 0, 0))
        draw.text((125, y + 2), name, font=fh_b(22), fill=(255, 255, 255, 255))
        draw_pill(draw, W - 230, y - 2, 170, 38, macro, fe_eb(18), (34, 197, 94), (0, 0, 0))
        draw.text((125, y + 36), desc, font=fh_m(17), fill=(210, 220, 235, 255))
        y += 112

    draw_pill(draw, 60, 1100, W - 120, 80, "MEAL BLUEPRINT AVAILABLE - डाइट चार्ट के लिए संपर्क करें", fh_b(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_08_best_indian_protein_foods.jpg", "JPEG", quality=92)
    print("Post 8 (Bilingual) created")

# =========================================================================
# 9. BEFORE GOING TO GYM (Bilingual)
# =========================================================================
def make_before_gym_post():
    canvas, draw = base_poster(f"{ASSETS}/indian_male_lifting.jpg", overlay_color=(10, 12, 16), opacity=0.90)
    common_header(draw, "PRE-WORKOUT", "वर्कआउट से पहले", cat_bg=(255, 100, 30), cat_fg=(255, 255, 255))

    circle_img = make_circle_crop(f"{ASSETS}/indian_male_lifting.jpg", 390, border_color=(255, 100, 30), border_width=8)
    canvas.paste(circle_img, (W - 440, 170), circle_img)

    draw.text((60, 165), "BEFORE YOU HIT GYM", font=fe_eb(52), fill=(255, 255, 255, 255))
    draw.text((60, 225), "जिम जाने से पहले: 4 जरूरी नियम", font=fh_b(36), fill=(255, 100, 30, 255))
    draw.text((60, 290), "4 PRE-WORKOUT RULES FOR MAXIMUM ENERGY", font=fe_eb(26), fill=(255, 190, 40, 255))
    draw.text((60, 335), "Follow these to double your strength & stamina", font=fe_b(22), fill=(200, 205, 220, 255))

    rules = [
        ("01", "CARB MEAL 45M BEFORE (45 मिनट पहले हल्का खाना)", "Eat complex carbs (1-2 Bananas, Oats, or Peanut Butter Toast).\n1-2 केला या ओट्स खाएं, ताकि कसरत के दौरान एनर्जी खत्म न हो।"),
        ("02", "HYDRATE 500ML WATER (500ml पानी पिएं)", "A 2% drop in hydration drops muscle strength by 15%!\nशरीर में 2% पानी कम होने से ताकत 15% घट जाती है। वर्कआउट से पहले पिएं।"),
        ("03", "HAVE A WORKOUT PLAN (प्लान पहले से तैयार रखें)", "Never wonder 'aaj kya karein'. Know sets, reps, and exercises.\nजिम में जाकर सोचना न पड़े कि आज क्या करना है। सेट और रैप्स तय रखें।"),
        ("04", "5-MIN DYNAMIC MOBILITY (5 मिनट वार्म-अप)", "Arm circles, leg swings, bodyweight squats to lube joint capsules.\nजोड़ों को एक्टिव करने के लिए वार्म-अप करें। स्ट्रेचिंग बाद के लिए रखें।")
    ]

    y = 585
    for num, title, desc in rules:
        draw_pill(draw, 60, y, 48, 36, num, fe_eb(18), (255, 100, 30), (255, 255, 255))
        draw.text((125, y + 2), title, font=fh_b(22), fill=(255, 255, 255, 255))
        d_l = desc.split("\n")
        draw.text((125, y + 34), d_l[0], font=fe_r(17), fill=(230, 235, 245, 255))
        draw.text((125, y + 58), d_l[1], font=fh_m(17), fill=(250, 210, 180, 255))
        y += 122

    draw_pill(draw, 60, 1100, W - 120, 80, "FEEL THE POWER - 1 दिन का फ्री ट्रायल पास लें (RSA GYM)", fh_b(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_09_before_gym_checklist.jpg", "JPEG", quality=92)
    print("Post 9 (Bilingual) created")

# =========================================================================
# 10. AFTER GOING TO GYM (Bilingual)
# =========================================================================
def make_after_gym_post():
    canvas, draw = base_poster(f"{ASSETS}/indian_trainer_coaching.jpg", overlay_color=(10, 12, 16), opacity=0.90)
    common_header(draw, "POST-WORKOUT", "वर्कआउट के बाद", cat_bg=(34, 197, 94), cat_fg=(0, 0, 0))

    circle_img = make_circle_crop(f"{ASSETS}/hero_indian_athletes.jpg", 390, border_color=(34, 197, 94), border_width=8)
    canvas.paste(circle_img, (W - 440, 170), circle_img)

    draw.text((60, 165), "AFTER YOU FINISH GYM", font=fe_eb(52), fill=(255, 255, 255, 255))
    draw.text((60, 225), "जिम खत्म करने के बाद: 4 रिकवरी नियम", font=fh_b(36), fill=(74, 222, 128, 255))
    draw.text((60, 290), "4 POST-WORKOUT RULES TO LOCK IN RESULTS", font=fe_eb(26), fill=(255, 180, 40, 255))
    draw.text((60, 335), "Muscles grow outside the gym when you follow this", font=fe_b(22), fill=(200, 205, 220, 255))

    rules = [
        ("01", "PROTEIN WITHIN 90 MINS (90 मिनट के अंदर प्रोटीन)", "Take 20-30g protein (Eggs, Paneer, Whey, or Soya) to reload.\n20-30g प्रोटीन (अंडा, पनीर, सत्तू या शेक) लें ताकि मसल रिकवर हो सके।"),
        ("02", "5-MIN STATIC STRETCHING (5 मिनट स्ट्रेचिंग)", "Stretch tight muscles. Restores muscle length and cuts soreness.\nमांसपेशियों को रिलैक्स करें ताकि अगले दिन बदन दर्द और अकड़न न रहे।"),
        ("03", "REPLACE SWEAT & SODIUM (पानी और नमक की भरपाई)", "Drink 700ml+ water with a pinch of salt to rehydrate.\nपसीने में निकला पानी और मिनरल्स तुरंत पानी पीकर पूरा करें।"),
        ("04", "7-8 HOURS SLEEP (7-8 घंटे गहरी नींद)", "Muscles grow in bed! Growth hormone peaks during deep sleep.\nमसल जिम में नहीं, सोते समय बनती है। गहरी नींद सबसे ज्यादा जरूरी है।")
    ]

    y = 585
    for num, title, desc in rules:
        draw_pill(draw, 60, y, 48, 36, num, fe_eb(18), (34, 197, 94), (0, 0, 0))
        draw.text((125, y + 2), title, font=fh_b(22), fill=(255, 255, 255, 255))
        d_l = desc.split("\n")
        draw.text((125, y + 34), d_l[0], font=fe_r(17), fill=(230, 235, 245, 255))
        draw.text((125, y + 58), d_l[1], font=fh_m(17), fill=(190, 240, 200, 255))
        y += 122

    draw_pill(draw, 60, 1100, W - 120, 80, "RECOVER STRONGER - आरा के सबसे बेहतरीन जिम से जुड़ें", fh_b(24), (255, 60, 0), (255, 255, 255))
    common_footer(draw)
    canvas.convert("RGB").save(f"{OUT}/post_10_after_gym_checklist.jpg", "JPEG", quality=92)
    print("Post 10 (Bilingual) created")

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
    print("All 10 bilingual Hindi + English master posters generated!")
