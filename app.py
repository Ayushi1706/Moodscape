from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import colorsys
import random
import math

# Mood keyword mappings to HSL color bases
MOOD_COLORS = {
    # Happy / Joyful
    "happy": [(45, 95, 65), (35, 90, 60), (55, 85, 70)],
    "joy": [(48, 100, 60), (40, 95, 65), (60, 80, 68)],
    "excited": [(20, 95, 58), (35, 100, 55), (10, 90, 60)],
    "cheerful": [(50, 88, 65), (42, 85, 70), (58, 80, 62)],
    "elated": [(45, 100, 62), (55, 95, 58), (38, 88, 68)],

    # Calm / Peaceful
    "calm": [(200, 45, 65), (210, 40, 70), (190, 50, 60)],
    "peaceful": [(195, 50, 68), (205, 45, 72), (185, 55, 65)],
    "serene": [(210, 55, 70), (200, 48, 74), (220, 50, 66)],
    "relaxed": [(180, 40, 68), (195, 45, 72), (170, 38, 65)],
    "tranquil": [(205, 50, 72), (215, 48, 68), (195, 55, 75)],

    # Sad / Melancholy
    "sad": [(220, 30, 48), (230, 25, 52), (210, 35, 45)],
    "melancholy": [(230, 28, 45), (220, 32, 50), (240, 25, 42)],
    "lonely": [(225, 25, 50), (215, 28, 55), (235, 22, 48)],
    "gloomy": [(220, 20, 42), (230, 18, 38), (210, 22, 45)],
    "blue": [(215, 35, 55), (225, 30, 50), (205, 40, 58)],

    # Angry / Intense
    "angry": [(5, 80, 45), (355, 85, 50), (15, 75, 42)],
    "frustrated": [(10, 70, 48), (0, 75, 52), (20, 65, 45)],
    "furious": [(2, 90, 40), (358, 88, 45), (8, 85, 42)],
    "irritated": [(12, 72, 50), (5, 78, 55), (18, 68, 48)],

    # Romantic / Love
    "love": [(345, 75, 62), (355, 70, 65), (330, 68, 68)],
    "romantic": [(340, 65, 65), (350, 60, 70), (325, 70, 62)],
    "passionate": [(350, 82, 55), (340, 78, 58), (5, 80, 52)],
    "tender": [(345, 55, 70), (335, 50, 74), (355, 60, 68)],

    # Anxious / Nervous
    "anxious": [(280, 35, 55), (270, 40, 58), (290, 30, 52)],
    "nervous": [(285, 38, 52), (275, 42, 56), (295, 32, 50)],
    "worried": [(275, 32, 55), (265, 35, 58), (285, 28, 52)],
    "stressed": [(290, 42, 50), (280, 45, 54), (300, 38, 48)],

    # Mysterious / Dark
    "mysterious": [(260, 40, 35), (270, 45, 30), (250, 38, 40)],
    "dark": [(240, 20, 25), (250, 18, 22), (230, 22, 28)],
    "gothic": [(270, 35, 28), (260, 38, 32), (280, 30, 25)],
    "eerie": [(255, 42, 32), (265, 38, 28), (245, 45, 36)],

    # Fresh / Natural
    "fresh": [(145, 55, 60), (155, 50, 65), (135, 58, 58)],
    "natural": [(120, 42, 58), (130, 45, 62), (110, 40, 55)],
    "alive": [(140, 62, 55), (150, 58, 60), (130, 65, 52)],
    "energetic": [(85, 72, 55), (95, 68, 58), (75, 78, 52)],

    # Nostalgic / Warm
    "nostalgic": [(28, 60, 62), (38, 55, 65), (18, 65, 58)],
    "warm": [(30, 75, 60), (40, 70, 65), (20, 80, 58)],
    "cozy": [(25, 65, 65), (35, 60, 70), (15, 70, 62)],
    "homey": [(32, 58, 68), (42, 52, 72), (22, 62, 65)],

    # Cool / Sophisticated
    "cool": [(200, 60, 50), (210, 55, 55), (190, 65, 48)],
    "sophisticated": [(240, 20, 40), (250, 18, 38), (230, 22, 42)],
    "elegant": [(245, 25, 45), (255, 22, 42), (235, 28, 48)],
    "classy": [(230, 15, 45), (240, 12, 42), (220, 18, 48)],
}

