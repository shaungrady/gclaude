# FDM fundamentals for printed joints (Prusa MK3S+, 0.4 mm nozzle)

Shared foundation for the other joinery docs. Target: Prusa MK3S+, 0.4 mm nozzle, 0.45 mm extrusion width, 0.20 mm layers, PrusaSlicer 2.7.2 (the version installed here), Prusament PLA/PETG. Numbers carry source tags [n]; "derived" means computed from geometry, "house" means the repo's CLAUDE.md rule, "unverified" means not confirmed by a primary measurement.

## Quick reference

| Item | Value | Source |
|---|---|---|
| General accuracy, well-tuned Original Prusa | ±0.2 mm or better | [11] |
| Press / interference (separate parts) | 0 to 0.05 mm per side, test first | house, unverified |
| Snug / locating fit | 0.1 mm per side | house; 0.1 mm gap fuses if printed in place [17] |
| Sliding fit (separate parts) | 0.2 mm per side | house [17] |
| Moving / print-in-place joint | 0.25 to 0.3 mm per side (0.2 mm marginal) | [11][17][18] |
| Vertical hole for screw clearance | model nominal + 0.2 to 0.3 mm diameter | house; [15] mechanism |
| Elephant foot compensation (bundled profile) | 0.2 mm (first layer only) | [1][2] |
| Wall from n perimeters (0.45 w, 0.2 h) | 1: 0.45, 2: 0.86, 3: 1.27, 4: 1.67, 5: 2.08 mm | [12], derived |
| Minimum wall | 0.86 mm (2 perimeters); 1.27 mm normal; ≥1.67 to 2.1 mm load bearing | [12], house |
| Minimum vertical gap that stays open | 0.3 mm safe; 0.2 mm marginal; <0.1 mm closed by slicer | [2][17] |
| Overhang, no supports | 45° clean; 50 to 60° acceptable on MK3S | [11][16][17] |
| Bridge | ≤5 mm no visible sag; ≤18 mm acceptable; 20 mm slight sag | [16][17] |
| Z/XY tensile strength, PLA | 0.33 to 0.73 (typ. ~0.6) | [3][5][7][8] |
| Z/XY tensile strength, PETG | 0.38 to 0.60 (typ. ~0.5) | [4][6][8] |
| Z strain to failure | ~2% (PLA 2.0%, PETG 1.8%) vs 7 to 8% XY; ratio ~0.25 | [5][6] |
| PLA HDT / Tg | 55 °C (0.45 and 1.8 MPa) / 55 to 60 °C | [3][20] |
| PETG HDT / Tg | 68 °C / ~80 °C | [4][21] |
| Annealed standard PLA | up to 10% XY shrink, Z growth; layer adhesion unchanged | [10] |

## 1. Dimensional accuracy and fits

