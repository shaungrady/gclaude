# FDM fundamentals for printed joints (Prusa MK3S+, 0.4 mm nozzle)

Status: draft in progress.

## Quick reference

| Item | Value | Source |
|---|---|---|
| PrusaSlicer elephant foot compensation (bundled profile) | 0.2 mm | [1][2] |
| Prusament PLA HDT (0.45 and 1.80 MPa) | 55 °C | [3] |
| Prusament PETG HDT (0.45 and 1.80 MPa) | 68 °C | [4] |
| PLA interlayer adhesion vs horizontal tensile | 17 ± 3 vs 51 ± 3 MPa (~0.33) | [3] |
| PETG interlayer adhesion vs horizontal tensile | 18 ± 4 vs 47 ± 2 MPa (~0.38) | [4] |

(Sections to follow.)

## Sources

1. Prusa Knowledge Base, "Elephant foot compensation." https://help.prusa3d.com/article/elephant-foot-compensation_114487
2. Repo profile `profiles/mk3s_pla_0.20mm.ini` (`elefant_foot_compensation = 0.2`).
3. Prusa Polymers, Prusament PLA technical data sheet v1.1 (2022). https://www.matterhackers.com/r/xFvGl8
4. Prusa Polymers, Prusament PETG technical data sheet v1.1 (2022). https://www.3dprintergear.com.au/assets/files/technical-data-sheet%20(1).pdf
