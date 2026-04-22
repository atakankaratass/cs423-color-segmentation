# Dataset Collection Guide

Use this guide when collecting the real project dataset.

## What You Should Collect

Collect photos of clearly countable colored objects.

Recommended target colors:

- red
- green
- blue
- yellow

These are practical because they are easy to separate in both RGB and HSV and give you a stronger final comparison.

## Minimum Dataset Recommendation

Aim for at least:

- 4 target colors
- 8 to 12 images per color
- at least 32 images total

For each color, try to include:

- controlled lighting
- dim lighting
- bright lighting
- plain background
- cluttered background
- no overlap
- mild overlap

## What You Need To Record For Every Image

Each image entry in the metadata file must include:

- `image_id`
- `image_path`
- `target_color`
- `expected_count`
- `lighting`
- `background`
- `overlap`

Optional but useful:

- `notes`

## Label Vocabulary

Use these labels consistently.

### Lighting

- `controlled`
- `dim`
- `bright`

### Background

- `plain`
- `cluttered`

### Overlap

- `none`
- `mild`
- `heavy`

## How To Capture Images

- Keep the camera roughly top-down or front-facing, but stay consistent per subset.
- Avoid motion blur.
- Keep objects fully visible unless you intentionally want a harder case.
- Count the target objects manually right after taking the photo.
- Do not rename files randomly after labeling.

## File Placement

- raw images: `data/real/raw/`
- dataset metadata: `data/real/metadata/dataset.json`
- profile config: `configs/profiles/v1/multi-color-template.json`

Start from:

- `data/real/metadata/dataset.template.json`

Then copy it to:

- `data/real/metadata/dataset.json`

## Recommended Team Split

- one person captures photos
- one person verifies counts and labels
- one person tunes profiles and runs experiments

This reduces labeling mistakes and helps keep the experiment reproducible.
