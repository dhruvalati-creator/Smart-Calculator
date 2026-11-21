"""
Generates crisp PWA icons in PNG and SVG formats.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def generate_icons(output_dir="web/icons"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Create SVG Icon
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4f46e5" />
      <stop offset="50%" stop-color="#6366f1" />
      <stop offset="100%" stop-color="#8b5cf6" />
    </linearGradient>
    <linearGradient id="displayGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#18181b" />
      <stop offset="100%" stop-color="#27272a" />
    </linearGradient>
    <linearGradient id="btnGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#3f3f46" />
      <stop offset="100%" stop-color="#27272a" />
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="16" stdDeviation="16" flood-color="#000000" flood-opacity="0.35" />
    </filter>
  </defs>

  <!-- Outer Rounded Square Background -->
  <rect x="16" y="16" width="480" height="480" rx="108" fill="url(#bgGrad)" filter="url(#shadow)" />

  <!-- Calculator Body -->
  <rect x="72" y="72" width="368" height="368" rx="48" fill="#18181b" />

  <!-- Display -->
  <rect x="100" y="104" width="312" height="76" rx="20" fill="url(#displayGrad)" stroke="#3f3f46" stroke-width="2" />
  <circle cx="124" cy="142" r="6" fill="#10b981" />
  <text x="388" y="152" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="34" font-weight="bold" fill="#60a5fa" text-anchor="end">123,456</text>

  <!-- Keypad Grid (3x3 grid + equal) -->
  <!-- Row 1 -->
  <rect x="100" y="200" width="68" height="52" rx="14" fill="url(#btnGrad)" />
  <text x="134" y="235" font-family="sans-serif" font-size="24" font-weight="bold" fill="#f4f4f5" text-anchor="middle">7</text>

  <rect x="180" y="200" width="68" height="52" rx="14" fill="url(#btnGrad)" />
  <text x="214" y="235" font-family="sans-serif" font-size="24" font-weight="bold" fill="#f4f4f5" text-anchor="middle">8</text>

  <rect x="260" y="200" width="68" height="52" rx="14" fill="url(#btnGrad)" />
  <text x="294" y="235" font-family="sans-serif" font-size="24" font-weight="bold" fill="#f4f4f5" text-anchor="middle">9</text>

  <rect x="340" y="200" width="72" height="52" rx="14" fill="#3b82f6" />
  <text x="376" y="236" font-family="sans-serif" font-size="28" font-weight="bold" fill="#ffffff" text-anchor="middle">÷</text>

  <!-- Row 2 -->
  <rect x="100" y="264" width="68" height="52" rx="14" fill="url(#btnGrad)" />
  <text x="134" y="299" font-family="sans-serif" font-size="24" font-weight="bold" fill="#f4f4f5" text-anchor="middle">4</text>

  <rect x="180" y="264" width="68" height="52" rx="14" fill="url(#btnGrad)" />
  <text x="214" y="299" font-family="sans-serif" font-size="24" font-weight="bold" fill="#f4f4f5" text-anchor="middle">5</text>

  <rect x="260" y="264" width="68" height="52" rx="14" fill="url(#btnGrad)" />
  <text x="294" y="299" font-family="sans-serif" font-size="24" font-weight="bold" fill="#f4f4f5" text-anchor="middle">6</text>

  <rect x="340" y="264" width="72" height="52" rx="14" fill="#3b82f6" />
  <text x="376" y="300" font-family="sans-serif" font-size="28" font-weight="bold" fill="#ffffff" text-anchor="middle">×</text>

  <!-- Row 3 -->
  <rect x="100" y="328" width="68" height="52" rx="14" fill="url(#btnGrad)" />
  <text x="134" y="363" font-family="sans-serif" font-size="24" font-weight="bold" fill="#f4f4f5" text-anchor="middle">1</text>

  <rect x="180" y="328" width="68" height="52" rx="14" fill="url(#btnGrad)" />
  <text x="214" y="363" font-family="sans-serif" font-size="24" font-weight="bold" fill="#f4f4f5" text-anchor="middle">2</text>

  <rect x="260" y="328" width="68" height="52" rx="14" fill="url(#btnGrad)" />
  <text x="294" y="363" font-family="sans-serif" font-size="24" font-weight="bold" fill="#f4f4f5" text-anchor="middle">3</text>

  <rect x="340" y="328" width="72" height="52" rx="14" fill="#6366f1" />
  <text x="376" y="364" font-family="sans-serif" font-size="28" font-weight="bold" fill="#ffffff" text-anchor="middle">=</text>

  <!-- Row 4 (0 & Clear) -->
  <rect x="100" y="392" width="148" height="32" rx="10" fill="url(#btnGrad)" />
  <text x="174" y="415" font-family="sans-serif" font-size="18" font-weight="bold" fill="#f4f4f5" text-anchor="middle">0</text>

  <rect x="260" y="392" width="68" height="32" rx="10" fill="url(#btnGrad)" />
  <text x="294" y="415" font-family="sans-serif" font-size="18" font-weight="bold" fill="#f4f4f5" text-anchor="middle">.</text>

  <rect x="340" y="392" width="72" height="32" rx="10" fill="#ef4444" />
  <text x="376" y="415" font-family="sans-serif" font-size="16" font-weight="bold" fill="#ffffff" text-anchor="middle">AC</text>
</svg>'''
    
    with open(os.path.join(output_dir, "icon.svg"), "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    # 2. Render PNG icons (512x512, 192x192, 180x180, 32x32) using Pillow
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer rounded background with Indigo gradient simulation
    draw.rounded_rectangle([16, 16, 496, 496], radius=108, fill=(99, 102, 241, 255))
    # Inner body
    draw.rounded_rectangle([72, 72, 440, 440], radius=48, fill=(24, 24, 27, 255))
    # Display
    draw.rounded_rectangle([100, 104, 412, 180], radius=20, fill=(39, 39, 42, 255), outline=(63, 63, 70, 255), width=2)
    draw.ellipse([120, 136, 132, 148], fill=(16, 185, 129, 255)) # Green status dot
    
    # Buttons
    btn_color = (46, 46, 51, 255)
    accent_color = (99, 102, 241, 255)
    blue_color = (59, 130, 246, 255)
    red_color = (239, 68, 68, 255)
    
    # Grid 1
    draw.rounded_rectangle([100, 200, 168, 252], radius=14, fill=btn_color)
    draw.rounded_rectangle([180, 200, 248, 252], radius=14, fill=btn_color)
    draw.rounded_rectangle([260, 200, 328, 252], radius=14, fill=btn_color)
    draw.rounded_rectangle([340, 200, 412, 252], radius=14, fill=blue_color)
    
    # Grid 2
    draw.rounded_rectangle([100, 264, 168, 316], radius=14, fill=btn_color)
    draw.rounded_rectangle([180, 264, 248, 316], radius=14, fill=btn_color)
    draw.rounded_rectangle([260, 264, 328, 316], radius=14, fill=btn_color)
    draw.rounded_rectangle([340, 264, 412, 316], radius=14, fill=blue_color)

    # Grid 3
    draw.rounded_rectangle([100, 328, 168, 380], radius=14, fill=btn_color)
    draw.rounded_rectangle([180, 328, 248, 380], radius=14, fill=btn_color)
    draw.rounded_rectangle([260, 328, 328, 380], radius=14, fill=btn_color)
    draw.rounded_rectangle([340, 328, 412, 380], radius=14, fill=accent_color)
    
    # Grid 4
    draw.rounded_rectangle([100, 392, 248, 424], radius=10, fill=btn_color)
    draw.rounded_rectangle([260, 392, 328, 424], radius=10, fill=btn_color)
    draw.rounded_rectangle([340, 392, 412, 424], radius=10, fill=red_color)

    # Save 512x512
    img.save(os.path.join(output_dir, "icon-512.png"), "PNG")
    
    # Save 192x192
    img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
    img_192.save(os.path.join(output_dir, "icon-192.png"), "PNG")

    # Save 180x180 (apple-touch-icon)
    img_180 = img.resize((180, 180), Image.Resampling.LANCZOS)
    img_180.save(os.path.join(output_dir, "apple-touch-icon.png"), "PNG")
    
    # Save 32x32 (favicon)
    img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
    img_32.save(os.path.join(output_dir, "favicon.png"), "PNG")
    
    print("All PWA icons created successfully.")

if __name__ == "__main__":
    generate_icons()
