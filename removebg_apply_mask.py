#!/usr/bin/env python3
"""Remove a photo background with remove.bg and apply its alpha mask to the original.

Usage:
  export REMOVE_BG_API_KEY='your-api-key'
  python removebg_apply_mask.py input.jpg output.png

The final PNG keeps the original image's dimensions and RGB pixels. Only its
alpha channel comes from remove.bg's result.
"""

import os
import sys
from pathlib import Path

import requests
from PIL import Image

API_URL = "https://api.remove.bg/v1.0/removebg"


def main() -> int:
    if len(sys.argv) != 3:
        print(
            f"Usage: {Path(sys.argv[0]).name} INPUT_IMAGE OUTPUT_PNG", file=sys.stderr
        )
        return 2

    api_key = os.environ.get("REMOVE_BG_API_KEY")
    if not api_key:
        print("Set REMOVE_BG_API_KEY before running this script.", file=sys.stderr)
        return 2

    input_path, output_path = map(Path, sys.argv[1:])
    if not input_path.is_file():
        print(f"Input image not found: {input_path}", file=sys.stderr)
        return 2

    try:
        with input_path.open("rb") as image_file:
            response = requests.post(
                API_URL,
                headers={"X-Api-Key": api_key},
                files={"image_file": (input_path.name, image_file)},
                data={"size": "full", "format": "png"},
                timeout=180,
            )
        response.raise_for_status()
    except requests.RequestException as exc:
        detail = exc.response.text if exc.response is not None else str(exc)
        print(f"remove.bg request failed: {detail}", file=sys.stderr)
        return 1

    try:
        # Preserve the original pixels and dimensions; use only the returned alpha.
        with Image.open(input_path) as original:
            original = original.convert("RGBA")
            from io import BytesIO

            cutout = Image.open(BytesIO(response.content)).convert("RGBA")
            alpha = cutout.getchannel("A")
            if alpha.size != original.size:
                alpha = alpha.resize(original.size, Image.Resampling.LANCZOS)
            original.putalpha(alpha)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            original.save(output_path, format="PNG", optimize=True)
    except Exception as exc:
        print(f"Could not create output PNG: {exc}", file=sys.stderr)
        return 1

    print(
        f"Saved transparent PNG: {output_path} ({original.width} x {original.height})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
