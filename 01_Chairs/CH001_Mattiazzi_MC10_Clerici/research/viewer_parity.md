# D02 viewer parity audit — 2026-09-30

Compared against `docs/CB001_D16_viewer.html`. D01 was NOT equivalent: four assembly buttons replaced the cabinet hierarchy and most controls were absent.

| Cabinet feature | MC10 D02 |
|---|---|
| Header, top navigation, left viewport + right scrollable sidebar, responsive single column | Same layout CSS and breakpoint |
| Seven views | Perspective/front/side/top/legs/armrests/underside; armrest replaces cabinet handle |
| Fixed-view gallery and full-size image | Seven direct CAD renders, independent of viewport interaction; modal + PNG download |
| AI material reference | Not available; explicitly identified as CAD, no fabricated AI images |
| Glass toggle | Explicitly disabled: chair has no glass |
| Back toggle / wireframe | Back region toggle / wireframe |
| GROUP → subgroup → part | Four inferred zones → ten geometric subgroup types → 75 source mesh objects |
| IDs, dropdown, buttons, double-click picking, highlight, dimensions/material | UUID-sorted M001–M075; original-coordinate mesh AABB; material unknown |
| Labels toggle | Clickable projected IDs with basic collision avoidance |
| Spread / exploded / distance | Reversible source-object placement; spread takes precedence |
| Group fitting | Fits currently visible geometry with viewport aspect ratio |
| Atlas / CSV / verification | Same row data; per-object CAD images, CSV and table with UUIDs |

## Browser checks completed
- Desktop two-column layout and CAD gallery rendered.
- F01 → front-leg surfaces: 5 entries; spread and labels rendered.
- M027 selection shows UUID and 35 × 0 × 560 source-coordinate AABB.
- Label toggle removes projected tags.
- All-group explosion renders; reset preserves source mesh positions.
- All seven view buttons update fixed-view title; wireframe renders.
- Verification has 75 data rows, 75 unique UUIDs.
- Atlas has 75 cards / 75 loaded images.
- No error-level browser logs during those checks.

## Evidence and limits
[DERIVED] Source mesh AABB: X 840.000, Y 651.964, Z 700.668 (source coordinates, treated as mm in legacy viewer; file unit setting still TO VERIFY). Relative to catalogue axis-mapped 840/655/700: 0/-3.036/+0.668. This is not manufacturing tolerance verification.

[ASSUMED] Classification is geometric, not a source assembly hierarchy. Surfaces are NOT physical parts. Cabinet has named generated parts; chair has unnamed source surfaces. Shared UI behavior does not make their manufacturing information equally reliable. Materials, joinery, physical part boundaries, reproduction rights remain open. Maturity remains L0 / HOLD.

Code architecture is adapted, not identical: cabinet embeds mesh JSON; chair loads a 3DM and has an external viewer module. Gallery is direct CAD rather than cabinet AI images; report pages are runtime-generated query routes rather than static files.
- Full-size CAD image modal tested (800 px source image).
- Mobile 390 × 844 tested: single-column layout, 362 px viewport, document width 390 px with no horizontal overflow; model fits. Temporary viewport reset.
- Static parity test asserts every cabinet HTML control ID exists in MC10; all 3 tests pass. JavaScript syntax check passes.
