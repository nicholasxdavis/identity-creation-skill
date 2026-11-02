#!/usr/bin/env python3
"""Remove a solid background, trim, center, and size an IP logo PNG."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


def nearest_bg_color(img: Image.Image, sample: int = 12) -> tuple[int, int, int]:
    """Estimate background from corner samples (mode of RGB triples)."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    points = [
        (0, 0),
        (w - 1, 0),
        (0, h - 1),
        (w - 1, h - 1),
        (sample, sample),
        (w - 1 - sample, sample),
        (sample, h - 1 - sample),
        (w - 1 - sample, h - 1 - sample),
    ]
    counts: dict[tuple[int, int, int], int] = {}
    for x, y in points:
        color = rgb.getpixel((max(0, min(w - 1, x)), max(0, min(h - 1, y))))
        counts[color] = counts.get(color, 0) + 1
    return max(counts, key=counts.get)


def color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def knock_out_background(
    img: Image.Image,
    bg: tuple[int, int, int],
    tolerance: float,
    feather: float,
) -> Image.Image:
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            dist = color_distance((r, g, b), bg)
            if dist <= tolerance:
                pixels[x, y] = (r, g, b, 0)
            elif dist < tolerance + feather and feather > 0:
                t = (dist - tolerance) / feather
                pixels[x, y] = (r, g, b, max(0, min(255, int(a * t))))
    return rgba


def content_bbox(img: Image.Image, alpha_threshold: int = 8) -> tuple[int, int, int, int]:
    alpha = img.split()[-1]
    mask = alpha.point(lambda p: 255 if p > alpha_threshold else 0)
    bbox = mask.getbbox()
    if not bbox:
        raise ValueError("No opaque content found after background removal")
    return bbox


def fit_centered(
    img: Image.Image,
    size: int,
    fill_ratio: float,
) -> Image.Image:
    """Place subject centered on a transparent square canvas."""
    bbox = content_bbox(img)
    subject = img.crop(bbox)
    sw, sh = subject.size
    target = max(1, int(size * fill_ratio))
    scale = min(target / sw, target / sh)
    new_w = max(1, int(sw * scale))
    new_h = max(1, int(sh * scale))
    subject = subject.resize((new_w, new_h), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ox = (size - new_w) // 2
    oy = (size - new_h) // 2
    canvas.paste(subject, (ox, oy), subject)
    return canvas


def process(
    input_path: Path,
    output_path: Path,
    size: int,
    fill_ratio: float,
    tolerance: float,
    feather: float,
    bg: tuple[int, int, int] | None,
) -> None:
    src = Image.open(input_path)
    bg_color = bg or nearest_bg_color(src)
    keyed = knock_out_background(src, bg_color, tolerance=tolerance, feather=feather)
    final = fit_centered(keyed, size=size, fill_ratio=fill_ratio)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(output_path, "PNG", optimize=True)
    print(f"bg≈{bg_color} → {output_path} ({size}×{size}, fill≈{fill_ratio:.0%})")


def parse_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("Expected RRGGBB or #RRGGBB")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source PNG with solid background")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output transparent PNG (default: <stem>-transparent.png)",
    )
    parser.add_argument("--size", type=int, default=1024, help="Output square size")
    parser.add_argument(
        "--fill",
        type=float,
        default=0.82,
        help="Subject fill ratio of the canvas (0.70-0.90 recommended)",
    )
    parser.add_argument("--tolerance", type=float, default=28.0, help="BG key tolerance")
    parser.add_argument("--feather", type=float, default=8.0, help="Edge feather width")
    parser.add_argument(
        "--bg",
        type=parse_rgb,
        default=None,
        help="Force background hex to remove (e.g. #E8EEF5)",
    )
    args = parser.parse_args()

    if not 0.5 <= args.fill <= 0.95:
        print("error: --fill must be between 0.5 and 0.95", file=sys.stderr)
        return 2

    out = args.output or args.input.with_name(f"{args.input.stem}-transparent.png")
    try:
        process(
            args.input,
            out,
            size=args.size,
            fill_ratio=args.fill,
            tolerance=args.tolerance,
            feather=args.feather,
            bg=args.bg,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
