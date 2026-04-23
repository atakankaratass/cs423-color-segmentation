# Edge Refinement Design

## Context

The project already compares RGB thresholding and HSV thresholding. The remaining work adds a third comparison method, `edge_supported`, so the report can compare a threshold-only pipeline against a threshold-plus-refinement pipeline.

The current implementation incorrectly counts a flat false-positive region as edge-supported because it measures Sobel responses anywhere inside the connected component. Strong contrast at the outside boundary of a wrong region is enough to keep it.

## Goal

Keep thresholded components only when they also contain meaningful internal edge or texture support. The refinement must reject flat regions whose apparent edge evidence comes only from their boundary against the background.

## Approach

Use the existing failing regression test as the guardrail. Keep the current pipeline structure and refine only the `edge_supported` scoring logic.

For each connected component:

1. Compute a tight bounding box around the component.
2. Measure gradient support only within the component's own interior analysis region, not from contrast introduced by the outer background boundary.
3. Keep the component only if its internal support fraction meets `min_edge_fraction`.

This keeps the change small, preserves the existing configuration shape, and aligns with the course goal of comparing segmentation methods that use different visual cues rather than only different thresholds.

## Rejected Alternatives

- Raise `min_edge_fraction` until the test passes: too brittle and does not fix the root cause.
- Erode every component before scoring: smaller code change, but it is more likely to remove valid support from already small objects.

## Testing

- Keep `test_hsv_edge_refinement_filters_out_flat_false_positive_region` as the regression test.
- Run the targeted pytest first.
- Run the repository validation suite with `make validate-pr` before commit and push.
