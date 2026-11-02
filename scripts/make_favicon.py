#!/usr/bin/env python3
"""Knock out a solid background, center, and export favicon sizes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


SIZES_ICO = [(16, 16), (32, 32), (48, 48)]
APPLE_TOUCH = 180


def nearest_bg_color(img: Image.Image, sample: int = 10) -> tuple[int, int, int]:
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


def fit_centered(img: Image.Image, size: int, fill_ratio: float) -> Image.Image:
    bbox = content_bbox(img)
    subject = img.crop(bbox)
    sw, sh = subject.size
    target = max(1, int(size * fill_ratio))
    scale = min(target / sw, target / sh)
    new_w = max(1, int(sw * scale))
    new_h = max(1, int(sh * scale))
    subject = subject.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(subject, ((size - new_w) // 2, (size - new_h) // 2), subject)
    return canvas


def parse_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("Expected RRGGBB or #RRGGBB")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def process(
    input_path: Path,
    out_dir: Path,
    fill_ratio: float,
    tolerance: float,
    feather: float,
    bg: tuple[int, int, int] | None,
    master_size: int,
) -> dict[str, Path]:
    src = Image.open(input_path)
    bg_color = bg or nearest_bg_color(src)
    keyed = knock_out_background(src, bg_color, tolerance=tolerance, feather=feather)
    master = fit_centered(keyed, size=master_size, fill_ratio=fill_ratio)

    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, Path] = {}

    master_path = out_dir / "favicon-master.png"
    master.save(master_path, "PNG", optimize=True)
    outputs["master"] = master_path

    png32 = out_dir / "favicon-32x32.png"
    master.resize((32, 32), Image.Resampling.LANCZOS).save(png32, "PNG", optimize=True)
    outputs["png32"] = png32

    png16 = out_dir / "favicon-16x16.png"
    master.resize((16, 16), Image.Resampling.LANCZOS).save(png16, "PNG", optimize=True)
    outputs["png16"] = png16

    apple = out_dir / "apple-touch-icon.png"
    # Apple touch icons typically sit on an opaque rounded square; keep transparent master scaled.
    master.resize((APPLE_TOUCH, APPLE_TOUCH), Image.Resampling.LANCZOS).save(
        apple, "PNG", optimize=True
    )
    outputs["apple"] = apple

    ico_path = out_dir / "favicon.ico"
    ico_images = [
        master.resize(sz, Image.Resampling.LANCZOS) for sz in SIZES_ICO
    ]
    ico_images[0].save(
        ico_path,
        format="ICO",
        sizes=SIZES_ICO,
        append_images=ico_images[1:],
    )
    outputs["ico"] = ico_path

    print(f"bg≈{bg_color}")
    for key, path in outputs.items():
        print(f"  {key}: {path}")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source square icon with solid background")
    parser.add_argument(
        "-d",
        "--out-dir",
        type=Path,
        default=Path("favicon-out"),
        help="Output directory",
    )
    parser.add_argument("--fill", type=float, default=0.82)
    parser.add_argument("--tolerance", type=float, default=30.0)
    parser.add_argument("--feather", type=float, default=8.0)
    parser.add_argument("--bg", type=parse_rgb, default=None)
    parser.add_argument("--master-size", type=int, default=512)
    args = parser.parse_args()

    if not 0.5 <= args.fill <= 0.95:
        print("error: --fill must be between 0.5 and 0.95", file=sys.stderr)
        return 2

    try:
        process(
            args.input,
            args.out_dir,
            fill_ratio=args.fill,
            tolerance=args.tolerance,
            feather=args.feather,
            bg=args.bg,
            master_size=args.master_size,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
