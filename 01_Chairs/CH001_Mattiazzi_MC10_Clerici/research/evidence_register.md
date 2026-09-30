# Evidence Register

| Evidence ID | Subject | Observation/value | Status | Source ID | Method | Uncertainty | Confidence | Verified by/date |
|---|---|---|---|---|---|---|---|---|
| EV-001 | Overall dimensions | 655 × 840 × 700 mm (W × D × H) | `[KNOWN]` | SRC-001 | Direct reading | Manufacturer orientation may differ from viewer axes | High | Codex / 2026-09-30 |
| EV-002 | Seat height | 390 mm; upholstered version 445 mm | `[KNOWN]` | SRC-001 | Direct reading | None stated | High | Codex / 2026-09-30 |
| EV-003 | Materials | European ash or oak; optional leather upholstery | `[KNOWN]` | SRC-001 | Direct reading | Finish/material assignment in CAD not validated | High | Codex / 2026-09-30 |
| EV-004 | Source geometry | Single-seat `.3dm`, 499,366 bytes | `[KNOWN]` | SRC-002 | Direct archive inspection | Modeling accuracy and production authority unknown | Medium–High | Codex / 2026-09-30 |

## Conflicts

No direct conflict is registered. The manufacturer's dimension order is W × D × H, while 3D software axes may use a different orientation.

## D02 viewer audit
- [KNOWN] Browser loader exposes 75 source meshes with 75 unique UUIDs (2026-09-30).
- [DERIVED] Mesh AABB is 840.000 × 651.964 × 700.668 source units; comparison with axis-mapped catalogue dimensions differs by 0 / -3.036 / +0.668. Model units and manufacturing significance remain unverified.
- [ASSUMED] Four geometric zones and ten subgroup labels are visualization classifications only. See `viewer_parity.md`.
