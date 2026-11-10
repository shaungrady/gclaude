# Permanent joining and splitting parts (FDM, MK3S+, PLA/PETG/ABS/ASA)

Scope: adhesives, solvent and thermal welding, adhesive joint geometry, splitting oversize parts, embedding hardware mid-print, adhesive mounting tapes. Fasteners, snap-fits, press fits and tolerance fundamentals live in sibling files.

## Quick reference

**Adhesive per material** (strengths are joint failure loads or lap shear; printed-part joints usually fail in the print first)

| Material | First choice | Alternatives | Avoid / caveat |
|---|---|---|---|
| PLA | Thin or gel CA | 2-part epoxy (sand + IPA first), MMA | Acetone does not weld PLA. DCM consumer sale banned in US [18] |
| PETG | MMA structural acrylic, or PU construction adhesive (won Cosel's PETG test) [7] | Epoxy, CA (both broke the PETG substrate rather than the bond) [7] | Some CA brands weakened PETG [7]; wood glue and UHU general purpose scored lowest [7] |
| ABS / ASA | Solvent weld (acetone/ABS slurry) or CA | Epoxy after sanding | Epoxy on unsanded ASA: ~25 % of CA's joint load [5] |

- CA on ASA (lap shear, 25.4 mm overlap, 0.06 mm bondline): 1810 N, equal to an unjointed printed control (1950 N); failure in the print. Epoxy (Loctite E-20HP): 470 N, adhesive failure; 808 N after 320-grit sanding [5]. That works out to about 2.8 MPa CA vs 0.7 to 1.25 MPa epoxy *if* the specimen was the D3163-standard 25.4 mm wide (width not stated in text; my calculation).
- Loctite 401 datasheet lap shear (ISO 4587): ABS 7.5 MPa, PC 9.6, PVC 10, all with substrate failure; Loctite 406 on ABS 8.8 MPa; 454 gel on ABS 8.3 MPa [3]. Molded plastics; printed parts give lower values.
- Stratasys ABS, double-butt-lap: hot air welding 40 to 100 % of the unjointed part's strength (best), solvent (Proweld) 40 to 59 %, CA 20 to 39 %, epoxies mostly 0 to 39 % [6].

**Glue gaps**
- Thin CA (401): max gap 0.15 mm [4]. Gel CA (454): 0.25 mm [4]; up to 1.0 mm only with activator, per a distributor (unverified) [4].
- Epoxy/MMA: design 0.1 to 0.2 mm. Thinner is stronger: 0.25 → 1.0 mm bondline cost 16 % of shear strength (CFRP adherends) [9]. Yap used 0.06 mm spacers [5].
- As-printed faces have Ra ≈ 13 µm, Rz ≈ 120 µm (ASA). Sanding with 320 grit gave Ra 5 µm, Rz 75 µm [5], so flat faces with "zero" gap already have ~0.1 mm of voids.

**Alignment features (defaults to start from)**
- PrusaSlicer cut-tool connectors (3.0.0-alpha14 source): size (diameter) 2.5 mm, depth 3 mm, depth tolerance 0.1 mm, size tolerance **0 mm** (hole = pin; set 0.2 to 0.4 mm yourself), snap bulge 15 % of radius (range 5 to 15), snap space 30 % (10 to 50), dovetail flap angle 60°, groove width = 4 × depth, groove depth = max(1 mm, 0.5 × handle size) [1].
- Own pins and keys: 0.1 mm per side for glued alignment (snug), 0.2 mm per side for dry slip (repo CLAUDE.md design rules). Pin engagement ≥ 1 × diameter per side (engineering judgment, unverified).

**Mounting tapes**
- VHB (B23F/G23F): design 12 psi (85 kPa) dynamic, **0.25 psi (1.7 kPa) static** = 60 cm² of tape per kg of constant load, safety factor > 5 [10]. Apply ≥ 15 psi (100 kPa) pressure, at ≥ 15 °C (60 °F) [10].
- Dual Lock 250↔400 (SJ3560/SJ3561): tensile engagement 60 psi, disengagement 107 psi, shear 70 psi, cleavage 28.5 lb/in, 90° peel 5.4 lb/in, static hold ≥ 2.2 lb/in² [11]. Wait 24 h before loading [11].
- Command strips: smooth surfaces only, not textured, brick or wallpaper; wait 1 h; apply above 10 °C; softens above 40 °C [12]. Large picture strip: about 4 lb per strip pair, but retailers list 15 or 16 lb for 4 pairs (conflict) [13].

## 1. Cyanoacrylate (CA)

**When**: small, tight-fitting joints, fast assembly, PLA/ABS/ASA. Best measured performer on ASA [5].
**Rules**
- Thin CA for fits ≤ 0.15 mm; gel for ≤ 0.25 mm and vertical faces [4].
- Activator speeds cure in big gaps but "can reduce ultimate strength"; test first [3]. Cure speed falls with gap and low humidity [3].
- Polyolefin primers (e.g. Loctite 770) are for PP/PE; PLA, PETG and ABS don't need them (general Loctite guidance, no source checked here). Clean with IPA [5].
- Service temperature: general-purpose CA is good to about 82 °C [5]; the 2012 reformulated 401 is rated higher [3].
- Heat post-cure (80 °C, 24 h) gave mixed results with CA [5]; skip it, especially on PLA (softens near 60 °C).
**Failure modes**: brittle in peel and impact; white blooming; some brands weaken PETG [7]. CNC Kitchen's PLA-copolyester hooks: thin CA ~58 kg vs 53 kg for an unglued print in the strong orientation; thick CA only slightly better [8].

## 2. Two-part epoxy

**When**: gap filling (0.1 to 0.5 mm), larger areas, potting, water exposure.
**Rules**: sand (320 grit) and solvent wipe; this raised epoxy joint load by 70 % on ASA and 54 % on nylon-CF [5]. Clamp with spacers. Heat post-cure helps epoxy [5], but PLA won't tolerate 80 °C.
**Failure modes**: adhesive (interface) failure on smooth or unsanded prints [5][6]; peel. Thomas Sanladerer found epoxy among the best on PLA, with the print failing first (secondhand via All3DP; unverified).

## 3. Structural acrylics (MMA) and polyurethane

MMA adhesives and Bostik P580 PU construction adhesive scored highest on PETG lap specimens in Cosel's test (values only in the video graphic; reviewers noted specimen bending, so not pure shear) [7]. Use MMA when PETG must carry load. PU foams and expands, so clamp it. Not quantified here: specific MMA products and their strength on PETG (unverified).

## 4. Solvent welding

- **ABS/ASA + acetone**: brush both faces, or use "ABS slurry" (scrap dissolved in acetone) as a gap filler. A dissolved-ABS-in-acetone adhesive reached 8.69 MPa lap shear, above commercial CAs (search abstract only; paper not read, unverified). Solvent weld on ABS blends: 40 to 59 % of parent strength [6]. Let the solvent flash off; trapped solvent leaves a soft joint for days.
- **PLA / PETG**: acetone does not work. DCM dissolves both, but the US EPA banned all consumer DCM in 2024 for unreasonable health risk [18]. Don't specify it.
- Design: flat mating faces with no gap, so solvent wicks in by capillary action; add alignment pins (sec. 7).

## 5. Thermal welding (friction / spin, hot air, 3D pen)

- **Hot air welding** with filler rod was the strongest method in [6] (40 to 100 % of parent); literature cites up to 90 % of parent [6]. Ultrasonic spot welds: 20 to 39 % [6].
- **Friction (rotary tool) welding**: chuck filament in a rotary tool (1/16 in collet for 1.75 mm) and run it along a V-seam. Reported qualitatively as failing beside the seam [19]. A rotary friction welding study on printed PLA reported ~11.1 MPa at 600 rpm (preprint, unverified) [19].
- **3D pen**: same filler-into-V-groove idea at lower energy. No measured strengths found (gap).
- **Design**: chamfer both edges 45° to form a 90° V groove, ~1.5 to 2 mm deep, so filler fuses into wall plastic, not a surface skin (engineering judgment). Use same-material filler. Weld PLA to PLA only.

## 6. Adhesive joint geometry

- Load adhesives in **shear or compression**, never peel or cleavage. Butt joints on a 1.2 mm wall give tiny area and put the layer interface in tension.
- Ranking: socket/sleeve ≥ double lap ≥ scarf > single lap >> butt. Single laps peel at their ends from eccentric load (general adhesives practice).
- Overlap: strength per area falls as overlap grows. 12.5 → 50 mm lap reduced average shear strength 54 % (CFRP) [9], so the load capacity rises sub-linearly. Prefer wider over longer.
- Sizing: A ≥ SF × F / τ. For as-printed PLA/PETG/ASA take τ ≈ 1 MPa (epoxy, unsanded) to 2.5 MPa (CA) from [5], SF 2 to 3. Example: 200 N with CA, SF 3 → 240 mm² (e.g. 12 × 20 mm).
- Print orientation: the bonded face's layer lines set the strength because the print usually fails before the glue [5]. Make the bonded face a top or bottom skin (100 % solid), not a wall of layer ends. Orientation effects on PLA lap joints exist but the published results conflict (Kovan 2017, unverified).
- **Glue groove**: a 1 × 1 mm channel 1 to 2 mm in from the edge catches squeeze-out and stores excess (engineering judgment). Keep at least one positive stop so the bondline cannot squeeze to zero.

```python
from build123d import *
# Socket joint: tube end glued into a sleeve. 0.1 mm radial glue gap.
tube_od, gap, wall, depth = 20.0, 0.1, 2.4, 15.0
sleeve = Cylinder(tube_od / 2 + gap + wall, depth + 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
sleeve -= Pos(0, 0, 3) * Cylinder(tube_od / 2 + gap, depth, align=(Align.CENTER, Align.CENTER, Align.MIN))
# 3 mm floor = positive stop; print the sleeve upright so the bore walls are perimeters
```

## 7. Splitting parts that don't fit

**Where to cut**
- Where bending moment and stress are low: near supports or mid-span of a short cantilever is bad; away from holes, fillets and hooks.
- Along existing features or edges, so the seam reads as a design line and is hidden.
- So each piece has a large flat face for the bed, and its critical faces (mating, cosmetic) print down or as perimeters. Make the cut face the bed face where possible: it then comes out dead flat and solid.
- Offset cuts in multi-piece assemblies (brick pattern) so seams don't line up.

**Alignment features**
- Dowels: separate printed or steel pins. Steel dowel pins (e.g. 3 × 10 mm) are stiffer and truer than printed ones. Print holes vertically (round); horizontal holes come out oval.
- Plugs: pin on one half, hole on the other. The pin is weak if its layers are across its axis; prefer dowels when the cut plane is vertical.
- Tongue-and-groove or dovetail along long seams: groove 0.1 mm per side wider for glue, 0.2 mm for dry fit.
- Registration bumps (hemispherical, 2 to 3 mm) for cosmetic shells with little load (judgment).

**PrusaSlicer cut tool** [1][2]
- Modes: planar (any angle) and dovetail. Connectors: **Plug** (added to one side, subtracted from the other), **Dowel** (holes in both sides plus a separate pin object), **Snap** (snap-fit plug). Shapes: prism or frustum; circle, square or hexagon [2].
- Defaults and tolerance mechanics (source): size 2.5 mm, depth 3 mm, size tolerance 0, depth tolerance 0.1 [1]. Only the hole grows: diameter + size tolerance, depth + depth tolerance (plug), or + 2 × depth tolerance total for dowels, which centers the pin [1]. With the default 0 size tolerance, the pin and hole are nominally identical, so set 0.2 to 0.4 mm for PLA.
- Dovetail groove defaults: flap angle 60°, width 4 × depth [1]. Not available with "cut into parts" [2].
- Dowel option must be chosen before placing connectors (forum report) [2]. Defaults may differ in 2.6 to 2.9 (not checked).
- Prefer modeling joints in build123d: you control clearance, orientation and chamfers.

```python
from build123d import *
# Lower half of a split box; cut plane is its top face (z = 20). Two dowel holes.
half = Box(120, 60, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))
pin_d, engage, clr = 5.0, 8.0, 0.2          # clr on diameter; glued: 0.2, dry slip: 0.4
for x in (-45, 45):
    half -= Pos(x, 0, 20 - engage) * Cylinder((pin_d + clr) / 2, engage + 0.01,
                                              align=(Align.CENTER, Align.CENTER, Align.MIN))
# Mirror for the upper half, then flip it so its cut face also prints on the bed.
```

## 8. Embedding hardware during a pause

- PrusaSlicer: preview → vertical slider → "+" → Pause print (M601). The pause is inserted **before** the selected layer [14]. Requires PrusaSlicer ≥ 2.2; not with sequential printing [14]. Users report off-by-one layer picks, so check the preview [14][15].
- Pocket clearance: 0.15 mm in all directions (MK3S, 0.4 mm nozzle, 0.15 mm layers) [15]. Make the pocket top land on a layer boundary, and set the pause at the first layer above the pocket. For appearance, 2 to 3 layers of cover are enough; for strength, put the pocket deeper [15].
- Magnets: a drop of CA keeps them from jumping to the nozzle or printer steel; mark polarity [15]. The MK3S steel sheet pulls magnets down (helpful). N-grade NdFeB max 80 °C; use SH grade (150 °C) near heat [17].
- Large metal inserts: spread glue stick on them so filament sticks [15]. Use a pre-printed cap over the cavity to make a flat surface for the next layer ("gap-cap") [16].
- Threaded rod or steel bar through long thin parts adds stiffness. Use a printed channel 0.3 to 0.5 mm over the rod diameter plus epoxy, or insert it during a pause [15] (clearance is judgment).
- Retention without a pause: press fit (see press-fit file) or CA in an open pocket. Pull-out depends on the adhesive, not the magnet.

```python
import math
from build123d import *
part = Box(40, 40, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
mag_d, mag_h, layer, z0 = 6.0, 3.0, 0.2, 2.0      # z0 on a layer boundary
pocket_h = math.ceil((mag_h + 0.15) / layer) * layer
part -= Pos(0, 0, z0) * Cylinder(mag_d / 2 + 0.15, pocket_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
pause_z = z0 + pocket_h   # pause before the layer that prints at this height
```
Check the actual layer heights in the preview. The 0.20 mm profile has a 0.2 mm first layer, but variable layer height or the 0.15 profile shifts them.

## 9. Adhesive-backed mounting (VHB, Dual Lock, Command, hook-and-loop)

- **Ratings in context**: VHB short-term shear is ~65 psi, but the long-term static design value is 0.25 psi [10]. Size static (hanging) loads from the static value: 60 cm²/kg [10]. Dual Lock static hold ≥ 2.2 lb/in² (~155 g/cm²) [11].
- **Peel and cleavage are weakest**: Dual Lock cleavage 28.5 lb/in and 90° peel 5.4 lb/in of width, against 60 to 70 psi in tension or shear [11]. Design the mount so the load is shear along the wall, with the tape area centered under the load and a stiff back plate (≥ 3 mm) so it can't flex into peel.
- **Ceilings**: tape is in tension and creeps; 3M applies the same 0.25 psi to static *tensile* loads [10]. Add a mechanical backup for anything over the 60 cm²/kg rule or anything that could hurt someone. No 3M ceiling guidance found for Command (gap).
- **Printed surface**: PSAs need smooth, flat contact. Use the **bed face** (smooth PEI or glass sheet) or an ironed top face as the tape face. Avoid textured-sheet faces, walls and infill-side top surfaces (Command: "smooth surfaces only" [12]). Make it a single flat pad with no text or chamfer inside the tape area. PET and ABS are medium surface energy, good for VHB 5952 (3M brochure, via search; PLA/PETG not listed, unverified) [20].
- **Prep and cure**: IPA wipe, not household cleaner [12]; pressure ≥ 15 psi [10]; Command 1 h before loading [12]; Dual Lock 24 h [11]; VHB builds strength over ~72 h (typical 3M guidance, unverified here).
- **Heat**: Command softens above 40 °C [12]; VHB B23F holds static load to 93 °C [10]. PLA mounts in sun or a car fail by creep of the PLA first.

## Gaps and conflicts

- No measured lap shear data found for CA or epoxy on printed PLA or PETG with stated area; values are inferred from ASA [5] and molded ABS [3].
- PETG CA compatibility: brand-dependent [7]; test before relying on it.
- Command large strip rating: 15 vs 16 lb per 4 pairs [13].
- PrusaSlicer defaults come from 3.0.0-alpha14 source; 2.x releases not verified.
- Friction-weld and 3D-pen strengths are qualitative or unverified.

## Sources

1. PrusaSlicer source (master, v3.0.0-alpha14, Nov 2026): `src/slic3r-shared/include/Slic3r/App/Plater/CutDialog.hpp`, `CutGizmo.hpp/.cpp`, `src/slic3r-shared/src/Slic3r/Biz/Utils/CutUtils.cpp`, `src/slic3r-domain/include/Slic3r/Domain/CutConnector.hpp`. https://github.com/prusa3d/PrusaSlicer
2. Prusa Knowledge Base, Cut tool. https://help.prusa3d.com/article/cut-tool_1779 ; forum on dowel ordering: https://forum.prusa3d.com/forum/english-forum-original-prusa-i3-mk4-hardware-firmware-and-software-help/cant-get-dowels-to-not-be-inside-the-part-e-g-separate-objects-to-arrange
3. Henkel, Loctite 401/406/454/495 TDS (2012 reformulation). https://www.ellsworth.com/globalassets/literature-library/manufacturer/henkel-loctite/henkel-loctite-401-406-454-and-495-reformulation.pdf
4. Henkel product pages: Loctite 401 (gap fill 0.15 mm) https://henkel-adhesives.com/us/en/product/instant-adhesives/loctite_401.html ; Loctite 454 (0.25 mm) https://next.henkel-adhesives.com/us/en/products/industrial-adhesives/central-pdp.html/loctite-454/BP000000153575.html
5. Yap et al., "Evaluation of structural epoxy and cyanoacrylate adhesives on jointed 3D printed polymeric materials," Int. J. Adhesion & Adhesives 100 (2020) 102602. https://doi.org/10.1016/j.ijadhadh.2020.102602
6. Espalin et al., "Analysis of bonding methods for FDM-manufactured parts," SFF Symposium 2010. https://utw10945.utweb.utexas.edu/Manuscripts/2010/2010-04-Espalin.pdf
7. Hackaday, "Comparing adhesives for gluing PETG prints" (2025), on Cosel's test https://hackaday.com/2025/01/30/comparing-adhesives-for-gluing-petg-prints/ ; video https://www.youtube.com/watch?v=tyo8vLorpZo
8. Hackaday, "Stronger 3D prints: glue or carbon fiber?" (2019), on CNC Kitchen. https://hackaday.com/2019/12/28/stronger-3d-prints-glue-or-carbon-fiber
9. Chen et al., "Parametric investigation into the shear strength of adhesively bonded single-lap joints," Materials 15 (2022) 8013. https://pmc.ncbi.nlm.nih.gov/articles/PMC9694882/
10. 3M VHB Structural Glazing Tapes B23F/G23F technical data. https://multimedia.3m.com/mws/media/411785O/3m-vhb-structural-glazing-tapes-b23f-and-g23f-technical-data-sheet.pdf
11. 3M Dual Lock SJ3560/SJ3561/SJ3562 technical data (Dec 2002). https://datasheet.chipsmall.com/SJ3560/464230.pdf
12. 3M Command Strips FAQ (2012). https://service.mattel.com/instruction_sheets/3M%20Command%20Strips%20FAQs%20V1052.pdf
13. Retail listings, Command 17206: https://www.staples.ca/products/930654-en-command-picture-hanging-strips-large-white-4-pack ; https://www.staples.com/command-large-picture-hanging-strips-white-4-pairs-pack-17206-es/product_884356
14. Prusa Knowledge Base, Insert pause or custom G-code at layer. https://help.prusa3d.com/article/insert-pause-or-custom-g-code-at-layer_120490
15. Prusa Blog, Practical uses of color change in PrusaSlicer. https://blog.prusa3d.com/practical-uses-of-color-change-in-prusaslicer_59563/
16. Hackaday, "Use a gap-cap to embed hardware" (2026). https://hackaday.com/2026/03/27/use-a-gap-cap-to-embed-hardware-in-your-next-3d-print/ ; original https://www.digikey.com/en/maker/blogs/2025/embedding-objects-inside-a-3d-print
17. K&J Magnetics, ST4 specs (N grade 80 °C) https://www.kjmagnetics.com/st4-neodymium-star-magnet ; D42SH (SH 150 °C) https://kjmagnetics.com/d42sh-neodymium-high-temp-disc-magnet
18. US EPA, Risk management for methylene chloride (2024 final rule). https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/risk-management-methylene-chloride
19. Vaasa Hacklab, Friction welding 3D prints (2016) https://vaasa.hacklab.fi/2016/06/15/friction-welding-3d-prints ; Scorchworks, Friction welding with a Dremel https://www.scorchworks.com/Blog/?p=442 ; rotary friction welding of PLA preprint https://archive.umsida.ac.id/index.php/archive/preprint/view/11393 (unverified)
20. 3M VHB LSE series brochure (surface energy classes). https://multimedia.3m.com/mws/media/1801882O/3m-vhb-tape-lse-series-brochure.pdf
