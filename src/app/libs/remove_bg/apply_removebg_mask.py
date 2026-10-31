#!/usr/bin/env python3
"""Apply a remove.bg PNG's transparency mask to the original image.

Usage:
  python apply_removebg_mask.py ORIGINAL.jpg REMOVEBG.png OUTPUT.png

Only the remove.bg alpha channel is used. Original RGB pixels and dimensions
are preserved; the mask is resized when remove.bg supplied a smaller preview.
"""

import argparse
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path, help="Original image, e.g. 038.jpg")
    parser.add_argument(
        "removebg_png", type=Path, help="Transparent PNG downloaded from remove.bg"
    )
    parser.add_argument("output", type=Path, help="Output PNG path")
    args = parser.parse_args()

    with Image.open(args.original) as src:
        original = src.convert("RGBA")

    with Image.open(args.removebg_png) as removed:
        removed_rgba = removed.convert("RGBA")
        alpha = removed_rgba.getchannel("A")

    if alpha.size != original.size:
        alpha = alpha.resize(original.size, Image.Resampling.LANCZOS)

    original.putalpha(alpha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    original.save(args.output, format="PNG", optimize=True)
    print(f"Saved {args.output} ({original.width} x {original.height})")


if __name__ == "__main__":
    main()
