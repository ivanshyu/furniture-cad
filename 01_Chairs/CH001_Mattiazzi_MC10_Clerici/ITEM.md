# ITEM — CH001 Mattiazzi MC10 Clerici Lounge

## Identity

| Field | Value |
|---|---|
| Item ID | `CH001` |
| Category | Chair |
| Original/designer | Konstantin Grcic for Mattiazzi |
| Period | 2015 |
| Intended use | Reference viewing / research |
| Fidelity target | Source-model visualization only |
| Current maturity | L0 |
| Owner | Ivan Shyu |
| Current revision | D02 |

## Rights and provenance

| Field | Value |
|---|---|
| Rights status | Third-party manufacturer/product CAD; redistribution terms not stated in the downloaded archive |
| Intended distribution | Public web visualization with source attribution |
| Restrictions | Do not claim original authorship; preserve source attribution; not a production drawing |

## Design brief

- Objective: publish an interactive browser viewer for the publicly linked MC10 Clerici Lounge CAD.
- Required overall dimensions: 655 × 840 × 700 mm (W × D × H), per manufacturer page.
- Material preference: ash or oak; optional leather upholstery, per manufacturer page.
- Required fidelity: render the supplied `.3dm` geometry without treating it as verified production geometry.
- Permitted redesign: none in D01.

## Known facts

| ID | Claim/value | Status | Source ID | Confidence | Notes |
|---|---|---|---|---|---|
| F-001 | Overall dimensions 655 × 840 × 700 mm | `[KNOWN]` | SRC-001 | High | Manufacturer product page |
| F-002 | Designer: Konstantin Grcic | `[KNOWN]` | SRC-001 | High | Manufacturer product page |
| F-003 | Public 3D CAD package contains 3DM, 3DS, RFA, SKP and STP | `[KNOWN]` | SRC-002 | High | Direct archive inspection |

## Confidence snapshot

| Area | Confidence | Reason |
|---|---:|---|
| Geometry | 75% | Manufacturer-linked CAD is present, but production tolerances are not verified |
| Construction | 15% | Viewer exposes exterior geometry, not joinery intent |
| Materials | 60% | Manufacturer names species/options; exact finish in CAD is not authoritative |

## Deliverables

- [x] Evidence audit (initial)
- [x] Interactive source-model viewer
- [ ] Dimension reconstruction
- [ ] Construction and material definition
- [ ] Prototype drawing package
- [ ] Prototype results
- [ ] Production package

## Current blockers

- CAD redistribution/license terms are not included in the archive.
- Geometry has not been validated against a physical sample or production drawing.

## Next action

Confirm reuse rights and measure the supplied CAD bounding box against the manufacturer dimensions.