**XY vs Z.** XY is set by extrusion behavior; Z is quantized to the layer height. PrusaSlicer slices each layer at a single height, so any Z feature (a ledge, the top of a slot, a horizontal hole's top) lands on a 0.2 mm grid (derived). Make Z dimensions that matter multiples of the layer height, counting the 0.2 mm first layer [12]. The first layer is squished, so the bottom 0.2 to 0.4 mm of any part is wider and its Z height depends on the live Z offset.

**Elephant foot.** The bundled profile sets `elefant_foot_compensation = 0.2` (the CLI default is 0) [2]. Prusa says ~0.2 mm suits a 0.4 mm nozzle and it should not exceed about half the first-layer extrusion width [1]. It shrinks only layer 1 inward, so first-layer holes grow slightly and narrow bottom features thin out. Still add a 0.3 to 0.5 mm 45° chamfer to bed edges of mating faces [16], house.

**XY size compensation.** `xy_size_compensation` (default 0) grows or shrinks every contour by a fixed offset: positive enlarges outer walls and shrinks holes, negative the reverse [2]. PrusaSlicer has no separate hole compensation (unlike Cura's), so a value that fixes outer dimensions closes small holes; size holes in CAD instead (forum consensus [2]). Leave it at 0.

**Why holes print undersized.** Four mechanisms [15]: (a) CAD faceting places polygon vertices on the circle, shrinking it by cos(π/n); (b) on curves the inner side of the bead gets excess plastic; (c) the extruded bead "cuts corners" and contracts toward the center, which the author found dominant; (d) ooze at segment starts. Here, `tools/build.py` exports STL at 0.01 mm linear tolerance, so (a) is negligible; (b) and (c) remain and grow as the radius shrinks. Typical result: vertical holes 0.1 to 0.3 mm small in diameter (one MK3 user needed 7.3 mm CAD for a 7 mm hole, anecdotal) [2]. Rule: +0.2 mm diameter for screw clearance (house), +0.3 mm for holes ≤4 mm or for pins that must slide; drill/ream critical bores.

**Horizontal holes** (axis parallel to bed) are worse: the top arc is a series of overhangs that sag, and the vertical size is quantized to layers. Expect the vertical diameter to read 0.1 to 0.3 mm small (unverified estimate). Use a teardrop or flat top (§3), add 0.1 mm extra clearance vertically, or rotate the part so the hole is vertical.

**Fit clearances.** Prusa states no universal value; start at ≥0.3 mm for moving parts like hinges and tune [11]. Measured on a MK3S+, PLA, 0.20 mm: print-in-place cubes on 5 mm pins fused at 0.1 mm gap and turned freely at 0.2 and 0.3 mm [17]. A MK4 group test found 0.25 mm optimal and 0.2 mm fused (search summary, not opened) [18]. Separate parts (printed apart, assembled) need less than print-in-place because nothing fuses: use the table values. Clearances are per side; a pin in a bore needs 2× in diameter.

**Stair-stepping on angled walls (derived).** A surface at angle θ from horizontal steps horizontally by h/tanθ per layer: 0.2 mm at 45°, 0.12 mm at 60°, 0.55 mm at 20°. Shallow tapers (cones, wedges, dovetail flanks, ramps) therefore have a sawtooth whose amplitude can exceed the fit clearance; contact is on the step tips. Make mating angled faces steeper than ~45° from horizontal, or orient them vertical so they print as smooth perimeters. Steps on a shallow mating ramp of two parts interlock like ratchet teeth.

**Seams.** Profile default `seam_position = aligned` [2]; aligned/rear stack the seam into a vertical line of zits [13]. Keep that line off bearing surfaces, pin bores, and snap contact faces: use `rear` and orient the part, or seam painting in the GUI [13]. PrusaSlicer prefers concave corners for seams, so a small notch or inside corner away from the mating face attracts the seam (derived from [13]). Scarf seams and staggered inner seams exist only in newer PrusaSlicer than 2.7.2 [13].

## 2. Anisotropy and strength

| Material, source | XY strength | Z strength | Z/XY | XY strain | Z strain |
|---|---|---|---|---|---|
| PLA, Ultimaker TDS, 100% infill [5] | 45.5 MPa (break) | 33.1 MPa | 0.73 | 7.8% | 2.0% |
| PLA, Hanon 2021 [7] | 56.5 MPa | 35.6 MPa | 0.63 | ~3.5% max | n/a |
| PLA, Prusament [3] | 51 ± 3 MPa | 17 ± 3 (interlayer test) | 0.33 | 2.9% at yield | n/a |
| PLA, CNC Kitchen, 230 °C [8] | ~60 MPa | 40 MPa | 0.67 | n/a | n/a |
| PETG, Ultimaker TDS [6] | 38.5 MPa (break) | 19.0 ± 6.4 MPa | 0.49 | 7.6% | 1.8% |
| PETG, Prusament [4] | 47 ± 2 MPa | 18 ± 4 (interlayer test) | 0.38 | 5.1% at yield | n/a |
| PETG, CNC Kitchen, 245 °C [8] | 55 MPa | 32 MPa | 0.58 | n/a | n/a |

Sources disagree on the ratio (0.33 to 0.73) because test methods differ; Prusa's "interlayer adhesion" is its own method. Caution: Prusament's "Vertical xz" column is a specimen printed on edge, not upright; do not read it as Z [3][4]. Agreement: Z failure is brittle at ~2% strain, about a quarter of XY [5][6]. Design rule: allowable stress across layers ≈ 1/3 of XY, strain across layers ≤1% (derived, conservative). Anything that flexes (snap arms, clips, living hinges) must bend in the XY plane.

**Temperature.** Interlayer strength peaks mid-range: PLA 20 MPa at 190 °C, 39 at 210, 40 at 230, 32 at 270; PETG 18 at 200, 22 at 215, 30 at 230, 32 at 245, 24 at 260 [8]. XY strength barely changed [8]. The bundled PLA profile prints at 215 °C [2]; Prusa's PETG profile at 240 °C [22]. For Z-loaded PLA parts, 225 to 230 °C buys little; drying filament matters more at high temperature [8].

**Layer height.** With a 0.4 mm nozzle, 0.05 to 0.2 mm all gave the same strength flat; upright (Z) hooks peaked at 0.15 mm, 0.3 mm held about half, 0.4 mm almost nothing [9]. Keep layers ≤0.2 mm for joints; use the 0.30 mm draft profile only for non-structural parts [9][12].

**Perimeters vs infill.** Prusa: "The strength of a model is mostly defined by the number of perimeters (not the infill)" [12]. CNC Kitchen found strength roughly proportional to wall thickness (material in the shell) [23]. Academic tensile-bar studies sometimes rank infill higher for pure axial tension (e.g. 10→100% infill +118% vs 2→6 walls +36% in one thesis [24], seen via search summary only); bending, torsion, and bearing around holes load the shell, so walls dominate for joints. Use 4 perimeters (~1.67 mm) and 40%+ infill for load-bearing parts (house).

## 3. Overhangs, bridges, features

**Overhangs.** Prusa: 45 to 60° from vertical prints clean depending on nozzle and settings (75° only on MK4S/CORE One cooling, not MK3S) [11]. Hubs: 45° safe [16]. MK3S+ angle test: acceptable to 50°, worse beyond [17]. `support_material_threshold = 50` in the profile [2]. Design to 45°; accept up to 50° on non-mating surfaces. PETG overhangs and bridges worse than PLA [22].

**Bridges.** Sag is always present to some degree above ~5 mm [16]. MK3S+ PLA: 2 to 18 mm acceptable, 20 mm slight sag [17]. Bridges print at `bridge_speed = 25`, flow 0.95, fan 100%, `thick_bridges = 0` [2]. Rule: ≤10 mm on any surface that sets a fit; ≤18 mm elsewhere; the first bridged layer is ~0.1 to 0.2 mm low, so add that to clearance above a bridged ceiling (unverified).

**Teardrop and flat-top holes.** Replace the top of a horizontal circle with two 45° tangent lines meeting at a point r·√2 above center; optionally truncate it flat at r + ~0.2 to 0.5 mm (the flat becomes a short bridge). Required above ~8 mm diameter (house), worthwhile at any size if the top must be round-ish. Verified in build123d 0.13 here:

```python
from math import sqrt
a = r / sqrt(2)
td = Circle(r) + Polygon((-a, a), (0, r * sqrt(2)), (a, a), align=None)  # tip +Y
hole = extrude(Plane.XZ * td, amount=L, both=True)  # on Plane.XZ local +Y maps to world +Z
# flat top: td & Rectangle(2*r, 2*r + cap, align=(Align.CENTER, Align.MIN)).moved(Location((0, -r)))
```

`Polygon` defaults to `align=(Align.NONE, Align.NONE)` in this version; pass `align=None` explicitly so the points are not recentered.

**Bed edges.** Chamfer 45°, not fillet: a fillet's lower part is a near-horizontal overhang, while a chamfer prints at 45° and also hides elephant foot [16]. Chamfer 0.4 to 0.5 mm on mating bottom edges; fillets are fine on vertical edges and top edges.

**Walls and features.** Perimeter spacing = w − h(1 − π/4) = 0.407 mm, so n perimeters span 0.45 + 0.407(n − 1) mm (Prusa quotes 0.86 mm for two) [12], derived. Draw walls at those widths to avoid gap-fill. Walls thinner than one extrusion width cannot be printed [11]; Arachne (default generator in 2.7.2) varies width and drops features below `min_feature_size` (25% of nozzle) [2]. MK3S+ printed 0.2 mm walls in a test [17] but they are useless structurally. Vertical pins <5 mm are perimeter-only and weak [16]; prefer ≥5 mm or a metal pin. Ribs and snap arms: ≥2 perimeters (0.86 mm) and ideally 3 to 4.

**Gaps.** The slicer fills cracks under 2 × `slice_closing_radius` = 0.098 mm [2]. MK3S+ gap test: 0.1 mm distinguishable but unacceptable, ≥0.2 mm acceptable; on another printer 0.2 mm merged, ≥0.3 mm clean [17]. Use ≥0.3 mm for slots that must stay open (e.g. flexure slits, split clamp kerfs), ≥0.4 mm through tall parts where small XY errors stack.

## 4. Creep, heat, and annealing

**Limits.** PLA HDT 55 °C at both 0.45 and 1.8 MPa [3]; Tg 55 to 60 °C [20]; Prusa says PLA softens and deforms over 60 °C [22]. PETG HDT 68 °C [4], Tg ~80 °C [21], suitable below ~80 °C [22]. A car interior in sun or a part near a motor or hot end exceeds PLA's limit: use PETG (or ASA/PC, outside this doc).

**Creep.** Printed PLA at 15 MPa constant tension (~30% of nominal UTS), 25 °C, ruptured in 1.2 to 2.3 h across 39 parameter sets (MakerBot, ASTM D2990 bars) [19]. That is one study on a lower-end printer, but it shows PLA creeps to failure at stresses far below short-term strength. PLA's creep accelerates sharply as it approaches 55 to 60 °C; PETG is less stiff (lower modulus [5][6]) but has more thermal margin. No controlled PLA-vs-PETG long-term creep dataset was found; claims that PETG creeps less at room temperature are anecdotal. Design rules (engineering judgment, unverified):
- Keep sustained stress ≤10 to 15% of the short-term XY strength, ≤5% across layers.
- Screwed/clamped joints lose preload as plastic under the head relaxes: use washers or a flanged head to spread load, keep the clamped plastic short, put metal (inserts, sleeves, compression limiters) in the load path, and design for retightening.
- Snap fits must return to undeflected at rest; never hold a printed arm deflected.
- Press fits relax over weeks; add a mechanical lock or adhesive if retention matters.

**Annealing.** Standard PLA at 100 °C for 45 min: up to 10% change, shrinking in XY and growing in Z (50 mm became ~45 mm XY, ~55 mm Z), too variable to pre-scale [10]. XY tensile +7.5%, layer adhesion unchanged (42 kg before and after), impact unchanged [10]. Do not anneal parts with fits; if heat resistance is needed, switch to PETG or an annealable "HT" PLA (vendor claims ~1 to 3% shrink, unverified).

## 5. Perimeters around holes and joint features

- Every perimeter also wraps each hole, so `perimeters=4` gives a ~1.67 mm solid ring around every bore [12] derived. A boss around a screw or insert should be at least hole radius + 4 perimeters; pass `--set perimeters=4 --set fill_density=40%` to `tools/slice.py` for load-bearing parts (house).
- Prefer making the boss geometry itself solid: if the boss wall is ≤ 2 × perimeter span, it prints as all perimeters with no infill.
- Localized settings: PrusaSlicer modifiers (box/cylinder/sphere primitives) can change perimeters and infill per region [14]; e.g. 100% infill inside a cylinder around a fastener. A user reports extra perimeters appear on the modifier boundary [14]. Modifiers require the GUI or a 3MF project; with the CLI, global `--set` is simpler.
- Fasteners loaded in Z (screw axis vertical, pulling layers apart) are the weakest case; orient so the screw axis is horizontal or the load compresses layers.

## 6. Joint design checklist

1. Choose orientation first: loads and flexing in XY; Z only in compression. Mating faces vertical or on the bed.
2. Set clearance per side from the table; double for diameter. Holes: +0.2 to 0.3 mm. Horizontal holes: teardrop/flat top.
3. Snap Z dimensions to 0.2 mm multiples; avoid shallow (<45°) mating tapers.
4. Chamfer bed edges 0.4 to 0.5 mm; keep slots ≥0.3 mm; walls as perimeter multiples (0.86, 1.27, 1.67, 2.08 mm).
5. Overhangs ≤45°, bridges ≤10 mm over fit surfaces.
6. Keep seams off bearing and contact faces (`rear` + orientation, or painting).
7. Material: PLA below 50 °C and low sustained stress; PETG for warmth, toughness, sustained load. No annealing on fitted parts.
8. Slice load-bearing joints with 4 perimeters, ≥40% infill, ≤0.2 mm layers.
9. For any new fit, print a small test coupon (pin + bore at clearance steps of 0.05 mm) before the full part.

## Sources

1. Prusa Knowledge Base, "Elephant foot compensation." https://help.prusa3d.com/article/elephant-foot-compensation_114487
2. Local: `profiles/mk3s_pla_0.20mm.ini` and `prusa-slicer --help-fff` (PrusaSlicer 2.7.2) for defaults (`elefant_foot_compensation`, `xy_size_compensation`, `slice_closing_radius` 0.049, `min_feature_size` 25%, Arachne default, `seam_position`). Hole-compensation absence and the 7.3 mm example: Prusa forum, https://forum.prusa3d.com/forum/prusaslicer/hole-size-compensation-parameter-in-prusaslicer-when/ and https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-how-do-i-print-this-printing-help/clearance-data (forum, anecdotal; the 7.3 mm example was seen via search summary).
3. Prusa Polymers, Prusament PLA technical data sheet v1.1 (2022). https://www.matterhackers.com/r/xFvGl8
4. Prusa Polymers, Prusament PETG technical data sheet v1.1 (2022). https://www.3dprintergear.com.au/assets/files/technical-data-sheet%20(1).pdf
5. Ultimaker PLA technical data sheet v5.00. https://um-support-files.ultimaker.com/materials/2.85mm/tds/PLA/Ultimaker-PLA-TDS-v5.00.pdf
6. Ultimaker PETG technical data sheet v1.00. https://um-support-files.ultimaker.com/materials/2.85mm/tds/PETG/Ultimaker-PETG-TDS-v1.00.pdf
7. Hanon, Marczis, Zsidai, "Influence of the 3D Printing Process Settings on Tensile Strength of PLA and HT-PLA," Periodica Polytechnica Mech. Eng. 65(1), 2021. https://pp.bme.hu/me/article/download/13683/8951
8. CNC Kitchen, "The Influence of Extrusion Temperature on Layer Adhesion." https://www.cnckitchen.com/blog/the-influence-of-extrusion-temperature-on-layer-adhesion
9. CNC Kitchen, "Layer Height vs Strength of FDM Prints." https://www.cnckitchen.com/blog/the-influence-of-layer-height-on-the-strength-of-fdm-3d-prints
10. CNC Kitchen, "Better performing 3D prints with annealing, but... Part 1: PLA." https://www.cnckitchen.com/blog/better-performing-3d-prints-with-annealing-but-part-1-pla
11. Prusa Knowledge Base, "Modeling with 3D printing in mind." https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164141
12. Prusa Knowledge Base, "Layers and perimeters." https://help.prusa3d.com/article/layers-and-perimeters_1748
13. Prusa Knowledge Base, "Seam position." https://help.prusa3d.com/article/seam-position_151069
14. Prusa Knowledge Base, "Modifiers." https://help.prusa3d.com/article/modifiers_1767
15. Nophead (HydraRaptor blog), "Polyholes." https://hydraraptor.blogspot.com/2011/02/polyholes.html
16. Hubs (Protolabs Network), "How to design parts for FDM 3D printing." https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
17. Fab Academy 2024, Reykjavik lab, design-rule tests on Prusa i3 MK3S+ (PLA, 0.20 mm); some tests on a FLSUN V400. https://fabacademy.org/2024/labs/reykjavik/assignments/week05.html
18. Fab Academy 2025, Singapore lab, MK4 vs X1C clearance test (seen via search summary only; unverified). https://fabacademy.org/2025/labs/singapore/group.assignments/wk05_group.html
19. Waseem et al., "Multi-Response Optimization of Tensile Creep Behavior of PLA 3D Printed Parts," Polymers 12(12):2962, 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7764475/
20. NatureWorks Ingeo 4043D technical data sheet (Tg 55 to 60 °C, ASTM D3418; third-party copy). https://cdn.shopify.com/s/files/1/1223/5992/files/PLA_4043D_TDS.pdf
21. Eastman Eastar 6763 copolyester data sheet (Tg ~80 °C, DSC; Protolabs copy). https://protolabs.com/media/pzub5tfo/eastar-6763.pdf
22. Prusa Knowledge Base material guides, "PLA" and "PETG." https://help.prusa3d.com/article/pla_2062 and https://help.prusa3d.com/article/petg_2059
23. CNC Kitchen, "Big nozzles: how do they make your 3D prints stronger?" (strength ~ proportional to wall thickness; via search summary). https://www.cnckitchen.com/blog/big-nozzles-how-do-they-make-your-3d-prints-stronger
24. Universidad Técnica Federico Santa María thesis, "Evaluación experimental de la influencia de parámetros de impresión sobre comportamiento mecánico del PLA" (via search summary; unverified). https://repositorio.usm.cl/handle/123456789/77535
