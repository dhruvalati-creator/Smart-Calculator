# 🧮 Smart Calculator (Cross-Platform Desktop & PWA)

[![PWA Ready](https://img.shields.io/badge/PWA-Installable-purple.svg)](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-CustomTkinter-indigo.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/tests-36%20passing-brightgreen.svg)]()

A professional, modern calculator available both as a **native desktop application (Python & CustomTkinter)** and as an **installable Progressive Web App (PWA)** that runs offline on **Windows, macOS, Linux, Android, and iOS/iPadOS**.

---

## 🌟 Key Features

### 📱 Progressive Web App (PWA)
- **100% Offline Capability**: Uses a Service Worker (`sw.js`) with Cache-First asset precaching so the calculator works anywhere without an internet connection.
- **Installable**: Installs directly to your Windows desktop or Android/iOS home screen like a native app.
- **Responsive Layout**: Fluid UI optimized for desktop monitors, tablets, and mobile phones with touch-friendly tap targets ($\ge 48\text{px}$) and haptic feedback.
- **Custom Loading Splash**: Custom high-resolution vector and PNG icons (512x512, 192x192, maskable, SVG).
- **History Storage**: Automatically saves up to 50 previous calculations in browser `localStorage`. Allows one-click calculation reuse and individual deletion.

### 🖥️ Native Desktop GUI (Python)
- **Two Modes**: Standard mode for daily math and Scientific mode for advanced computing.
- **Themes**: Instant toggle between Dark Charcoal and Clean Light themes without restart.
- **Safety**: Safe expression evaluator using Abstract Syntax Trees (`ast` in Python, Recursive Descent Parser in JS) without unsafe `eval()`.
- **Keyboard Shortcuts**: Complete desktop keyboard integration (`0-9`, `+ - * / ^ % ( )`, `Enter`, `Backspace`, `Esc`, `s`, `c`, `t`, `l`, `p`).

---

## 🏗️ Project Architecture & Folder Structure

```text
smart_calculator/
│
├── web/                        # Progressive Web Application (PWA)
│   ├── index.html              # Modern responsive HTML5 interface & splash screen
│   ├── manifest.json           # PWA metadata, standalone display & theme colors
│   ├── sw.js                   # Service Worker precaching & offline caching
│   ├── test_calc.html          # Automated browser test suite for JS engine
│   ├── generate_icons.py       # Icon generator (SVG, PNG 512, 192, 180, 32)
│   ├── css/
│   │   └── style.css           # Modern CSS with dark/light themes & fluid layout
│   ├── js/
│   │   ├── calculator.js       # Core math engine & safe recursive-descent evaluator
│   │   └── app.js              # PWA controller, install prompt, history, key bindings
│   └── icons/
│       ├── icon-512.png        # 512x512 maskable app icon
│       ├── icon-192.png        # 192x192 mobile icon
│       ├── apple-touch-icon.png# 180x180 iOS home screen icon
│       ├── favicon.png         # 32x32 browser favicon
│       └── icon.svg            # Scalable vector icon
│
├── smart_calculator/           # Native Python Package
│   ├── __init__.py             # Package initializer
│   ├── calculator.py           # Core math logic & business calculations (OOP)
│   ├── evaluator.py            # Safe AST-based expression evaluator
│   ├── history.py              # Persistent JSON history (add, get, delete, clear)
│   ├── gui_theme.py            # Dark & Light palettes, fonts, styling
│   ├── gui.py                  # Professional CustomTkinter desktop interface
│   └── ui.py                   # Terminal CLI fallback
│
├── tests/
│   ├── test_calculator.py      # 28 unit tests (core math, evaluator, history)
│   └── test_gui.py             # 8 automated GUI component tests
│
├── data/
│   └── history.json            # Persistent JSON calculation records
│
├── web_server.py               # Local server displaying Local & LAN IP for mobile
├── run_web.bat                 # One-click Windows launcher for Web App (PWA)
├── main.py                     # Entry point for native Python GUI
├── run.bat                     # One-click Windows launcher for native Desktop GUI
├── requirements.txt            # Python dependencies (customtkinter, Pillow)
└── README.md                   # Complete documentation
```

---

## 🚀 Running the Web Application (PWA)

### Option 1: One-Click Windows Launcher
Double-click **`run_web.bat`** in the project directory.

### Option 2: Command Line
Run the local web server:
```bash
python web_server.py
```

The terminal will display your access URLs:
```text
=================================================================
         🧮 SMART CALCULATOR - PROGRESSIVE WEB APP (PWA)        
=================================================================
 [*] Local PC URL:       http://localhost:8000
 [*] Mobile / LAN URL:   http://192.168.1.x:8000
-----------------------------------------------------------------
```

Your default web browser will open `http://localhost:8000` automatically.

---

## 📲 How to Install as an App

### 1. On Windows (Desktop)
1. Open `http://localhost:8000` in **Google Chrome** or **Microsoft Edge**.
2. Click the **📲 Install** button in the calculator header, or click the **Install App icon** in your browser's address bar.
3. Click **Install**.
4. A dedicated, borderless desktop app window opens with its own taskbar icon and desktop shortcut.

### 2. On Android (Phones & Tablets)
1. Connect your phone to the same Wi-Fi network as your computer.
2. In **Chrome**, open the LAN URL shown in your terminal (e.g., `http://192.168.1.x:8000`).
3. Tap the **📲 Install** button in the calculator header, or open the Chrome menu (**⋮**) and tap **"Add to Home screen"** or **"Install app"**.
4. The Smart Calculator icon will appear on your phone's home screen and app drawer. It launches full-screen and functions 100% offline.

### 3. On iPhone & iPad (iOS / Safari)
1. Open the LAN URL in **Safari**.
2. Tap the **Share** button (**⎋**).
3. Scroll down and tap **"Add to Home Screen"**.
4. Tap **Add**. Smart Calculator will appear on your home screen and open without Safari address bars.

---

## 🧪 Testing

### 1. Automated Python Test Suite
Run all 36 automated unit and GUI component tests:
```bash
python -m unittest discover -s tests -v
```

### 2. Browser Unit Tests (JavaScript Engine)
With the server running, navigate to:
```text
http://localhost:8000/test_calc.html
```
This runs 30+ browser test assertions checking operator precedence, scientific functions, and division-by-zero handling.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
