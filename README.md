# 🎨 Moodscape — Mood-Based Color Palette Generator

A simple but unique project that combines **Python** (backend logic) and **HTML/CSS/JS** (frontend UI).

---

## What It Does

Type any feeling or mood in plain English → get a beautiful, harmonious color palette.

**Examples:**

| Mood | Colors |
|------|--------|
| `calm and peaceful` | soft blues and teals |
| `excited and happy` | warm oranges and yellows |
| `melancholy and lonely` | muted cool blues |
| `romantic evening` | dusty pinks and roses |
| `mysterious and dark` | deep purples and indigos |

---

## Project Structure

```
moodscape/
├── app.py          # Python backend server
├── index.html      # Frontend UI
├── style.css       # Styles (external)
└── README.md
```

---

## How It Works

### 🐍 Python (`app.py`)

- Keyword-maps **50+ mood words** to HSL color bases
- Blends colors when **multiple moods** are detected
- Generates harmonious palettes using **analogous + complementary** color theory
- Serves everything via a simple built-in HTTP server — **no dependencies!**

### 🖼️ Frontend (`index.html` + `style.css`)

- Elegant editorial design with grain texture and Fraunces serif font
- Animated swatch reveal with smooth hover interactions
- Click any swatch or hex tag to **copy the color code**
- Export your palette as **CSS variables** or **JSON**
- Save palettes to **history** (localStorage)
- Works **offline** too — has a client-side fallback if the Python server isn't running

---

## Features

- ✅ Plain English mood input
- ✅ 6-color harmonious palette output
- ✅ Click-to-copy hex codes
- ✅ Export as CSS variables or JSON
- ✅ Palette history (saved in browser)
- ✅ Suggestion chips for quick mood selection
- ✅ Offline-capable with client-side fallback

---

## License

MIT — free to use, modify, and share.
