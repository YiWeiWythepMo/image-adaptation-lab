from __future__ import annotations

import json
from pathlib import Path
from typing import Dict
from datetime import datetime

from PIL import Image


# 支持的图片格式
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def load_presets(config_path: Path) -> Dict[str, Dict[str, int]]:
    """
    加载尺寸配置文件（JSON）
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Preset config not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resize_with_padding(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """
    核心逻辑：等比缩放 + 白底填充

    目标：
    - 不裁切主体
    - 保持原图完整
    - 用白色背景补齐比例差
    """
    # 转为 RGB（避免 PNG 等模式问题）
    original = image.convert("RGB")
    original_width, original_height = original.size

    # 计算缩放比例（保证完整显示）
    scale = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # 执行缩放
    resized = original.resize((new_width, new_height))

    # 创建白底画布
    canvas = Image.new("RGB", (target_width, target_height), color=(255, 255, 255))

    # 计算居中位置
    offset_x = (target_width - new_width) // 2
    offset_y = (target_height - new_height) // 2

    # 粘贴到画布中央
    canvas.paste(resized, (offset_x, offset_y))

    return canvas


def process_folder(input_dir: Path, output_dir: Path, presets: Dict[str, Dict[str, int]]) -> dict:
    """
    批量处理文件夹内图片

    功能：
    - 遍历所有图片
    - 按 preset 生成多尺寸版本
    - 记录成功与失败
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # 找到所有图片文件
    image_files = [
        p for p in input_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    summary = {
        "input_dir": str(input_dir.resolve()),
        "output_dir": str(output_dir.resolve()),
        "total_input_images": len(image_files),
        "generated_files": [],
        "failed_files": []
    }

    for image_path in image_files:
        try:
            with Image.open(image_path) as img:
                # 对每种尺寸配置进行处理
                for preset_name, size in presets.items():
                    target_width = size["width"]
                    target_height = size["height"]

                    # 调用 resize + padding
                    result = resize_with_padding(img, target_width, target_height)

                    # 输出目录：按 preset 分类
                    output_subdir = output_dir / preset_name
                    output_subdir.mkdir(parents=True, exist_ok=True)

                    # 输出文件名：原名 + preset
                    output_file = output_subdir / f"{image_path.stem}_{preset_name}.jpg"
                    result.save(output_file, quality=95)

                    summary["generated_files"].append(str(output_file.resolve()))

        except Exception as e:
            summary["failed_files"].append({
                "file": str(image_path.resolve()),
                "error": str(e)
            })

    summary["generated_count"] = len(summary["generated_files"])
    summary["failed_count"] = len(summary["failed_files"])
    return summary


def main() -> None:
    """
    主入口：
    - 生成时间戳目录
    - 执行批处理
    - 输出报告
    """

    project_root = Path(__file__).resolve().parent.parent
    input_dir = project_root / "sample_images"

    # ✅ 新增：时间戳（格式：20260330_153045）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 输出目录带时间戳（避免覆盖）
    output_dir = project_root / "output" / "resized" / timestamp

    config_path = project_root / "config" / "resize_presets.json"

    # 报告文件也带时间戳
    report_path = project_root / "output" / f"resize_report_{timestamp}.json"

    # 加载尺寸配置
    presets = load_presets(config_path)

    # 执行批处理
    summary = process_folder(input_dir, output_dir, presets)

    # 写入报告
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # 控制台输出
    print("Resize finished.")
    print(f"Input images: {summary['total_input_images']}")
    print(f"Generated files: {summary['generated_count']}")
    print(f"Failed files: {summary['failed_count']}")
    print(f"Output folder: {output_dir}")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()