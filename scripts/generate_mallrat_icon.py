#!/usr/bin/env python3
"""
Generate Mallrat pixel art icon (64x64, 16-color palette).
Retro RPG inventory style.
"""
from PIL import Image, ImageDraw

# 16-color palette (RGB tuples) — muted, earthy with gold accent
PALETTE = {
    0: (15, 15, 26),    # bg dark blue-black
    1: (26, 26, 46),    # dark blue (shadows)
    2: (58, 59, 89),    # mid blue-gray
    3: (90, 90, 120),   # light blue-gray
    4: (74, 124, 89),   # forest green (rat body)
    5: (90, 148, 112),  # light green (rat highlight)
    6: (201, 162, 39),  # gold (glow/display)
    7: (255, 215, 0),   # bright gold (center glow)
    8: (139, 90, 43),   # brown (wood/display case)
    9: (200, 160, 100), # light brown
    10: (255, 200, 150),# skin/paper tone
    11: (50, 60, 100),  # dark blue accent
    12: (100, 100, 150), # light purple accent
    13: (120, 120, 120), # gray
    14: (200, 200, 200), # light gray
    15: (15, 15, 26),   # transparent → bg
}

def put_pixel(draw, x, y, color_idx, scale=1):
    for dx in range(scale):
        for dy in range(scale):
            draw.point((x*scale + dx, y*scale + dy), PALETTE[color_idx])

def main():
    img = Image.new('RGB', (64, 64), PALETTE[0])
    draw = ImageDraw.Draw(img)

    # Draw in 1x1 pixel grid (no scale), then let viewer scale
    # Using direct pixel placement for perfect control
    
    # === DISPLAY CASE (bottom third) ===
    # Case outline — 20x14 pixels, centered at y=40-54
    case_x0, case_y0, case_w, case_h = 22, 38, 20, 18
    for x in range(case_x0, case_x0 + case_w):
        draw.point((x, case_y0), PALETTE[8])      # top edge
        draw.point((x, case_y0 + case_h - 1), PALETTE[8])  # bottom edge
    for y in range(case_y0, case_y0 + case_h):
        draw.point((case_x0, y), PALETTE[8])      # left edge
        draw.point((case_x0 + case_w - 1, y), PALETTE[8])  # right edge
    # Fill glass with dark blue
    for x in range(case_x0 + 1, case_x0 + case_w - 1):
        for y in range(case_y0 + 1, case_y0 + case_h - 1):
            draw.point((x, y), PALETTE[2])
    
    # === GLOWING OBJECT INSIDE (scroll/gem) ===
    # Center of case: x=32, y=47
    glow_center = (32, 47)
    # Core — bright gold
    draw.point(glow_center, PALETTE[7])
    # Cross shape
    for offset in [-1, 0, 1]:
        draw.point((glow_center[0] + offset, glow_center[1]), PALETTE[6])
        draw.point((glow_center[0], glow_center[1] + offset), PALETTE[6])
    # Diamond ring
    ring = [(30,47), (31,46), (33,46), (34,47), (33,48), (31,48)]
    for px, py in ring:
        draw.point((px, py), PALETTE[6])
    
    # === MALLRAT — small creature peering from left ===
    # Body: 8x5 pixel blob at (14, 46)
    rat_pixels = [
        (14,46), (15,46), (16,46),
        (14,47), (15,47), (16,47),
        (14,48), (15,48), (16,48),
        (14,49), (15,49),
        (15,50)  # tail tip
    ]
    for px, py in rat_pixels:
        draw.point((px, py), PALETTE[4])
    # Ear
    draw.point((14, 45), PALETTE[5])
    # Eye
    draw.point((16, 46), PALETTE[7])
    # Nose
    draw.point((17, 48), PALETTE[10])
    
    # === MALL FLOOR/TILES ===
    # Bottom band — floor tiles
    for y in range(56, 64):
        for x in range(0, 64):
            tile = ((x // 8) + (y // 8)) % 2
            draw.point((x, y), PALETTE[2 if tile else 1])
    
    # === FRAME BORDER (pixel double-line) ===
    border_color = PALETTE[6]
    for x in range(0, 64):
        draw.point((x, 0), border_color)
        draw.point((x, 63), border_color)
    for y in range(0, 64):
        draw.point((0, y), border_color)
        draw.point((63, y), border_color)
    # Inner line
    for x in range(2, 62):
        draw.point((x, 1), PALETTE[3])
        draw.point((x, 62), PALETTE[3])
    for y in range(2, 62):
        draw.point((1, y), PALETTE[3])
        draw.point((62, y), PALETTE[3])

    img.save('/Users/leoguinan/clawd/local-ai-business/landing-page/icons/mallrat-icon.png')
    print("Saved mallrat-icon.png (64x64)")

if __name__ == "__main__":
    main()
