# Open Questions

| Question ID | Question | Why it matters | Related evidence/part | Priority | Validation method | Owner | Status |
|---|---|---|---|---|---|---|---|
| Q-001 | What reuse/redistribution terms apply to the downloadable CAD? | Determines whether the geometry may remain publicly hosted | SRC-002 | High | Obtain written license/permission or published terms | Owner | Open |
| Q-002 | Does the `.3dm` bounding box exactly match 655 × 840 × 700 mm after axis mapping? | Prevents scale/orientation errors | EV-001, EV-004 | High | Inspect Rhino model units and computed bounds | Owner | Open |
| Q-003 | Are internal joints and section sizes production-authoritative? | Required before any fabrication use | EV-004 | Critical | Obtain production drawings or physical measurements | Owner | Open |
| Q-004 | Do the four inferred viewer groups correspond to actual shop assemblies and joints? | The exploded view must not be mistaken for an assembly sequence | EV-004, DEC-001 | High | Compare against manufacturer assembly/production documentation | Owner | Open |

This D01 viewer is L0 reference visualization only and must not be used as a production drawing.

- Q-005: Verify Rhino file units and explain catalogue-versus-mesh extent differences (651.964 vs 655; 700.668 vs 700); no manufacturing tolerances inferred.
- Q-006: Validate per-surface subgroup assignments and physical component boundaries; M001–M075 are not a fabrication BOM.
