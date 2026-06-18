# Construct-Validity Reclassification Audit (First Pass)

Date: 2026-04-21

Status: exploration-only first pass for `JCB-051`.

Inputs: `datasets/probe_metadata.json`, `results/20260421_phrase_density.json`.

Caveat: phrase-density evidence currently covers `R08`, `R18`, and `R19`; other probes use metadata-only classification.

## Summary

- search_surface_referenceable: 6
- search_surface_mixed: 7
- reconstruction_ambiguous: 4
- reconstruction_candidate: 2
- high_phrase_surface_flag_count: 3

## Probe Table

| Probe | Retrieval | Referenceability | Class | High phrase surface | Treatment |
|---|---|---|---|---|---|
| R01 | search-like | high | search_surface_referenceable | false | mixed_review |
| R02 | search-like | high | search_surface_referenceable | false | mixed_review |
| R03 | search-like | medium | search_surface_mixed | false | mixed_review |
| R04 | search-like | high | search_surface_referenceable | false | mixed_review |
| R05 | search-like | medium | search_surface_mixed | false | mixed_review |
| R06 | search-like | medium | search_surface_mixed | false | mixed_review |
| R07 | search-like | high | search_surface_referenceable | false | mixed_review |
| R08 | reconstruction-like | low | reconstruction_ambiguous | true | needs_reference_or_abstention |
| R09 | search-like | medium | search_surface_mixed | false | mixed_review |
| R10 | search-like | medium | search_surface_mixed | false | mixed_review |
| R11 | reconstruction-like | low | reconstruction_ambiguous | false | needs_reference_or_abstention |
| R12 | search-like | medium | search_surface_mixed | false | mixed_review |
| R13 | reconstruction-like | low | reconstruction_ambiguous | false | needs_reference_or_abstention |
| R14 | search-like | high | search_surface_referenceable | false | mixed_review |
| R15 | search-like | high | search_surface_referenceable | false | mixed_review |
| R16 | reconstruction-like | medium | reconstruction_candidate | false | reconstruction_candidate |
| R17 | reconstruction-like | medium | reconstruction_candidate | false | reconstruction_candidate |
| R18 | reconstruction-like | low | reconstruction_ambiguous | true | needs_reference_or_abstention |
| R19 | search-like | medium | search_surface_mixed | true | search_dominant_caution |

## Next Step

- Extend phrase-surface measurement to all probes and conditions, then reclassify with evidence-surface density for every cell.
