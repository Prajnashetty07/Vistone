import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from skin_tone import classify_monk_v9_5

# === Configuration ===
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(APP_ROOT, "static", "uploads")
ALLOWED_EXT = {"jpg", "jpeg", "png", "webp"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)


# === Helper Function ===
def allowed(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# === Color Psychology Dictionary (Positive Meanings) ===
color_psychology = {
    "Deep Charcoal Blue": "Symbolizes depth, confidence, and calm authority — enhances clarity and focus.",
    "Soft Berry Pink": "Represents warmth, charm, and affection — adds approachability.",
    "Cool Emerald": "Evokes balance, sophistication, and renewal — for calm confidence.",
    "Muted Teal": "Symbolizes stability and rejuvenation — balances emotion and logic.",
    "Soft Coral Rose": "Represents passion and warmth — uplifting yet sophisticated.",
    "Earthy Olive Green": "Signifies resilience and natural strength — grounding yet refreshing.",
    "Dusty Lavender": "Represents creativity, tranquility, and balance — soothing and timeless.",
    "Slate Blue": "Symbolizes calm intelligence and reliability — composed personalities.",
    "Peony Pink": "Evokes romance, confidence, and playfulness — soft yet empowering.",
    "Midnight Navy": "Represents wisdom, professionalism, and trust — conveys authority.",
    "Mauve Rose": "Symbolizes compassion, elegance, and poise — romantic but subtle.",
    "Deep Forest Green": "Represents growth and grounding — deeply natural and confident.",
    "Terracotta Clay": "Represents warmth and creativity — earthy and expressive.",
    "Warm Moss Green": "Symbolizes harmony and stability — nature’s calm essence.",
    "Muted Cranberry": "Evokes strength and refinement — quietly confident.",
    "Dusty Periwinkle": "Represents calm intelligence — imaginative and composed.",
    "Soft Steel Blue": "Symbolizes clarity and calm — emotionally grounded.",
    "Blush Pink": "Represents tenderness and grace — universally flattering.",
    "Slate Navy": "Conveys professionalism and self-assurance — cool stability.",
    "Dusty Rose": "Represents emotional warmth and nostalgia — elegant and timeless.",
    "Pine Green": "Symbolizes endurance and harmony — deeply grounding.",
    "Muted Terracotta": "Represents grounded creativity and strength — mature warmth.",
    "Golden Olive": "Symbolizes prosperity and optimism — earthy liveliness.",
    "Brick Red": "Represents confidence and strength — classic and bold.",
    "Smoky Lavender": "Represents calm and self-reflection — mystical and refined.",
    "Storm Blue": "Evokes trust and composure — balanced energy.",
    "Neutral Rosewood": "Symbolizes warmth and luxury — romantic understatement.",
    "Deep Sapphire": "Represents intelligence, focus, and stability — evokes inner power.",
    "Mulberry Wine": "Symbolizes mystery, elegance, and confidence — bold refinement.",
    "Cedar Green": "Represents endurance and renewal — earthy sophistication.",
    "Burnt Sienna": "Symbolizes warmth, creativity, and confidence — expressive tone.",
    "Honey Bronze": "Represents optimism and luxury — grounded richness.",
    "Warm Burgundy": "Evokes passion and depth — bold and refined.",
    "Dusty Plum": "Represents wisdom and mystery — feminine introspection.",
    "Steel Teal": "Symbolizes calm control and clarity — modern timelessness.",
    "Mauve Cocoa": "Represents warmth and depth — inviting sophistication.",
    "Deep Teal": "Represents emotional intelligence and calm — introspective depth.",
    "Blackberry Purple": "Symbolizes creativity and individuality — thoughtful confidence.",
    "Midnight Blue": "Represents serenity and trust — elegant stability.",
    "Rust Brown": "Represents stability and grounded warmth — earthy dependability.",
    "Marigold Ochre": "Symbolizes joy and vitality — confident warmth.",
    "Cocoa Brick": "Represents comfort and dependability — timeless warmth.",
    "Smoky Rosewood": "Symbolizes romantic confidence and passion — refined energy.",
    "Pewter Blue": "Represents balance and composure — cool sophistication.",
    "Soft Mulberry": "Evokes creativity and expression — classy playfulness.",
    "Sapphire Blue": "Represents wisdom, confidence, and reliability — polished clarity.",
    "Deep Fig Purple": "Symbolizes power and creativity — introspective boldness.",
    "Teal Navy": "Represents calm leadership — expressive refinement.",
    "Burnt Copper": "Symbolizes energy and transformation — passionate warmth.",
    "Golden Saffron": "Represents optimism and vitality — uplifting power.",
    "Warm Espresso Brown": "Conveys stability and refinement — dependable elegance.",
    "Blackened Plum": "Symbolizes sophistication and depth — warm mystery.",
    "Stormy Teal": "Represents balance and calm — modern tranquility.",
    "Cedar Brown": "Symbolizes comfort and tradition — familiar strength.",
    "Deep Indigo Blue": "Represents intelligence and calm — perceptive depth.",
    "Black Cherry": "Symbolizes strength and sensuality — confident uniqueness.",
    "Pine Teal": "Represents renewal and focus — harmonizing energy.",
    "Burnt Umber": "Symbolizes grounded confidence — natural classic.",
    "Ember Red": "Represents courage and energy — warm passion.",
    "Caramel Bronze": "Symbolizes warmth and charisma — radiant confidence.",
    "Deep Mauve Brown": "Represents sophistication and balance — refined neutrality.",
    "Petrol Blue": "Symbolizes intelligence and composure — elegant modernity.",
    "Mahogany Red": "Represents depth and strength — confident richness.",
    "Royal Sapphire": "Represents nobility and confidence — empowering sophistication.",
    "Eggplant Purple": "Symbolizes creativity and individuality — bold luxury.",
    "Deep Teal Green": "Represents balance and renewal — grounded freshness.",
    "Molten Copper": "Symbolizes passion and creativity — magnetic warmth.",
    "Rich Maroon": "Represents depth and sensuality — powerful elegance.",
    "Golden Amber": "Symbolizes optimism and success — radiant energy.",
    "Raisin Plum": "Represents reflection and poise — graceful femininity.",
    "Slate Petrol": "Symbolizes calm sophistication — balanced intelligence.",
    "Cinnamon Brown": "Evokes comfort and strength — authentic grounding.",
    "Royal Cobalt": "Represents strength and intelligence — calm authority.",
    "Deep Aubergine": "Symbolizes creativity and luxury — deep elegance.",
    "Emerald Teal": "Represents renewal and clarity — elegant freshness.",
    "Metallic Bronze": "Represents ambition and resilience — bold empowerment.",
    "Blood Red": "Symbolizes passion and power — strong confidence.",
    "Golden Curry": "Represents creativity and warmth — lively energy.",
    "Deep Clove Brown": "Conveys maturity and strength — classic dependability.",
    "Petrol Slate": "Symbolizes focus and balance — calm professionalism.",
    "Royal Sapphire Blue": "Represents calm authority — classic confidence.",
    "Molten Gold": "Symbolizes prosperity and inspiration — radiant positivity.",
    "Oxblood Red": "Represents confidence and strength — deep power.",
    "Rich Henna Brown": "Evokes warmth and maturity — timeless dependability.",
}

# === Monk Skin Tone Scale Colors ===
mst_scale = [
    {"hex": "#f6ede4", "tone": 1},
    {"hex": "#f3e7db", "tone": 2},
    {"hex": "#f7ead0", "tone": 3},
    {"hex": "#eadaba", "tone": 4},
    {"hex": "#d7bd96", "tone": 5},
    {"hex": "#a07e56", "tone": 6},
    {"hex": "#825c43", "tone": 7},
    {"hex": "#604134", "tone": 8},
    {"hex": "#3b312a", "tone": 9},
    {"hex": "#292420", "tone": 10}
]

# === Smart Psychology Lookup ===
def get_color_psychology(color_name: str, avoid: bool = False) -> str:
    """Return color psychology text for both best and avoid colors."""
    if not color_name:
        return "This color enhances your natural tone beautifully." if not avoid else "This color may clash with your natural undertone."

    # Exact match first
    if color_name in color_psychology:
        base = color_psychology[color_name]
        return base if not avoid else f"This shade may clash or feel overpowering. ({base})"

    # Colors to Avoid — Refined Descriptions
    keyword_map = {
        "Pale Peach": "Appears washed-out and may drain warmth from the skin — reduces natural glow.",
        "Neon Lime": "Too bright and artificial — clashes with most undertones and distracts from complexion.",
        "Ivory Beige": "Can make the complexion appear dull or uneven — lacks contrast.",
        "Lemon Yellow": "Overly vibrant — exaggerates redness and uneven tones.",
        "Bright Tomato Red": "Too intense — may overpower the natural balance of the skin tone.",
        "Cool Light Gray": "Makes the skin appear pale or muted — lacks warmth.",
        "Warm Mustard Yellow": "Too saturated — may clash with cooler undertones.",
        "Electric Orange": "Overly vibrant — draws attention away from natural undertone harmony.",
        "Pale Sand Beige": "Too light — tends to flatten deeper tones and reduce radiance.",
        "Neon Pink": "Overly reflective — competes with undertone vibrancy.",
        "Pastel Lavender": "Too cool — can make skin appear grayish or faded.",
        "Golden Yellow": "Can exaggerate uneven tones — overpowers medium to deep undertones.",
        "Pumpkin Orange": "Too intense — may clash with cool undertones.",
        "Golden Khaki": "Adds dullness to complexion — lacks freshness.",
        "Warm Mustard": "Overly rich — appears heavy on cool tones.",
        "Neon Tangerine": "Too bright and reflective — distracts from natural tone.",
        "Ash Gray": "Flattens and dulls undertones — removes warmth.",
        "Icy Mint": "Too cool and pale — clashes with warm undertones.",
        "Bright Magenta": "Highly saturated — can overpower neutral tones.",
        "Powder Blue": "Makes skin appear faded — lacks contrast.",
        "Icy Sky Blue": "Too light — cool tones appear flat or dull.",
        "Neon Fuchsia": "Overly vivid — distracts from natural features.",
        "Dusty Beige": "Too muted — removes freshness and contrast.",
        "Yellow Pastel": "Too pale — exaggerates uneven undertones.",
        "Lime Neon": "Harsh and unnatural — unflattering for most tones.",
        "Beige-Taupe": "Too close to natural undertones — drains vibrancy.",
        "Pale Lemon": "Overly bright — reduces contrast and balance.",
        "Light Peach": "Too subtle — dulls complexion.",
        "Acid Yellow": "Highly reflective — unflattering for all undertones.",
        "Dusty Sand Beige": "Too muted — lacks vitality and warmth.",
        "Cool Ash Gray": "Makes skin appear flat and lifeless.",
        "Cold Ash Gray": "Drains color — removes warmth from the complexion.",
        "Beige Peach": "Too similar to undertone — looks washed out.",
        "Lime Green": "Too neon — creates unnatural contrast.",
        "Pastel Blue": "Too pale — lacks depth against skin.",
        "Dusty Mauve": "Too cool — reduces skin warmth.",
        "Light Sand Beige": "Too close to skin shade — flattens depth.",
        "Baby Blue": "Overly pale — clashes with warm undertones.",
        "Soft Lavender Gray": "Too cool — lacks harmony with warm tones.",
        "Sandy Beige": "Washes out deeper tones — lacks contrast.",
        "Pastel Orange": "Too soft — drains vibrancy from medium tones.",
        "Cool Mist Gray": "Too muted — dulls complexion.",
        "Light Butter Yellow": "Overly pale — reduces contrast and radiance.",
        "Peach Blush": "Too soft — lacks dimension on deeper tones.",
        "Powder Yellow": "Too muted — exaggerates dullness.",
        "Silver Gray": "Flattens complexion — removes warmth.",
        "Dusty Sage": "Too muted — lacks freshness and vitality.",
        "Baby Lavender": "Overly pale — lacks energy and depth.",
        "Neon Lime Green": "Harsh and reflective — rarely complements any undertone.",
        "Butter Yellow": "Overly light — exaggerates imperfections.",
        "Cool Silver Gray": "Too cold — removes natural warmth.",
        "Powder Pink": "Overly pale — lacks vitality.",
        "Neon Chartreuse": "Highly reflective — visually overwhelming.",
    }

    if color_name in keyword_map:
        return keyword_map[color_name]

    return "This color enhances your natural tone beautifully." if not avoid else "This shade is less flattering for your undertone."


# === Routes ===
@app.route("/", methods=["GET"])
def index():
    """Display the home upload page."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """Handle image upload and color analysis."""
    file = request.files.get("image")
    if not file or file.filename == "":
        flash("Please upload an image.")
        return redirect(url_for("index"))

    if not allowed(file.filename):
        flash("Unsupported file type. Use JPG/PNG/WebP.")
        return redirect(url_for("index"))

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    try:
        result = classify_monk_v9_5(save_path, debug=False)
    except Exception as e:
        print("[error] analyze:", e)
        flash("Could not analyze the photo. Try a clearer, front-facing image.")
        return redirect(url_for("index"))

    tone = result.get("tone", 5)
    undertone = result.get("undertone", "Neutral")
    best_colors = result.get("best_colors", []) or []
    avoid_colors = result.get("avoid_colors", []) or []

    return render_template(
        "result.html",
        image_url=url_for("static", filename=f"uploads/{filename}"),
        tone=tone,
        undertone=undertone,
        best_colors=best_colors,
        avoid_colors=avoid_colors,
        color_psychology=color_psychology,
        get_color_psychology=get_color_psychology,
        mst_scale=mst_scale
    )


# === Main Entry Point ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)