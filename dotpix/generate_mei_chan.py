#!/usr/bin/env python3
"""
Generate Mei-chan pixel art (64x64)
Automatically creates a dot pixel art of Mei-chan
"""

import json
from pathlib import Path

def create_mei_chan():
    width, height = 64, 64
    
    # Color palette
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    GRAY = 8
    ORANGE = 9
    BROWN = 10  # 栗色 (hair)
    PINK = 11   # 肌色 (skin)
    
    # Initialize canvas
    canvas = [[BLACK for _ in range(width)] for _ in range(height)]
    
    # Helper function to draw filled circle
    def fill_circle(cx, cy, radius, color):
        for y in range(height):
            for x in range(width):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                    canvas[y][x] = color
    
    # Helper function to draw ellipse
    def fill_ellipse(cx, cy, rx, ry, color):
        for y in range(height):
            for x in range(width):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    canvas[y][x] = color
    
    # Helper function to draw rectangle
    def fill_rect(x1, y1, x2, y2, color):
        for y in range(max(0, y1), min(height, y2)):
            for x in range(max(0, x1), min(width, x2)):
                canvas[y][x] = color
    
    # 1. Background (transparent/black)
    # Already black
    
    # 2. Body (white dress)
    fill_ellipse(32, 50, 14, 12, WHITE)
    fill_rect(24, 42, 40, 52, WHITE)
    
    # 3. Neck
    fill_rect(28, 38, 36, 44, PINK)
    
    # 4. Head (skin color)
    fill_ellipse(32, 28, 14, 12, PINK)
    
    # 5. Hair (brown/chestnut) - Main part
    fill_ellipse(32, 24, 16, 14, BROWN)
    
    # Hair - Bangs (front)
    for x in range(22, 42):
        for y in range(18, 28):
            if (x - 32) ** 2 + (y - 28) ** 2 > 100:  # Outer part
                canvas[y][x] = BROWN
    
    # Hair - Sides (bob cut)
    for y in range(26, 42):
        # Left side
        for x in range(16, 24):
            if y > 28 + (x - 16):
                canvas[y][x] = BROWN
        # Right side
        for x in range(40, 48):
            if y > 28 + (48 - x):
                canvas[y][x] = BROWN
    
    # Hair - Top
    fill_ellipse(32, 16, 14, 6, BROWN)
    
    # 6. Eyes (green)
    # Left eye
    fill_ellipse(27, 27, 3, 2, GREEN)
    # Right eye
    fill_ellipse(37, 27, 3, 2, GREEN)
    
    # Eye pupils (black)
    canvas[27][27] = BLACK
    canvas[27][37] = BLACK
    
    # Eye highlights (white)
    canvas[26][26] = WHITE
    canvas[26][36] = WHITE
    
    # 7. Eyebrows (brown)
    for x in range(24, 30):
        canvas[24][x] = BROWN
    for x in range(34, 40):
        canvas[24][x] = BROWN
    
    # 8. Mouth (small smile)
    canvas[33][30] = RED
    canvas[33][31] = RED
    canvas[33][32] = RED
    canvas[33][33] = RED
    canvas[34][31] = RED
    canvas[34][32] = RED
    
    # 9. Blush (pink)
    canvas[30][23] = PINK
    canvas[30][24] = PINK
    canvas[30][40] = PINK
    canvas[30][41] = PINK
    
    # 10. Blue ribbon (on chest)
    # Bow parts
    fill_ellipse(27, 43, 4, 3, BLUE)
    fill_ellipse(37, 43, 4, 3, BLUE)
    # Center knot
    fill_rect(30, 42, 34, 46, BLUE)
    # Ribbon tails
    canvas[46][28] = BLUE
    canvas[47][28] = BLUE
    canvas[48][29] = BLUE
    canvas[46][36] = BLUE
    canvas[47][36] = BLUE
    canvas[48][35] = BLUE
    
    # 11. Golden bell (center of ribbon)
    canvas[44][31] = YELLOW
    canvas[44][32] = YELLOW
    canvas[45][31] = YELLOW
    canvas[45][32] = YELLOW
    canvas[46][31] = YELLOW
    canvas[46][32] = YELLOW
    # Bell highlight
    canvas[44][31] = WHITE
    
    # 12. Hair highlight (ahoge/antenna hair)
    canvas[14][30] = BROWN
    canvas[13][31] = BROWN
    canvas[12][32] = BROWN
    canvas[13][32] = BROWN
    
    # 13. Shoulders
    fill_ellipse(20, 48, 4, 3, PINK)
    fill_ellipse(44, 48, 4, 3, PINK)
    
    # 14. Dress details (collar)
    fill_rect(26, 40, 38, 43, WHITE)
    
    # 15. Add some shading to hair
    for y in range(36, 42):
        for x in range(18, 24):
            if canvas[y][x] == BROWN:
                canvas[y][x] = GRAY  # Shadow
        for x in range(40, 46):
            if canvas[y][x] == BROWN:
                canvas[y][x] = GRAY  # Shadow
    
    return canvas, width, height


def save_mei_chan():
    canvas, width, height = create_mei_chan()
    
    # Color definitions
    colors = [
        (0, 0, 0),      # 0: Black
        (128, 0, 0),    # 1: Red
        (0, 128, 0),    # 2: Green
        (128, 128, 0),  # 3: Yellow
        (0, 0, 128),    # 4: Blue
        (128, 0, 128),  # 5: Magenta
        (0, 128, 128),  # 6: Cyan
        (192, 192, 192),# 7: White
        (128, 128, 128),# 8: Gray
        (255, 128, 0),  # 9: Orange
        (139, 69, 19),  # 10: Brown (chestnut)
        (255, 218, 185),# 11: Pink (skin)
    ]
    
    data = {
        'name': 'Mei-chan',
        'description': 'AI メイドのメイ - 栗色のショートボブ、緑の瞳、青いリボンと金色のベル',
        'width': width,
        'height': height,
        'canvas': canvas,
        'colors': colors
    }
    
    output_path = Path(__file__).parent / 'mei-chan.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ めいちゃんのドット絵を保存しました！")
    print(f"   📁 {output_path}")
    print(f"   📐 サイズ：{width}x{height}")
    print(f"\n🎨 色パレット:")
    print(f"   栗色 (髪)，肌色 (顔)，緑 (瞳)，青 (リボン)，黄 (ベル)，白 (服)")
    print(f"\n💡 使い方:")
    print(f"   python dotpix.py -w 64 -H 64")
    print(f"   L キーで mei-chan.json を読み込んでください")
    
    # Also create a simple ASCII preview
    print(f"\n📊 プレビュー (縮小):")
    preview_size = 32
    scale = width // preview_size
    print("+" + "-" * (preview_size + 2) + "+")
    for y in range(0, height, scale):
        line = "|"
        for x in range(0, width, scale):
            color_idx = canvas[y][x]
            if color_idx == 0:
                line += " "
            elif color_idx == 7:  # White
                line += "░"
            elif color_idx == 10:  # Brown
                line += "▓"
            elif color_idx == 11:  # Pink
                line += "▒"
            elif color_idx == 4:  # Blue
                line += "█"
            elif color_idx == 3:  # Yellow
                line += "●"
            elif color_idx == 2:  # Green
                line += "◉"
            else:
                line += "·"
        line += "|"
        print(line)
    print("+" + "-" * (preview_size + 2) + "+")


if __name__ == '__main__':
    save_mei_chan()
