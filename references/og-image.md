# OG image lane

Generate brand-aligned `1200×630` Open Graph preview images for high-value pages. Combine IP/visual assets, sharp typography, and programmatic Pillow compositing.

## Workflow

1. **Page & Context Analysis**: Inspect the target page URL, metadata, value proposition, and visual identity (brand colors, IP mascot, value drivers).
2. **Layout Selection**:
   - **Split Pane (IP + UI)**: Character/key visual on one side; headline + badge on the other.
   - **Feature / Product Showcase**: Centered UI preview with branding accents.
   - **Bold Editorial / Minimal**: Massive headline, high-contrast background, brand badge.
3. **Asset Generation / Retrieval**: Generate or collect focal visuals (IP, gradient plate, UI frame). Keep critical content inside the safe zone.
4. **Python Compositing**: Run [../scripts/create_og_image.py](../scripts/create_og_image.py) to assemble text, badge, brand, and optional mascot onto the plate. Export exactly `1200 × 630` PNG.
5. **Delivery**: Return the image path, layout used, and ready-to-paste `<meta>` tags.

## Technical Specs & Safe Zones

- **Resolution**: `1200 × 630` (≈1.91:1).
- **Safe Zone**: Keep critical content inside `1080 × 510` (60px inner margin) for X/LinkedIn/Facebook crops.
- **Palette**: Prefer rich dark plates (`#0D0F12`, `#0B132B`, `#121212`) with high-contrast text and brand accents, or match the product tokens.
- **Typography**:
  - Badge: 18-24px, uppercase, bold
  - Headline: 54-72px, max 2-3 lines
  - Subhead: 24-32px, max 2 lines

## Layout Configurations

### Option A: Split Pane (IP + Headline)
- Left (~55%): badge, headline, subhead, brand
- Right (~45%): centered IP / product visual

### Option B: Centered Hyper-Frame UI
- Top (~25%): branding + headline
- Bottom (~75%): floating app/device frame cropped at the lower edge

## Generation Prompt Skeleton (background plate)

```text
Create one full-bleed 1200x630 horizontal digital banner image designed specifically for an Open Graph social preview card.
Background: premium dark-mode background <color e.g., #0B0F19> with subtle radial gradient lighting and soft ambient glow accents.
Subject: on the right half, place a high-contrast, simplified <subject or product asset> framed in a clean rounded card container. Left half remains clean and spacious for programmatic text overlay.
Composition: strict 1.91:1 widescreen horizontal aspect ratio (1200x630). Keep 60px padding safe zones along all borders. Balanced, modern, high-converting tech landing page style.
Style: ultra-clean vector and 3D hybrid look, soft subtle shadows, zero noise, high legibility.
Constraints: No flat text overlays in the generator background, no ugly borders, no thin line noise, no watermarks.
```

Leave headline/badge text for the Python compositor. Do not bake primary copy into the generated plate unless the user asks.

## Python Compositing

```bash
python scripts/create_og_image.py \
  --title "Transform Your Workflow in Seconds" \
  --subtitle "The AI toolkit for high-performing teams." \
  --badge "PRODUCT UPDATE" \
  --brand "example.com" \
  --background plate.png \
  --mascot mascot-transparent.png \
  -o og-image.png
```

Without `--background`, the script uses a solid dark plate. Without `--mascot`, it renders text-only.

## Integration Metadata

```html
<!-- Open Graph -->
<meta property="og:type" content="website" />
<meta property="og:url" content="https://yourdomain.com/page" />
<meta property="og:title" content="Page Title - Product Name" />
<meta property="og:description" content="Concise value proposition." />
<meta property="og:image" content="https://yourdomain.com/assets/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Page Title - Product Name" />
<meta name="twitter:description" content="Concise value proposition." />
<meta name="twitter:image" content="https://yourdomain.com/assets/og-image.png" />
```

## Done Checklist

- [ ] Exact `1200×630` PNG produced
- [ ] Critical content inside the 60px safe zone
- [ ] Headline ≤ 3 lines, subhead ≤ 2 lines
- [ ] Brand / IP colors respected
- [ ] Meta tag snippet delivered with the file path
