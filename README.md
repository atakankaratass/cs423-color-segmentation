# CS423 Color Segmentation Project

Classical computer vision pipeline for color-based object extraction and counting.

Current baseline implementation includes:

- RGB thresholding
- HSV thresholding
- binary morphology cleanup
- connected-component counting
- dataset evaluation CLI
- versioned profile configuration
- bundled sample dataset for reproducible smoke tests
- real-dataset folder/template for final project data collection

## Mandatory Dataset Checklist

These are now mandatory project requirements, not optional nice-to-haves:

- fixed metadata schema for every image
- `expected_count` for every image
- `lighting`, `background`, and `overlap` labels for every image
- versioned profile configuration files kept separate from dataset metadata

## Setup

```bash
make install-dev
```

## Validation

```bash
make validate-pr
```

This runs:

- format checks
- lint
- tests
- smoke test

## Sample Evaluation

```bash
make evaluate-rgb
make evaluate-hsv
make run-experiments
make generate-report
make tune-sample-rgb
make tune-sample-hsv
```

Outputs are written to `results/tables/`.

`make generate-report` writes:

- `results/reports/sample/profile-summary.csv`
- `results/reports/sample/condition-summary.csv`
- `results/reports/sample/masks/*.png`
- `results/reports/sample/overlays/*.png`

`make tune-sample-rgb` and `make tune-sample-hsv` write ranked tuning artifacts under:

- `results/tuning/sample/.../tuning-results.json`
- `results/tuning/sample/.../tuning-results.csv`
- `results/tuning/sample/.../tuning-results.md`

## Real Dataset Preparation

Use the real dataset template and guide:

- metadata template: `data/real/metadata/dataset.template.json`
- starter profiles: `configs/profiles/v1/multi-color-template.json`
- collection guide: `docs/dataset-collection-guide.md`

After your team fills `data/real/metadata/dataset.json`, run:

```bash
make validate-real-dataset
```

## CLI Usage

```bash
PYTHONPATH=src python3 -m cs423_segmentation evaluate \
  --metadata data/sample/metadata/dataset.json \
  --profile hsv_red \
  --output results/tables/hsv-sample-results.json

PYTHONPATH=src python3 -m cs423_segmentation run-experiments \
  --metadata data/sample/metadata/dataset.json \
  --output results/tables/experiment-summary.json
```

## Repository Rules

Read before contributing:

- `CONTRIBUTING.md`
- `AGENTS.md`
- `docs/ai-tooling.md`
