#!/usr/bin/env python3
"""
Generate Idea Dining Club pixel art icon (64x64, 16-color palette).
Retro RPG inventory style — two plates sharing a central dish.
"""
from PIL import Image, ImageDraw

PALETTE = {
    0: (15, 15, 26),    # bg dark blue-black
    1: (26, 26, 46),    # dark blue (shadows)
    2: (58, 59, 89),    # mid blue-gray
    3: (90, 90, 120),   # light blue-gray
    4: (201, 162, 39),  # gold (premium/plates)
    5: (255, 215, 0),   # bright gold (food/idea)
    6: (139, 90, 43),   # brown (wood table)
    7: (200, 160, 100), # light wood
    8: (74, 124, 89),   # green accent
    9: (90, 148, 112),  # light green
    10: (255, 200, 150),# skin tone
    11: (50, 60, 100),  # dark blue
    12: (120, 120, 140),# gray
    13: (160, 130, 80), # bronze
    14: (220, 220, 220),# white
    15: (15, 15, 26),   # transparent → bg
}

def main():
    img = Image.new('RGB', (64, 64), PALETTE[0])
    draw = ImageDraw.Draw(img)

    # === TABLE / SURFACE ===
    # Horizontal wooden planks at y=44-52
    table_y0, table_h = 44, 10
    for y in range(table_y0, table_y0 + table_h):
        for x in range(0, 64):
            plank = (x // 16) % 2
            draw.point((x, y), PALETTE[7 if plank else 6])
    
    # Table edge (top)
    for x in range(0, 64):
        draw.point((x, table_y0 - 1), PALETTE[6])
    
    # === TWO PLATES (circular-ish, pixelated) ===
    # Left plate — circle-ish around center-left
    left_plate_center = (24, 36)
    right_plate_center = (40, 36)
    plate_radius = 6
    
    def draw_plate(cx, cy):
        # Plate rim — bright gold
        for dy in range(-plate_radius, plate_radius + 1):
            width = int((plate_radius**2 - dy**2)**0.5)
            for dx in range(-width, width + 1):
                draw.point((cx + dx, cy + dy), PALETTE[4])
        # Inner — off-white
        inner_r = plate_radius - 2
        for dy in range(-inner_r, inner_r + 1):
            width = int((inner_r**2 - dy**2)**0.5)
            for dx in range(-width, width + 1):
                draw.point((cx + dx, cy + dy), PALETTE[14])
    
    draw_plate(*left_plate_center)
    draw_plate(*right_plate_center)
    
    # === CENTRAL DISH (shared between plates, above table) ===
    # Small bowl/vase with "idea" (lightbulb-ish or swirl)
    bowl_x, bowl_y = 32, 30
    # Bowl body — gold vase shape
    bowl_pixels = []
    for dy in range(-2, 2):
        for dx in range(-2, 2):
            if abs(dx) + abs(dy) <= 2:
                bowl_pixels.append((bowl_x + dx, bowl_y + dy))
    bowl_pixels.extend([
        (bowl_x - 1, bowl_y + 2), (bowl_x + 1, bowl_y + 2),
        (bowl_x - 2, bowl_y + 3), (bowl_x + 2, bowl_y + 3),
    ])
    for px, py in bowl_pixels:
        draw.point((px, py), PALETTE[5])
    
    # Idea spark — a small star/burst emanating upward
    spark_center = (bowl_x, bowl_y - 3)
    spark_offsets = [(0,-1), (-1,0), (1,0), (0,-2), (-1,-1), (1,-1)]
    for dx, dy in spark_offsets:
        draw.point((spark_center[0] + dx, spark_center[1] + dy), PALETTE[5])
    
    # === FRAME BORDER (double-line) ===
    border_color = PALETTE[4]
    for x in range(0, 64):
        draw.point((x, 0), border_color)
        draw.point((x, 63), border_color)
    for y in range(0, 64):
        draw.point((0, y), border_color)
        draw.point((63, y), border_color)
    # Inner highlight
    for x in range(2, 62):
        draw.point((x, 1), PALETTE[5])
        draw.point((x, 62), PALETTE[5])
    for y in range(2, 62):
        draw.point((1, y), PALETTE[5])
        draw.point((62, y), PALETTE[5])

    img.save('/Users/leoguinan/clawd/local-ai-business/landing-page/icons/dining-icon.png')
    print("Saved dining-icon.png (64x64)")

if __name__ == "__main__":
    main()
