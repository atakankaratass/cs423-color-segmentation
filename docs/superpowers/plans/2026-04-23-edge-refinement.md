# Edge Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `edge_supported` keep components with internal edge support while rejecting flat false-positive regions that only have outer boundary contrast.

**Architecture:** Keep the pipeline shape unchanged and adjust only the refinement scoring path in `src/cs423_segmentation/pipeline.py`. Use the existing regression test in `tests/test_morphology_and_pipeline.py` as the red/green guardrail, and compute support from component-local analysis so the outer background boundary does not count as evidence.

**Tech Stack:** Python 3.9+, NumPy, pytest, Makefile validation targets

---

### Task 1: Lock the failing behavior

**Files:**

- Modify: `tests/test_morphology_and_pipeline.py`
- Test: `tests/test_morphology_and_pipeline.py::test_hsv_edge_refinement_filters_out_flat_false_positive_region`

- [ ] **Step 1: Keep the failing regression test explicit**

```python
def test_hsv_edge_refinement_filters_out_flat_false_positive_region() -> None:
    result = run_pipeline(image, config)
    assert result.count == 1
    assert result.component_sizes == [4]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_morphology_and_pipeline.py -k edge_refinement -q`
Expected: `FAIL` with `assert 2 == 1`

### Task 2: Implement the minimal refinement fix

**Files:**

- Modify: `src/cs423_segmentation/pipeline.py`
- Read: `src/cs423_segmentation/counting.py`
- Test: `tests/test_morphology_and_pipeline.py::test_hsv_edge_refinement_filters_out_flat_false_positive_region`

- [ ] **Step 1: Add component-local support measurement**

```python
def _component_internal_edge_fraction(
    grayscale: np.ndarray, component: np.ndarray, gradient_threshold: float
) -> float:
    rows, cols = np.nonzero(component)
    row_start, row_end = rows.min(), rows.max() + 1
    col_start, col_end = cols.min(), cols.max() + 1
    component_crop = component[row_start:row_end, col_start:col_end]
    grayscale_crop = grayscale[row_start:row_end, col_start:col_end]
    return ...
```

- [ ] **Step 2: Use local intensity differences that stay inside the component**

```python
vertical_pairs = component_crop[:-1, :] & component_crop[1:, :]
vertical_support = vertical_pairs & (
    np.abs(grayscale_crop[:-1, :] - grayscale_crop[1:, :]) >= gradient_threshold
)
```

Mirror the same logic horizontally, count supported pixels from those internal pairs, and divide by component size.

- [ ] **Step 3: Swap the refinement loop to use the new fraction**

```python
grayscale = image.astype(np.float32).mean(axis=-1)
for component in extract_components(mask, min_component_size=1):
    edge_fraction = _component_internal_edge_fraction(grayscale, component, gradient_threshold)
    if edge_fraction >= min_edge_fraction:
        refined |= component
```

- [ ] **Step 4: Run the targeted test to verify it passes**

Run: `python3 -m pytest tests/test_morphology_and_pipeline.py -k edge_refinement -q`
Expected: `1 passed`

### Task 3: Run repository validation and integrate

**Files:**

- Validate current branch state

- [ ] **Step 1: Run validation suite**

Run: `make validate-pr`
Expected: all configured checks pass

- [ ] **Step 2: Commit the change**

```bash
git add docs/superpowers/specs/2026-04-23-edge-refinement-design.md docs/superpowers/plans/2026-04-23-edge-refinement.md src/cs423_segmentation/pipeline.py tests/test_morphology_and_pipeline.py
git commit -m "feat: add edge-assisted component refinement"
```

- [ ] **Step 3: Push the branch**

Run: `git push`
Expected: push succeeds and remote branch updates
