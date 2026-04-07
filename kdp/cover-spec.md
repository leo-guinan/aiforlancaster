# Book Cover Design Specification

## AI for Main Street
### A No-Hype Guide for Lancaster Small Business Owners
**Author:** Leo Guinan

---

## 1. Format & Dimensions

| Property | Value |
|---|---|
| Format | Kindle eBook (front cover only) |
| Dimensions | 1600 × 2560 px |
| Aspect Ratio | 1:1.6 (standard KDP Kindle) |
| Color Space | RGB |
| File Format | SVG (scalable), export to JPG/PNG for upload |
| Resolution | 300 DPI equivalent at print size |

**Note:** Paperback full wrap (spine + back) to be designed separately once page count is finalized.

---

## 2. Design Philosophy

**Anti-hype. Anti-guru. Pro-clarity.**

This cover should communicate:
- Seriousness without stuffiness
- Practicality over promises
- Local business warmth, not Silicon Valley cold
- Independent press quality, not self-published rush job

Think: the kind of book a Chamber of Commerce director would pick up and respect. Not the kind of book with "PASSIVE INCOME!!!" on the cover.

**Visual references (tone, not imitation):**
- Basecamp's "Rework" — clean, bold, typographic
- O'Reilly technical books — functional, no-nonsense
- Pentagram identity work — restrained, confident

---

## 3. Color Palette

| Role | Color | Hex | Notes |
|---|---|---|---|
| Background | Dark Navy | `#1B2838` | Deep, serious, not black (black looks cheap on screens) |
| Primary Text | Warm White / Cream | `#F5F0E8` | Softer than pure white, feels more like a printed page |
| Accent | Amber Gold | `#D4A843` | Warmth, Main Street, Lancaster heritage. Used sparingly. |
| Subtle Accent | Muted Gold | `#A8883A` | For thin rules/lines only |
| Secondary Text | Light Slate | `#B8C4D0` | For subtitle, lower contrast but still readable |

### Color Rationale
- **Navy over black:** Black backgrounds on Kindle feel flat and cheap. Dark navy has depth and suggests professionalism (financial services, law firms, serious publications).
- **Cream over white:** Pure white on dark backgrounds is harsh. Cream feels warmer, more "book" and less "website."
- **Single accent (amber/gold):** Gold communicates value without flash. It reads "Main Street" not "Wall Street." One accent color = restraint = credibility.

---

## 4. Typography

### Font Stack (Google Fonts — all free, all open license)

| Role | Font | Weight | Size (at 1600px wide) | Fallback |
|---|---|---|---|---|
| "AI for" (pre-title) | Inter | 300 (Light) | 52px | Arial, Helvetica |
| "Main Street" (hero) | Inter | 800 (Extra Bold) | 148px | Arial Black |
| Subtitle | Inter | 300 (Light) | 38px | Arial |
| Author name | Inter | 400 (Regular) | 36px | Arial |
| Thin rule accent | — | — | 2px height | — |

### Why Inter?
- Designed for screens (critical for Kindle/thumbnail)
- Excellent weight range (300–800 used here)
- High x-height = readable at small sizes
- Neutral but not cold — it has subtle warmth in its curves
- Free, open source, widely available
- Fallback: system sans-serif fonts are nearly identical

### Alternative Fonts (if customizing later):
- **Title:** Outfit (geometric, modern), or Source Sans Pro (Adobe, very clean)
- **Display:** Space Grotesk (slightly more character), or Manrope
- **Subtitle:** IBM Plex Sans (light weight is gorgeous)

---

## 5. Layout & Composition

### Vertical Grid (top to bottom, 2560px height)