FALLBACK_MOODS = {
    "default": [(200, 50, 60), (180, 45, 65), (220, 55, 58)],
}

def find_mood_colors(text):
    """Find matching mood colors from text input."""
    text_lower = text.lower()
    words = text_lower.replace(",", " ").replace(".", " ").replace("!", " ").split()

    matched_palettes = []
    matched_words = []

    for word in words:
        if word in MOOD_COLORS:
            matched_palettes.append(MOOD_COLORS[word])
            matched_words.append(word)

    # Also check partial matches
    if not matched_palettes:
        for word in words:
            for mood_key in MOOD_COLORS:
                if mood_key in word or word in mood_key:
                    matched_palettes.append(MOOD_COLORS[mood_key])
                    matched_words.append(mood_key)
                    break

    return matched_palettes, matched_words

def blend_hsl(colors_list):
    """Blend multiple HSL color tuples."""
    if not colors_list:
        return (200, 50, 60)
    h_sum = sum(c[0] for c in colors_list)
    s_sum = sum(c[1] for c in colors_list)
    l_sum = sum(c[2] for c in colors_list)
    n = len(colors_list)
    return (h_sum / n, s_sum / n, l_sum / n)

def hsl_to_hex(h, s, l):
    """Convert HSL to hex color."""
    s /= 100
    l /= 100
    r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

def generate_palette(base_hsl, palette_size=6):
    """Generate a harmonious palette from a base HSL color."""
    h, s, l = base_hsl
    palette = []

    # Strategies: analogous + complementary + triadic variations
    offsets = [0, 30, -30, 180, 60, -60]
    lightness_variants = [l, l - 15, l + 15, l - 8, l + 8, l - 20]
    sat_variants = [s, s - 10, s + 10, s - 5, s + 5, s - 15]

    for i in range(palette_size):
        new_h = (h + offsets[i % len(offsets)]) % 360
        new_l = max(20, min(85, lightness_variants[i % len(lightness_variants)]))
        new_s = max(15, min(100, sat_variants[i % len(sat_variants)]))
        hex_color = hsl_to_hex(new_h, new_s, new_l)
        palette.append({
            "hex": hex_color,
            "hsl": f"hsl({new_h:.0f}, {new_s:.0f}%, {new_l:.0f}%)",
            "h": round(new_h),
            "s": round(new_s),
            "l": round(new_l)
        })

    return palette

def analyze_mood(text):
    """Main analysis function."""
    if not text.strip():
        return {"error": "Please enter a mood or feeling."}

    matched_palettes, matched_words = find_mood_colors(text)

    if matched_palettes:
        # Blend all matched mood base colors
        all_base_colors = []
        for palette in matched_palettes:
            all_base_colors.extend(palette)
        base_hsl = blend_hsl(all_base_colors)
        mood_label = " + ".join(matched_words[:3])
    else:
        # Default: derive from text character sum
        char_sum = sum(ord(c) for c in text.lower() if c.isalpha())
        h = (char_sum * 37) % 360
        s = 45 + (char_sum % 30)
        l = 50 + (char_sum % 20)
        base_hsl = (h, s, l)
        mood_label = "unique blend"

    palette = generate_palette(base_hsl)

    # Pick a name for the palette
    palette_names = [
        f"The {text.strip().title()} Collection",
        f"Shades of {matched_words[0].title()}" if matched_words else f"Essence of {text.strip()[:15].title()}",
        f"{text.strip()[:20].title()} Spectrum",
    ]
    palette_name = palette_names[1] if matched_words else palette_names[2]

    return {
        "palette": palette,
        "mood": mood_label,
        "palette_name": palette_name,
        "input": text.strip(),
        "matched": bool(matched_words),
        "matched_words": matched_words[:5]
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging

    def do_GET(self):
        if self.path.startswith("/analyze"):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            mood_text = params.get("mood", [""])[0]
            mood_text = urllib.parse.unquote_plus(mood_text)

            result = analyze_mood(mood_text)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        elif self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("Mood Palette Server running on http://localhost:8080")
    server.serve_forever()
