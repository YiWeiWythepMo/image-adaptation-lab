from __future__ import annotations

import json
from pathlib import Path
from collections import Counter


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}


def scan_images(input_dir: Path) -> dict:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input folder does not exist: {input_dir}")

    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path is not a folder: {input_dir}")

    image_files = [
        p for p in input_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    ext_counter = Counter(p.suffix.lower() for p in image_files)

    return {
        "input_dir": str(input_dir.resolve()),
        "total_images": len(image_files),
        "by_extension": dict(sorted(ext_counter.items())),
        "files": [str(p.resolve()) for p in image_files],
    }


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    input_dir = project_root / "sample_images"
    output_dir = project_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    result = scan_images(input_dir)

    output_file = output_dir / "image_inventory_report.json"
    output_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("Scan finished.")
    print(f"Total images: {result['total_images']}")
    print(f"Report saved to: {output_file}")


if __name__ == "__main__":
    main()