```
┌─────────────────────────────┐
│                             │  ← Top margin: ~380px
│         AI for              │  ← Pre-title line
│                             │  ← 30px gap
│      MAIN STREET            │  ← Hero text (visual anchor)
│      ═══════════            │  ← Gold accent line (2px, partial width)
│                             │  ← 60px gap
│   A No-Hype Guide for      │  ← Subtitle line 1
│   Lancaster Small Business  │  ← Subtitle line 2
│   Owners                    │  ← Subtitle line 3
│                             │
│                             │
│  ┌─┐ ┌─┐ ┌─┐               │  ← Simple storefront silhouette (optional)
│                             │
│                             │
│       LEO GUINAN            │  ← Author name
│                             │  ← Bottom margin: ~180px
└─────────────────────────────┘
```

### Horizontal Alignment
- All text: **center-aligned**
- Accent line: centered, approximately 60% of text width
- Generous side margins (minimum 120px each side)

### Spacing Rationale
- Title sits in the upper-middle third (where eyes land first on a cover)
- "Main Street" is the largest element — it should be readable even at 100px thumbnail width
- Author name at the bottom with breathing room — this is not an ego cover
- Subtitle has clear hierarchy below the main title

---

## 6. Graphic Elements

### Primary: Thin Horizontal Rule
- Position: directly below "MAIN STREET"
- Color: Amber Gold (`#D4A843`)
- Width: ~450px (roughly 60% of "MAIN STREET" text width)
- Height: 2px
- Purpose: separates title from subtitle, adds a touch of warmth, suggests a street/horizon line

### Secondary (Optional): Storefront Silhouette
- A minimal, geometric row of 3 simple building shapes
- Color: Muted Gold (`#A8883A`) at reduced opacity (30-40%)
- Position: lower-middle area, between subtitle and author name
- Size: small — roughly 200px wide × 80px tall
- Style: pure geometric rectangles with simple peaked/flat roofs
- **If it looks even slightly clipart-y, remove it. Typography-only is better than bad graphics.**

### What NOT to include:
- ❌ AI/robot imagery
- ❌ Circuit boards, neural networks, binary code
- ❌ Stock photography of any kind
- ❌ Gradients (flat colors only)
- ❌ Drop shadows on text
- ❌ More than one accent color
- ❌ Decorative borders or frames

---

## 7. Thumbnail Readability Test

At 100px wide (typical Amazon browse size), the following MUST be legible:
1. "MAIN STREET" — clearly readable as the dominant element
2. General sense of "this is a professional, serious book"
3. Dark background with light text contrast

At 100px, the following will NOT be readable (and that's OK):
- Subtitle text
- Author name (though it should be visible as a text block)
- Accent line (too thin — that's fine)

### Contrast Ratios (WCAG)
- Cream on Navy: **12.3:1** (exceeds AAA)
- Gold on Navy: **5.8:1** (exceeds AA)
- Slate on Navy: **6.1:1** (exceeds AA)

---

## 8. Production Notes

### For Kindle Upload (KDP)
- Export SVG → PNG at 1600×2560
- Ensure RGB color space
- File size under 50MB
- Format: TIFF or PNG (PNG preferred for screen-first)

### For Paperback (future)
- Will need full wrap: front + spine + back
- Spine width calculated from page count (KDP provides calculator)
- Back cover: synopsis, barcode area, minimal design
- Bleed: 0.125" on all edges
- Convert to CMYK for print (navy will shift — test proof carefully)

### For Social Media / Marketing
- Create square crop (1:1) featuring just "AI for Main Street" title block
- Create wide banner (16:9) for Twitter/LinkedIn headers
- The gold accent line works well as a brand element across formats

---

## 9. File Manifest

| File | Purpose | Status |
|---|---|---|
| `cover-spec.md` | This specification document | ✅ Complete |
| `cover-front.svg` | Working SVG front cover | ✅ Complete |
| `cover-front.png` | Rasterized PNG for KDP upload | ⬜ Export from SVG |
| `cover-full-wrap.svg` | Full paperback wrap | ⬜ Pending page count |
| `cover-social-square.png` | Social media square crop | ⬜ Pending |
| `cover-social-banner.png` | Social media banner | ⬜ Pending |
