---
name: image_inventory
description: Scan a local image folder and summarize image counts by format.
---

# Image Inventory Skill

Use this skill when the user wants to inspect a folder of images before batch processing.

Workflow:
1. Use the local Python script `scripts/image_inventory.py`.
2. Scan the sample image folder and count supported image files.
3. Save the summary report to `output/image_inventory_report.json`.
4. Return a short summary including total image count and file types.

Rules:
- Only inspect image files.
- Do not delete or overwrite original images.
- If the folder is empty, report that clearly.