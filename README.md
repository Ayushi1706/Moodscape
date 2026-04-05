# 🎨 Moodscape — Mood-Based Color Palette Generator

A simple but unique project that combines **Python** (backend logic) and **HTML/CSS/JS** (frontend UI).

## What It Does
Type any feeling or mood in plain English → get a beautiful, harmonious color palette.

**Examples:**
- `calm and peaceful` → soft blues and teals
- `excited and happy` → warm oranges and yellows
- `melancholy and lonely` → muted cool blues
- `romantic evening` → dusty pinks and roses
- `mysterious and dark` → deep purples and indigos

## How It Works

### Python (`app.py`)
- Keyword-maps 50+ mood words to HSL color bases
- Blends colors when multiple moods are detected
- Generates harmonious palettes using analogous + complementary color theory
- Serves everything via a simple built-in HTTP server (no dependencies!)

### Frontend (`index.html`)
- Elegant editorial design with grain texture, Fraunces serif font
- Animated swatch reveal with hover interactions
- Click any swatch or hex tag to copy the color code
- Export your palette as **CSS variables** or **JSON**
- Save palettes to **history** (localStorage)
- Works offline too — has a client-side fallback if Python server isn't running

