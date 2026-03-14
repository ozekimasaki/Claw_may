#!/usr/bin/env python3
"""
Export Mei-chan pixel art to PNG
"""

import json
from pathlib import Path
from PIL import Image

def export_to_png():
    # Load JSON
    json_path = Path(__file__).parent / 'mei-chan.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    canvas = data['canvas']
    width = data['width']
    height = data['height']
    colors = data['colors']
    
    # Create image (scale up for visibility)
    scale = 8  # 8x scale
    img = Image.new('RGBA', (width * scale, height * scale), (0, 0, 0, 0))
    
    # Draw pixels
    for y in range(height):
        for x in range(width):
            color_idx = canvas[y][x]
            if color_idx < len(colors):
                r, g, b = colors[color_idx]
                # Skip black (background)
                if color_idx == 0:
                    continue
                for py in range(scale):
                    for px in range(scale):
                        img.putpixel((x * scale + px, y * scale + py), (r, g, b, 255))
    
    # Save PNG
    output_path = Path(__file__).parent / 'mei-chan.png'
    img.save(output_path, 'PNG')
    
    print(f"✅ PNG を保存しました！")
    print(f"   📁 {output_path}")
    print(f"   📐 サイズ：{width * scale}x{height * scale} (原寸：{width}x{height})")
    print(f"   🔍 スケール：{scale}x")
    
    # Also create a smaller version (2x scale)
    scale_small = 2
    img_small = Image.new('RGBA', (width * scale_small, height * scale_small), (0, 0, 0, 0))
    for y in range(height):
        for x in range(width):
            color_idx = canvas[y][x]
            if color_idx < len(colors) and color_idx != 0:
                r, g, b = colors[color_idx]
                for py in range(scale_small):
                    for px in range(scale_small):
                        img_small.putpixel((x * scale_small + px, y * scale_small + py), (r, g, b, 255))
    
    output_small = Path(__file__).parent / 'mei-chan-small.png'
    img_small.save(output_small, 'PNG')
    print(f"\n✅ 小さいバージョンも保存しました！")
    print(f"   📁 {output_small}")
    print(f"   📐 サイズ：{width * scale_small}x{height * scale_small}")


if __name__ == '__main__':
    export_to_png()
