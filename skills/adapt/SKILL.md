---
name: ecommerce-image-layout-adapter
description: Use this skill when adapting ecommerce images to a target aspect ratio or page layout while keeping the product and other locked objects unchanged. This skill analyzes the image in three layers—locked objects, decorations, and background—then chooses a conservative layout strategy: first uniform scaling, then padding, then AI background extension only in newly added areas. Do not use this skill for freeform creative redesign, full poster remakes, or cases where the main subject itself should be regenerated.
---

# Ecommerce Image Layout Adapter

## Purpose

This skill adapts ecommerce visuals to new page sizes and aspect ratios while preserving the original subject identity and brand-critical elements.

The goal is not to redesign the image.  
The goal is to make the image fit a new layout with minimal risk.

This skill follows a fixed decision order:

1. identify locked objects
2. identify decorations
3. adapt layout by scaling
4. add padding if needed
5. use AI generation only for new background regions
6. evaluate whether the result is acceptable

---

## When to use

Use this skill when:

- the image needs to fit a new aspect ratio or target canvas
- the product must remain unchanged
- the image contains a locked object that should only move or scale
- the background can be extended if needed
- the task is layout adaptation, not creative redesign

Examples:

- convert a square ecommerce image into a banner
- adapt a hero image to desktop and mobile ratios
- preserve the product while creating more empty space for layout
- extend the background without changing the product itself

---

## When NOT to use

Do not use this skill when:

- the user wants a new creative concept
- the subject itself should be redrawn or redesigned
- the product should change appearance, material, color, or structure
- the image is primarily a typography poster or text-heavy design
- the task is full ad design rather than conservative adaptation

Examples:

- “redesign this as a futuristic campaign poster”
- “change the product appearance”
- “replace the whole scene with a new concept”
- “rebuild the ad from scratch”

---

## Layer model

This skill analyzes the image using three layers.

### 1. Locked Objects

Locked objects are the most important visual subjects.

Current locked object types:

- product
- FIFA World Cup trophy

Locked objects must remain unchanged in content.

Allowed actions:

- move
- uniform scale

Forbidden actions:

- redraw
- reshape
- recolor
- regenerate
- crop key parts
- occlude key parts
- non-uniform scale

Core rule:

> Locked objects participate only in layout adjustment, not in content generation.

---

### 2. Decorations

Decorations include:

- logo
- text
- label
- badge
- watermark-like brand elements

#### Logo

Logo should be preserved whenever possible.

Allowed actions:

- move
- uniform scale

Forbidden actions:

- redraw
- distort
- replace with a different logo
- alter official brand appearance unless explicitly allowed

#### Text

Text should be identified separately from the background.

Text handling rule:

- simple text may be preserved temporarily
- complex text may be removed and rebuilt later outside this skill pipeline

This skill does not rely on image generation to accurately recreate text.

---

### 3. Background

Background includes all non-locked, non-decoration visual areas such as:

- scene
- wall
- floor
- table
- room
- atmosphere
- generic environmental elements

Background is the only layer allowed to be extended by AI generation.

Core rule:

> Background exists to support layout adaptation, not to become a new design focus.

---

## Required reasoning order

Always follow this order.

### Step 1: Identify locked objects

Check whether the image contains:

- product
- World Cup trophy

For each locked object, determine:

- whether it exists
- whether it is complete
- whether it is near the edge
- whether it can fit the target layout by move + uniform scale only

Do not decide strategy before this step.

---

### Step 2: Identify decorations

Check whether the image contains:

- logo
- text

Determine:

- whether the logo must be preserved
- whether text is simple or complex
- whether decoration placement will constrain the layout

Do not let decoration handling override locked object preservation.

---

### Step 3: Choose the background adaptation strategy

Use this fixed priority order.

#### Strategy order

1. **Uniform scaling of locked objects**
2. **Padding to target ratio**
3. **AI generation only for newly added background areas**

Never skip directly to full-image regeneration.

#### Rule 1: Scaling first

Try to solve the layout by moving and uniformly scaling locked objects.

If scaling alone is enough, stop there.

#### Rule 2: Padding second

If scaling alone is not enough, add padding to reach the target ratio.

The original content should remain intact as much as possible.

#### Rule 3: AI background extension last

If padding creates empty or visually weak areas, use AI generation only to extend the newly added background zones.

Do not redraw the locked objects.  
Do not redraw the original core content area.  
Do not use AI generation to redesign the full composition.

---

## Conservative execution policy

Default to the most conservative valid solution.

Preference order:

1. scale only
2. scale + padding
3. scale + padding + background extension

If two strategies are both acceptable, choose the safer one.

---

## Refusal / fallback conditions

Do not force automatic generation in these cases:

- locked object cannot remain complete
- target ratio would require extreme subject shrinkage
- new padded area is too large for reliable background extension
- logo is too important and cannot be preserved safely
- text is too complex and heavily integrated into the composition
- the result would effectively become a redesign rather than an adaptation

Fallback options:

- return a conservative padded version
- flag for manual review
- recommend text reconstruction outside the image-generation step

---

## Output format

When using this skill, produce a structured internal analysis before execution.

Suggested format:

```json
{
  "locked_objects": [
    {
      "type": "product",
      "present": true,
      "complete": true,
      "allowed_actions": ["move", "scale_uniform"]
    }
  ],
  "decorations": {
    "has_logo": true,
    "has_text": true,
    "text_complexity": "simple"
  },
  "background": {
    "editable": true
  },
  "selected_strategy": "scale_then_padding_then_background_extension",
  "risk_level": "medium"
}