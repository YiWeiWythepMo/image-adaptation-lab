---
name: image_resize
description: Generate multiple preset output sizes for local images using safe padding and timestamped output folders.
---

# Image Resize Skill（多尺寸适配技能）

## 使用场景
当用户需要将一批电商图片适配成多种标准尺寸（如 1:1、4:5、16:9）时使用。

---

## 工作流程

1. 调用本地脚本：`scripts/image_resize.py`
2. 从 `config/resize_presets.json` 读取尺寸配置
3. 扫描 `sample_images/` 文件夹中的所有图片
4. 对每张图片执行：
   - 等比缩放（不裁切主体）
   - 使用白色背景进行 padding
5. 为每个尺寸生成输出图片
6. 输出目录带时间戳，避免覆盖历史结果：
   - `output/resized/<timestamp>/`
7. 生成处理报告：
   - `output/resize_report_<timestamp>.json`
8. 返回摘要信息：
   - 输入数量
   - 生成数量
   - 失败数量

---

## 设计原则（非常重要）

### 1. 保守处理（Safe-first）
- 不裁切主体
- 不破坏原图结构

### 2. 可追溯（Traceable）
- 每次运行都有独立时间戳目录
- 不覆盖历史结果

### 3. 批处理稳定性
- 单张失败不影响整体流程
- 所有错误被记录

---

## 规则

- 仅处理支持格式：jpg / png / webp / bmp
- 所有输出为 JPG（统一格式）
- 原始图片绝不覆盖
- 输出目录自动创建
- 若文件损坏或读取失败，记录到报告中

---

## 输出结构示例
output/
└─ resized/
└─ 20260330_153045/
├─ square/
├─ portrait_4_5/
└─ banner_16_9/

output/
└─ resize_report_20260330_153045.json

---

## 后续扩展方向（为未来 AI 做铺垫）

该 skill 当前为“规则驱动”版本，后续可以扩展：

- 智能裁切（主体检测）
- padding vs crop 自动决策
- AI 扩图（outpainting）
- 多背景生成