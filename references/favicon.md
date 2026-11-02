# Favicon lane

Create clean, iconic, highly simplified square favicons that are perfectly centered, readable at tiny sizes, and exported as transparent multi-size assets.

## Workflow

1. **Brand & Name Evaluation**: Parse the brand name, product context, or existing concept. Prefer README, landing copy, design tokens, and identity-creation mascot outputs when available.
2. **Concept Selection**: Pick a single hyper-recognizable focal symbol (simplified mascot face, silhouette, monogram, or emblem) that stays legible at `16×16` and `32×32`.
3. **Image Generation**: Generate a full-resolution `1:1` square with the subject strictly centered on a **solid** high-contrast background (e.g. `#00FF00` or a flat brand field) for clean keying.
4. **Python Post-Processing**: Run [../scripts/make_favicon.py](../scripts/make_favicon.py) to:
   - Remove the solid background → true PNG transparency
   - Trim excess padding and re-center
   - Export `favicon.ico` (16/32/48), `favicon-16x16.png`, `favicon-32x32.png`, `favicon-master.png`, and `apple-touch-icon.png` (180×180)
5. **Delivery**: Report the concept rationale, show the final icon, and list output paths plus HTML head snippet.

## Complexity & Scale Budget

- Must stay legible at `16×16` and `32×32`.
- Exactly one central shape / emblem / face.
- Omit thin lines, fine textures, small facial detail, and text.
- High contrast against both light and dark browser chrome.

## Shape Language & Centering

- Strictly centered horizontally and vertically.
- ~10-15% margin on each side (subject fills ~80-85%).
- Bold, rounded, weighty contours and broad color blocks.
- Upright orientation unless a tilt is intrinsic to the mark.

## Prompt Skeleton

```text
Create one complete full-bleed 1:1 square icon asset.
Background: fill the entire square canvas with a solid uniform background color [e.g., bright green #00FF00 or solid white].
Subject: place one hyper-simplified, bold, ultra-recognizable <subject> emblem/character face directly in the exact center of the frame.
Complexity: use minimal basic geometric shapes and broad continuous color regions. Ensure strong visual clarity at extreme small scale (16x16 pixels). Remove all fine lines, small details, textures, outlines, and extra text.
Composition: keep the subject perfectly centered both horizontally and vertically, filling approximately 80-85% of the frame with balanced margins around all sides.
Style: clean graphic mark, thick soft rounded contours, high-contrast visual balance, subtle dimensional depth.
Constraints: No text, no extra background scenery, no shadows casting off the canvas, no borders or frames, and no off-center compositions.
```

## Python Production

```bash
python scripts/make_favicon.py <source.png> -d favicon-out --fill 0.82
```

Useful flags:
- `--bg RRGGBB`: force key color when auto-detect fails
- `--tolerance` / `--feather`: tighten or soften the key
- `--master-size 512`: transparent master resolution

## HTML Snippet

```html
<link rel="icon" href="/favicon.ico" sizes="any" />
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
```

## Done Checklist

- [ ] Concept matches the product / brand
- [ ] Subject centered with balanced margins
- [ ] Readable when previewed at 16×16 and 32×32
- [ ] Transparent exports written via the script
- [ ] HTML head snippet provided
