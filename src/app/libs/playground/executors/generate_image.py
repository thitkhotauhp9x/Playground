"""Generate an image from a text prompt using the OpenAI Images API.

Usage:
    export OPENAI_API_KEY="..."
    python -m playground.executors.generate_image "A small red panda reading under a tree" \
        --output red-panda.png
"""

from __future__ import annotations

import argparse
import base64
from pathlib import Path

from openai import OpenAI


def generate_image(prompt: str, output: Path, size: str = "1024x1024") -> Path:
    """Generate one image and save it locally; returns the output path."""
    client = OpenAI()  # Reads OPENAI_API_KEY from the environment.
    result = client.images.generate(
        model="gpt-image-2.5-flare",
        prompt=prompt,
        n=1,
        size=size,
        output_format="png",
    )

    image_data = result.data[0].b64_json
    if not image_data:
        raise RuntimeError("The image API returned no image data.")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(base64.b64decode(image_data))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an image from a text prompt.")
    parser.add_argument("prompt", help="Describe the image to generate")
    parser.add_argument("--output", type=Path, default=Path("generated.png"))
    parser.add_argument(
        "--size", default="1024x1024", help="Image size, e.g. 1024x1024"
    )
    args = parser.parse_args()

    saved_path = generate_image(args.prompt, args.output, args.size)
    print(f"Saved image to {saved_path.resolve()}")


if __name__ == "__main__":
    main()
