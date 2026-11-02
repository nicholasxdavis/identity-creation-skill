#!/usr/bin/env python3
"""Composite a 1200×630 Open Graph image with headline, badge, and optional mascot."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1200, 630
SAFE_MARGIN = 60


def load_font(candidates: list[str], size: int) -> ImageFont.ImageFont:
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        test = " ".join(current + [word])
        bbox = font.getbbox(test)
        if (bbox[2] - bbox[0]) <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def create_og_image(
    output_path: Path,
    title: str,
    subtitle: str,
    badge_text: str,
    brand_name: str,
    background_path: Path | None = None,
    mascot_path: Path | None = None,
    bg_color: tuple[int, int, int] = (11, 15, 25),
    accent: tuple[int, int, int, int] = (99, 102, 241, 60),
    accent_border: tuple[int, int, int, int] = (129, 140, 248, 180),
) -> Path:
    if background_path and background_path.exists():
        base = Image.open(background_path).convert("RGBA").resize(
            (WIDTH, HEIGHT), Image.Resampling.LANCZOS
        )
    else:
        base = Image.new("RGBA", (WIDTH, HEIGHT), (*bg_color, 255))

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    if mascot_path and mascot_path.exists():
        mascot = Image.open(mascot_path).convert("RGBA")
        mascot.thumbnail((480, 480), Image.Resampling.LANCZOS)
        mw, mh = mascot.size
        pos_x = WIDTH - SAFE_MARGIN - mw
        pos_y = (HEIGHT - mh) // 2
        overlay.paste(mascot, (pos_x, pos_y), mascot)

    font_candidates = [
        "Inter-Bold.ttf",
        "Geist-Bold.ttf",
        "PlusJakartaSans-Bold.ttf",
        "arialbd.ttf",
        "Arial Bold.ttf",
        "DejaVuSans-Bold.ttf",
    ]
    font_regular_candidates = [
        "Inter-Regular.ttf",
        "Geist-Regular.ttf",
        "PlusJakartaSans-Regular.ttf",
        "arial.ttf",
        "Arial.ttf",
        "DejaVuSans.ttf",
    ]

    font_badge = load_font(font_candidates, 20)
    font_title = load_font(font_candidates, 56)
    font_sub = load_font(font_regular_candidates, 26)
    font_brand = load_font(font_candidates, 22)

    curr_y = SAFE_MARGIN + 20
    badge = badge_text.upper()
    pad_x, pad_y = 12, 6
    bb = font_badge.getbbox(badge)
    badge_w = (bb[2] - bb[0]) + pad_x * 2
    badge_h = (bb[3] - bb[1]) + pad_y * 2

    draw.rounded_rectangle(
        [SAFE_MARGIN, curr_y, SAFE_MARGIN + badge_w, curr_y + badge_h],
        radius=12,
        fill=accent,
        outline=accent_border,
        width=1,
    )
    draw.text(
        (SAFE_MARGIN + pad_x, curr_y + pad_y - 2),
        badge,
        font=font_badge,
        fill=(199, 210, 254, 255),
    )
    curr_y += badge_h + 30

    for line in wrap_text(title, font_title, 620)[:3]:
        draw.text((SAFE_MARGIN, curr_y), line, font=font_title, fill=(255, 255, 255, 255))
        curr_y += 68

    curr_y += 10
    for line in wrap_text(subtitle, font_sub, 620)[:2]:
        draw.text((SAFE_MARGIN, curr_y), line, font=font_sub, fill=(156, 163, 175, 255))
        curr_y += 34

    draw.text(
        (SAFE_MARGIN, HEIGHT - SAFE_MARGIN - 24),
        brand_name,
        font=font_brand,
        fill=(243, 244, 246, 255),
    )

    final_img = Image.alpha_composite(base, overlay).convert("RGB")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_img.save(output_path, "PNG", optimize=True)
    print(f"wrote {output_path} ({WIDTH}×{HEIGHT})")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", type=Path, default=Path("og-image.png"))
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--badge", default="PRODUCT")
    parser.add_argument("--brand", required=True)
    parser.add_argument("--background", type=Path, default=None)
    parser.add_argument("--mascot", type=Path, default=None)
    args = parser.parse_args()

    create_og_image(
        output_path=args.output,
        title=args.title,
        subtitle=args.subtitle,
        badge_text=args.badge,
        brand_name=args.brand,
        background_path=args.background,
        mascot_path=args.mascot,
    )


if __name__ == "__main__":
    main()
