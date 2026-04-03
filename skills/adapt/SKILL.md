---
name: ecommerce-image-layout-adapter
description: Use this skill when adapting an ecommerce image to a new aspect ratio or layout while keeping the product and other locked objects unchanged. This skill identifies locked objects, decorations, and background, then recommends a conservative adaptation strategy. Do not use this skill for creative redesign or full image remakes.
---

# Ecommerce Image Layout Adapter

## Goal

Adapt an ecommerce image to a target canvas or aspect ratio without redesigning the image.

This skill is for **layout adaptation**, not creative remake.

The model should give a **conservative recommendation** for how to adapt the image while keeping important elements stable.

---

## Use this skill when

Use this skill when:

- the image needs to fit a new size, ratio, or layout
- the main subject should remain unchanged
- the task is adaptation rather than redesign
- the background may be extended if necessary

Typical cases:

- convert a square ecommerce image into a banner
- adapt a hero image to desktop and mobile layouts
- create more usable empty space around a product
- extend background while preserving the original subject

---

## Do not use this skill when

Do not use this skill when:

- the user wants a new visual concept
- the subject itself should be redrawn or restyled
- the product should change appearance, structure, material, or color
- the task is a full poster remake or ad redesign
- the image is mainly typography and layout rather than product imagery

---

## Core boundaries

### Locked objects

Locked objects are elements that must remain unchanged in content.

Current locked object types:

- product
- FIFA World Cup trophy

Allowed actions:

- move
- uniform scale

Not allowed:

- redraw
- regenerate
- reshape
- recolor
- distort
- non-uniform scale
- crop key parts
- cover key parts

Rule:

- locked objects may be adjusted for layout
- locked objects must not be recreated

---

### Decorations

Decorations include:

- logo
- text
- label
- badge
- watermark-like brand elements

Rules:

- logo should be preserved if possible
- logo may move or scale uniformly
- logo should not be replaced or regenerated unless explicitly allowed
- simple text may be preserved
- complex text should not rely on image generation for precise reconstruction
- if text is too complex, it may be rebuilt later outside this skill pipeline

---

### Background

Background includes all non-locked, non-decoration visual areas, such as:

- wall
- floor
- table
- room
- scene
- atmosphere
- generic environmental elements

Rules:

- background may be extended if needed
- extension should be limited to newly added regions
- the original core content area should not be regenerated
- background extension is for layout support, not creative redesign

---

## Recommended reasoning process

The model should analyze the image in this order:

1. identify locked objects
2. identify decorations
3. identify whether the background can support adaptation
4. recommend the simplest acceptable strategy

Preferred strategy order:

1. `scale_only`
2. `scale_plus_padding`
3. `scale_plus_padding_plus_background_extension`

This order is a **preference**, not a rigid execution tree.

The model should use judgment to decide which strategy is most appropriate for the specific image.

---

## What the model should decide

For each image, the model should judge:

- what the locked objects are
- whether they can remain complete and stable
- whether text or logo placement affects layout choices
- whether padding is enough
- whether background extension is necessary
- whether the result is low, medium, or high risk

The model should prioritize:

- preserving subject identity
- minimizing unnecessary changes
- avoiding risky regeneration
- choosing the simplest workable solution

---

## Required output

Before execution, produce a structured recommendation.

Use this format:

```json
{
  "image_analysis": {
    "locked_objects": [
      {
        "type": "product",
        "present": true,
        "complete": true
      }
    ],
    "decorations": {
      "has_logo": true,
      "has_text": true,
      "text_complexity": "simple"
    },
    "background_editable": true
  },
  "recommended_strategy": "scale_plus_padding",
  "reason": "The product can remain unchanged, but scaling alone is not enough to fit the target layout cleanly.",
  "risk_level": "low"
}