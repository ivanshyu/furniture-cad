# Decision Log

| Decision ID | Date | Decision | Reason | Evidence/options considered | Affected files/parts | Approved by |
|---|---|---|---|---|---|---|
| DEC-001 | 2026-09-30 | Publish an interactive four-group exploded view: B01 back, S01 seat, F01 left frame, F02 right frame | The source 3DM exposes 75 unnamed render surfaces rather than a verified parts/BOM hierarchy | Source geometry, catalogue form, viewer usability | `docs/mc10/index.html`; CH001 construction notes | Owner requested cabinet-style exploded view |

## DEC-002 — D02 cabinet UI parity
Replace the four-button viewer with cabinet-style layout, seven views, fixed CAD gallery, GROUP/subgroup/source-object hierarchy, picking/highlighting, labels, spread/explosion, atlas, CSV and verification. Stable IDs are sorted by source UUID. Geometry classification remains assumed; do not label 75 surfaces as 75 manufacturing parts. See viewer_parity.md for explicit differences and checks.
