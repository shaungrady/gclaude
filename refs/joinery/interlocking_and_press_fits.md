# Interlocking joints and interference fits (FDM, 0.4 mm nozzle, PLA/PETG)

Scope: joints held by geometry, friction, or interference only (fasteners, glue, snap hooks are in sibling files). Numbers are **CAD dimensions**. "Per side" = gap on one face; "diametral" = difference in diameters. **[derived]** = geometry worked out here, not measured; **[unverified]** = no primary source found.

## Quick reference

| Need | CAD value (start here, then coupon-test) | Source |
|---|---|---|
| Sliding fit (rail, dovetail, lid in groove), per side | PLA 0.15–0.25 mm, PETG 0.2–0.3 mm | [5] |
| Moving joint that must break free, per side | 0.15 mm (horizontal axis), 0.15–0.2 mm (vertical axis); PETG needs the larger value | [2] |
| Hinge/moving part first try (Prusa) | ≥ 0.3 mm clearance | [8] |
| Large/unknown-quality interlocking part (conservative) | 0.5 mm | [6][7] |
| Press fit, generic, per side | 0.05–0.15 mm interference | [5] |
| Press fit, hand vs vise, diametral | light 0.1–0.2 mm; tight 0.4–0.6 mm (tight value is high for PLA, see text) | [1] |
| Steel dowel into printed hole | Press: CAD hole = pin d + 0 to +0.1 mm. Snug/slip: d + 0.25 to +0.3 mm | [11][12], see §2 |
| Bearing seat, PETG (peer-reviewed) | 0.2 mm diametral CAD interference: ~600 N to press in, ~300 N to pull out | [4] |
| 608 bearing (22 mm OD), vertical axis bore | 22.0–22.1 mm press; 22.3 mm + crush ribs for a forgiving fit; tune in 0.05 mm steps | [4][12][17], **[derived]** |
| Dovetail, per flank (normal to the flank) | 0.1–0.2 mm locating; 0.2–0.3 mm free sliding | [2][5][13] |
| Tapered dovetail taper | 1–2° per side (print); wood uses 0.25–0.5° | [14][15] |
| Puzzle/tongue offset | 0.2 mm small parts, 0.4 mm large parts (SLA data; add for FDM) | [7] |
| Filament (1.75 mm) as pin | 2.0–2.1 mm hole; 1.85 mm reported too tight | **[unverified]** community |

Even with accurate outer dimensions, holes print ~0.1–0.3 mm undersize [10][12]; chamfer bed-side mating edges 0.4 mm for elephant foot.

## 0. Universal rules

- **Holes print small, pegs print large.** A 45 mm hole printed 44.80 mm on a calibrated PLA printer; matching ISO 286 clearance fits needed a slicer hole expansion of 0.13 mm (per side) [10]. One fit-test model reports press fit at 0.00 mm offset and sliding from +0.20 mm [12]. So "nominal hole = press fit" is a reasonable first guess for XY holes.
- **Orientation changes the fit.** The same joint needed 0.15 mm horizontal vs 0.2 mm vertical in PETG on a Prusa MK4S [2]. Coupon-test in the part's orientation [13].
- **Layer adhesion is the weak axis.** Standing (Z) vs lying tensile: PLA 37–40 vs ~60 MPa (≈65%) at 200–250 °C; PETG 30–32 vs 55 MPa (≈55–58%) at 230–245 °C, worse when printed cold [9]. Features loaded across layers (vertical pegs, Z-stacked dovetail necks) fail there first.
- **Interlocks are much weaker than solid.** In a PLA tensile study (100% infill, 0.2 mm layers) the best interlock (C-shaped, 5 mm neck) reached 7 MPa, only ~16% of the 44.4 MPa solid specimen; dovetail and T-shapes were weaker. Thickening the neck to 7 mm *reduced* strength [22]. Size interlocks for location and shear, not for primary tension.
- **Repeated assembly loosens interference.** Second press-in of the same PETG seat needed ~33% less force and pull-out dropped ~17% [4]. Printed press fits are effectively single-use.
- Chamfer or radius lead-in edges: eases assembly and reduces stress concentrations [6][8].

## 1. Sliding joints: dovetails, T-slots, rails

**When:** location and retention in two axes, assembly along the third (slides, swappable mounts, lids). The slide axis needs an end stop.

**Geometry and play [derived].** Let α = flank angle from the normal to the base (the undercut angle), c = clearance normal to each flank.
- Lift-off play (normal to base): Δz = c / sin α. At c = 0.2 mm: α = 15° → 0.77 mm; 30° → 0.40 mm; 45° → 0.28 mm. Small woodworking angles (1:6 ≈ 9.5°) give large play in plastic; **use α = 30–45°**.
- Lateral play when seated on the floor: ±c / cos α. Under lift-off load both flanks contact and the joint self-centers with zero lateral play.
- To get flank clearance c from a horizontal offset, widen the cutter by c / cos α per side (see snippet).
- Leave a floor gap ≥ c so the flanks, not the floor, set the fit.

**Layer stepping on angled flanks [derived].** Printed with layers crossing the flank (profile standing in XZ), each layer is a vertical step. PrusaSlicer slices at mid-layer, so the surface deviates by ±(h·tan α)/2 horizontally, i.e. ±(h·sin α)/2 normal to the flank: ±0.05 mm at h = 0.2 mm, α = 30°; ±0.07 mm at 45°. Steps on the two parts don't nest unless both print the same way, so budget an extra ≈ h·sin α/2 per flank, or use 0.15 mm layers for the joint. Printing the profile flat in XY (slide axis vertical) eliminates stepping: perimeters trace the exact profile.

**Print orientation.**
- *Slide axis horizontal, base on bed* (default for long rails): male tail flanks overhang outward at α; female undercut flanks overhang inward at α. Both fine for α ≤ 45° [8]. No ceiling, no supports. Lift-off load then runs across layers through the tail neck: make the neck ≥ 4–5 mm and fillet its root [22].
- *Slide axis vertical:* most accurate profile, every layer is a complete interlock, lift-off load acts in-plane (strong). Sliding friction and any bending of the rail act across layers. Good for short (< ~40 mm) high-load joints.
- **T-slots:** printed with the slide axis horizontal, the T-head ceiling is a flat bridge. Keep it ≤ 10 mm (CLAUDE.md) or, better, replace the flat underside with 45° faces (a "dovetail-T"); or print slide-axis vertical.

**Length.** Engagement ≥ 1.5× the joint width resists racking **[unverified rule of thumb]**. Long straight dovetails bind from straightness error; prefer more clearance (0.25–0.3 mm) beyond ~100 mm, or taper.

**Taper / wedge-locking dovetail.** Taper the width along the length so it slides freely and locks in the last few mm. Print guide: 1–2° per side [14]. Woodworking uses 0.25–0.5° per side [15], but the take-up travel to close clearance c is c / tan(taper) [derived]: c = 0.2 mm at 1° → 11.5 mm; at 0.5° → 23 mm. Larger print tolerances therefore favor 1–2°. The taper self-locks if its angle < atan(μ); for PLA-on-PLA μ is roughly 0.2–0.4 **[unverified]**, so 1–2° per side is self-locking and needs a tap to release. A printed sliding-dovetail lock defaults to 0.45 mm clearance (0.55 mm if it binds) and must print flat, not tilted [16].

**End stops and detents.** Blind the female channel at one end (a 2–3 mm wall) for a hard stop. For a friction detent, reduce clearance to ~0 over the last 3–5 mm, or add a 0.2–0.3 mm bump on a flexing tongue **[unverified; flexing detents belong to the snap-fit file]**.

**Failure modes:** neck tears along layers; elephant foot binds the bottom flank; wear-in and creep loosen it.

```python
from build123d import *
import math

def tail_pts(w_root, h, alpha_deg, c=0.0):
    """Dovetail trapezoid for Plane.XZ (local y = global Z). Narrow root at y=0,
    flaring by alpha from vertical. c = clearance normal to each flank."""
    t, dx = math.tan(math.radians(alpha_deg)), c / math.cos(math.radians(alpha_deg))
    w0, w1 = w_root + 2 * dx, w_root + 2 * h * t + 2 * dx
    return [(-w0 / 2, 0), (w0 / 2, 0), (w1 / 2, h), (-w1 / 2, h)]

L, H, A, C = 40, 5, 30, 0.2           # length, tail height, flank angle, clearance
male = Box(30, L, 6, align=(Align.CENTER, Align.CENTER, Align.MIN))
male += Pos(0, 0, 6) * extrude(Plane.XZ * Polygon(*tail_pts(10, H, A), align=None),
                               amount=L / 2, both=True)          # slide axis = Y
female = Box(30, L, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
groove = [(x, 10 - y) for x, y in tail_pts(10, H + C, A, C)]      # opening at top face, floor gap C
female -= extrude(Plane.XZ * Polygon(*groove, align=None), amount=L / 2 + 1, both=True)
```
Both parts print base-down without supports (snippet tested in build123d 0.13). For a taper, loft two profiles with different `w_root`.

## 2. Pins and dowels

**Steel dowel pins (preferred for shear and wear).** Use vertical-axis holes (rounder, more accurate).
- Press fit: CAD hole at nominal to +0.1 mm diametral; printed undersize supplies the interference [10][12].
- Tight/snug: +0.26 mm diametral (0.13 mm per side), or +0.36 mm if a small gap is fine; use solid infill around the hole so it can be drilled/reamed [11]. Drilling or reaming to final size is the most repeatable route for precision seats [26].
- Sources disagree by ~0.2 mm on what "nominal" yields; always run a coupon (§7).
- Wall around a pressed pin: ≥ 4 perimeters (1.8 mm) [8], more for PLA, which cracks rather than yields [1].

**Printed pins.** Print **horizontally** (pin axis parallel to bed) so bending and shear run along the extrusions. Vertical pins break between layers (≈55–65% strength across layers [9]); horizontally printed dowels gave higher joint moment capacity than vertical ones in a 3D-printed furniture-dowel study (ABS/ASA) [23]. Fix the round-pin problems of horizontal printing: add a flat of 0.3–0.5 mm on the bed side (kills elephant foot and gives adhesion), and let the top be pointed/teardrop or accept a slightly oval top **[derived]**. Make pins short and thick and fillet the root [30]. Pin-to-hole clearance: use sliding values (0.15–0.3 mm per side) for removable pins.

**Filament as pin.** 1.75 mm filament makes a captive hinge axle; a hole of 2.0–2.1 mm is common in tested designs, 1.85 mm reported too tight **[unverified, community]**. PLA filament embrittles with age; prefer PETG filament or a steel pin [29].

```python
d, l, flat = 5.0, 30.0, 0.4                     # horizontal printed pin with a bed flat
pin = Pos(0, 0, d / 2 - flat) * (Rot(90, 0, 0) * Cylinder(d / 2, l))   # axis along Y
pin &= Box(d, l, d, align=(Align.CENTER, Align.CENTER, Align.MIN))     # trim below z=0
```

## 3. Press fits, crush ribs, bearing seats

**Amounts.** Generic: 0.05–0.15 mm per side [5]; light (hand) 0.1–0.2 mm and tight (vise) 0.4–0.6 mm diametral [1]. The 0.4–0.6 mm figure has no test behind it and risks cracking PLA hoops; treat > 0.3 mm diametral as needing a compliant feature. Force scales steeply with interference ("tiny changes can double the press force") [26]; Bottini & Boschetto showed FDM assembly force tracks a "real interference" that includes surface roughness/peaks, which depends on build orientation [25].

**Measured bearing seat (PETG, peer-reviewed) [4].** 25.8 mm CAD bore for a 26 mm OD bearing (0.2 mm diametral nominal interference), Cura, 0.2 mm layers, 3 walls, 3 top/bottom, 20% gyroid, 235 °C. Press-in peak ≈ 600 N, pull-out ≈ 300 N. Second cycle: ≈ 400 N in, < 250 N out. Note: the paper calls this a "608", but a 608 is 22 mm OD; 26 mm OD is a 6000. The interference figures stand either way. For a 608 with the bore axis vertical, scale to 22.0–22.1 mm CAD for press and trial in 0.05 mm steps (community 608 parts ship ±0.05 mm variants) **[derived from 4, 12]**.

**Design rules for bearing seats.**
- Print the bore axis vertical (round, accurate perimeters). Add a lead-in chamfer [26] (0.5 mm × 45°) and a 1–1.5 mm bottom shoulder **[derived]**.
- Bearing makers warn that excessive press fit removes the bearing's internal clearance [24]; igus specifies H7 bores for its plastic bushings [24].
- Plastic creeps: check the fit again 10–30 min after pressing [26]; nylon creep made press-force prediction unreliable in an MIT dowel study [27]. For long life, add axial retention (shoulder + lip, clip, or cap) rather than relying on the press alone.
- Prefer PETG for seats: PLA is stiffer and cracks; PETG/nylon tolerate strain but creep [1].

**Crush ribs.** Small axial ribs inside an oversized bore; only the ribs touch, so a missed interference is forgiven [17]. Use 3 or more [19]. Injection-molding practice: ~2.5 mm diameter rib, ~0.25 mm interference [20]. A tester found the fit came mainly from the bore wall flexing inward, not rib crushing, and that infill under the wall acts as ribs that resist it [18, via search summary, page not opened]. Ribs are single-use once crushed; Slant 3D's "grip fins" (thin flexing fins) are reusable [21]. Ribs concentrate bearing load on lines; heavy radial loads crush them further and loosen the seat (Hackaday commenter, [17]). Suggested printable start **[unverified, derived]**: bore = OD + 0.3 mm, 6 semicircular ribs r = 0.5–0.6 mm (≥ 1 extrusion wide), rib tips on a circle OD − 0.2 to −0.3 mm.

```python
D, W, n, r_rib, gap, intf = 22.0, 7.0, 6, 0.6, 0.3, 0.25   # 608 seat, bore axis = Z
hub = Cylinder(16, W + 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
hub -= Pos(0, 0, 2) * Cylinder((D + gap) / 2, W, align=(Align.CENTER, Align.CENTER, Align.MIN))
hub -= Cylinder(D / 2 - 1.5, 2, align=(Align.CENTER, Align.CENTER, Align.MIN))   # 1.5 mm shoulder
for i in range(n):
    hub += Rot(0, 0, i * 360 / n) * Pos(D / 2 - intf + r_rib, 0, 2) * \
           Cylinder(r_rib, W, align=(Align.CENTER, Align.CENTER, Align.MIN))
```
(Add the entry chamfer before export.)

**Slotted / compliant press features.** Splitting a boss or pin with a 0.5–1 mm slot turns hoop stress into beam bending and tolerates 2–3× the interference **[unverified]**; slot along layers (axis vertical for a split boss) so the halves bend in-plane. Hexagonal holes for round parts also limit contact to six lines and reduce press force [21].

## 4. Keyed, puzzle, tongue-and-groove, mortise-and-tenon, finger joints

- **Tolerances.** FDM interlocks: 0.5 mm conservative (Hubs, Formlabs) [6][7]. Formlabs puzzle example: 0.2 mm offset for small parts, 0.4 mm for large, at a 65° cutout (SLA; use the upper end for FDM) [7]. A printed PLA rotating (finger-prosthesis) joint was stiff at 0.4 mm, smooth at 0.5 mm [28]. Locating (non-moving) joints can use 0.1–0.2 mm per side because they don't need to slide after assembly [3].
- **Puzzle/jigsaw (splitting panels):** knob neck ≥ 5 mm; neck shape matters more than size (C-shape beat dovetail and T-shapes; 7 MPa best vs 44.4 MPa solid) [22]. Print panels flat so the knob lies in XY and loads stay in-plane.
- **Tongue-and-groove:** sliding clearance per side (§Quick ref); tongue ≥ 3 perimeters thick (1.35 mm minimum, ≥ 2 mm loaded, per CLAUDE.md). Chamfer the tongue tip 0.3–0.5 mm.
- **Mortise-and-tenon:** use square tenons; round tenons suffer layer stepping on FDM [7]. Print the tenon so its length lies in XY (horizontal) if it carries bending. A through-tenon with a cross wedge (tusk tenon) gives a fastener-free, re-tightenable joint (§5).
- **Finger/box joints for printed panels:** thin comb fingers break easily [7]; make fingers ≥ 3 mm wide and ≥ the panel thickness long **[unverified]**, print panels flat so fingers are in XY.
- **Keys:** a multi-key joint stacks tolerance errors; keep to one or two keyed features [7].
- **Bayonet/twist-lock (non-snap):** L-shaped slot with lugs that ride a ramp; a 2–5° helical ramp in the locking leg draws the parts together, and friction or a compressed gasket holds them. Print the axis vertical so the lug and slot are full perimeters in XY; lug ceilings in the female become bridges, so keep them ≤ 10 mm wide or chamfer 45°. **[unverified: no measured source found]**

## 5. Wedge, cam, friction, and self-tightening joints

- **Wedges and tapers:** below the friction angle (atan μ) a taper self-locks; 1–2° per side on prints [14] (§1). Use for tapered dovetails, cross-wedges through tenons, wedge-clamped rails. Print wedges flat so driving loads run along layers.
- **Cam locks:** an eccentric of offset e moves the follower 2e over a half turn; keep the cam's local slope below the friction angle so it stays put, and print the cam disc flat (XY) so its working edge is perimeters **[derived/unverified]**.
- **Friction fits** (lids, plugs): 0.0–0.1 mm per side **[derived from 5]**, or one thin flexible lip; they loosen with cycles [4] and creep [26].
- **Joints that tighten under load:** a dovetail or hook loaded away from its base wedges and self-centers [derived, §1]; orient hooks/undercuts so service load pulls them into engagement, and so the loaded section is in XY.

## 6. Which load each joint should carry

| Joint | Good for | Avoid | Orientation for strength |
|---|---|---|---|
| Dovetail/T-rail | lift-off + lateral location, shear along base | axial pull (needs stop), bending of long rails | tail neck in XY, or slide axis vertical |
| Steel dowel | shear, location | axial retention by friction alone | hole axis vertical |
| Printed pin | light shear, hinges | cyclic bending | pin printed horizontal |
| Press fit/bearing | radial location, moderate axial | repeated disassembly, sustained heat | bore axis vertical, PETG |
| Puzzle/finger | in-plane location, shear | primary tension (≈16% of solid) [22] | panel flat |
| Wedge/taper | preload, takes up tolerance | vibration without a stop | wedge flat |

## 7. Test coupons (calibrate on your own printer)

- Peg-and-hole block, gaps 0.1 → 0.5 mm in 0.05 mm steps; same orientation, layer height, material, and cooling as the part; test at room temperature; label press / transition / sliding / loose. Largest gap that still presses = your press value; smallest that slides smoothly = sliding value [5].
- Joint coupons in both orientations (vertical and horizontal), at 0.10/0.15/0.20 mm and 0.10/0.20/0.30 mm [2]; dovetail coupons printed both ways [13].
- For bearings: print a ring with bores stepping 0.05 mm; recheck after 10–30 min for creep [26]; don't reuse a seat you've pressed twice [4].
- Measure printed holes with pin gauges or a drill-bit set, not calipers alone; printed bores can be elliptical, so measure at several angles [32]. A 1.75 mm filament hole gauge exists for filament pins [31].
- Make clearance a `build(**params)` argument and sweep it with `--set`.

## Gaps and conflicts

- No primary measured data found for dovetail clearance vs angle, crush-rib sizing on FDM, bayonets, or cam locks; those numbers are derived or flagged.
- Press-fit interference: 0.1–0.3 mm diametral (most sources, [4]) vs 0.4–0.6 mm "tight" [1]. The latter is untested and likely cracks PLA.
- Conservative 0.5 mm FDM interlock tolerance [6][7] conflicts with 0.15–0.2 mm measured on modern printers [2]. The difference is printer era/calibration; trust your coupon.
- [4] labels a 26 mm OD bearing "608" (a 608 is 22 mm OD).
- [22] figures come from a secondary report; the original *Results in Engineering* paper could not be opened.

## Sources

1. Zbotic, "3D Printing Tolerances: Designing Gaps for Press Fits, Threads, and Snap Fits." https://zbotic.in/3d-printing-tolerances-designing-gaps-for-press-fits-threads-and-snap-fits/
2. Fab Academy 2025, Ísafjörður lab group assignment week 5 (Bambu X1C PLA; Prusa MK4S PLA/PETG; 0.2 mm layers). https://fabacademy.org/2025/labs/isafjordur/group_assignments/group_week05/
3. QIDI, "How to 3D Print Interlocking Parts and Assemblies." https://qidi3d.com/blogs/news/how-to-3d-print-interlocking-parts-and-assemblies
4. Jovanović Pešić Ž. et al., "…press-fit joints in polymer housings," *Tribology in Industry* 47(2), 2025, 389–400 (PETG bearing seats, force-displacement). https://scidar.kg.ac.rs/bitstream/123456789/22638/1/M24-JovanovicPesic-Tribology%20in%20industry.pdf
5. Sovol, "FDM 3D Printing Tolerances & Clearances: How to Design Parts That Fit." https://www.sovol3d.com/blogs/news/fdm-3d-printing-tolerances-clearances-how-to-design-parts-that-fit
6. Hubs, "How to design interlocking joints for 3D printed parts." https://www.hubs.com/knowledge-base/how-design-interlocking-joints-fastening-3d-printed-parts
7. Formlabs, "How to 3D Print Interlocking Parts and Assemblies." https://formlabs.com/blog/how-to-3d-print-interlocking-joints/
8. Prusa Knowledge Base, "Modeling with 3D printing in mind." https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135
9. CNC Kitchen (S. Hermann), "The Influence of Extrusion Temperature on Layer Adhesion." https://www.cnckitchen.com/blog/the-influence-of-extrusion-temperature-on-layer-adhesion
10. Grgić I. et al., "Accuracy of FDM PLA Polymer 3D Printing Technology Based on Tolerance Fields," *Processes* 11(10):2810, 2023. https://www.mdpi.com/2227-9717/11/10/2810
11. Xometry Pro forum, "Will a 6 mm dowel fit in this hole" (Xometry engineer reply). https://xometry.pro/en/topic/will-a-6mm-dowel-fit-in-this-hole/
12. MakerWorld, "Tolerance & Fit Test" (model 2820462). https://makerworld.com/en/models/2820462-tolerance-fit-test
13. MakerWorld, "Dovetail tolerance test" (model 132619). https://makerworld.com/models/132619
14. Siraya Tech, "3D Print Joints Guide." https://siraya.tech/blogs/news/3d-print-joints
15. Bridge City Tools, "Perfect tapered sliding dovetails in wood by hand." https://blog.bridgecitytools.com/2012/09/18/perfect-tapered-sliding-dovetails-in-wood-by-hand/
16. MakerWorld, sliding dovetail lock with tapered wedge (model 2591490). https://makerworld.com/models/2591490
17. Hackaday, "Adding Crush Ribs To 3D Printed Parts For A Better Press Fit" (D. Royer, Marginally Clever), 2020. https://hackaday.com/2020/10/15/adding-crush-ribs-to-3d-printed-parts-for-a-better-press-fit/
18. Printables, "Test Print: Crush Ribs Version04" (43636); page not opened, content from search summary. https://www.printables.com/prints/43636-test-print-crush-ribs-version04
19. Protolabs, "Adding Crush Ribs to Molded Parts." https://www.protolabs.com/resources/design-tips/adding-crush-ribs-to-molded-parts/
20. RapidDirect, "Add Crush Ribs in Injection Molded Parts." https://www.rapiddirect.com/blog/crush-ribs/
21. DigiKey Maker.io, "10 Smart 3D Printing Tips: Tolerances, Holes and Slicer Tricks" (cites Slant 3D grip fins), 2026. https://www.digikey.co.za/en/maker/blogs/2026/10-smart-3d-printing-tips-tolerances-holes-and-slicer-tricks
22. All3DP, "Ditch the glue: researchers find C-shaped joints outperform dovetails in PLA prints" (reporting a *Results in Engineering* study, Univ. of Galway/ATU). https://all3dp.com/4/ditch-the-glue-researchers-find-c-shaped-joints-outperform-dovetails-in-pla-prints/
23. Kuşkun T., 3D-printed dowel L-joints, horizontal vs vertical orientation, *Gazi Univ. J. Sci. Part C*, 2025. https://dergipark.org.tr/en/pub/gujsc/article/1727452
24. NTN Americas technical resources (bearing fits); igus plain-bearing tolerances wiki. https://ntnamericas.com/?p=934 ; https://www.igus.co.uk/plain-bearing/wiki/tolerances
25. Bottini L., Boschetto A., "Interference fit of material extrusion parts," *Additive Manufacturing*, 2019, doi:10.1016/j.addma.2018.11.025. https://iris.uniroma1.it/handle/11573/1201095
26. hex-3d-gon, "Press Fits and Bearing Fits." https://hex-3d-gon.pages.dev/lessons/tolerance-006
27. MIT thesis, "Press fit design: force and torque testing of steel dowel pins in brass and nylon samples." https://dspace.mit.edu/handle/1721.1/36722
28. Fab Academy 2022, A. Yousef, week 6 (printed joint clearance trials). https://fabacademy.org/2022/labs/techworks/students/amin-yousef/week6.html
29. Hackaday, "Glue-in Hinge Design Tries Something Different" (filament-pin hinge; comments on brittleness), 2026. https://hackaday.com/2026/06/12/glue-in-hinge-design-tries-something-different/
30. Hackaday, "How To Design 3D Printed Pins That Won't Break" (Slant 3D), 2025. https://hackaday.com/2025/12/01/how-to-design-3d-printed-pins-that-wont-break/
31. Printables, "1.75 mm filament hole gauge" (240168). https://www.printables.com/model/240168-175mm-filament-hole-guage
32. University of York Technical Support Services wiki, "3DP Tolerances and Fits" (elliptical 26 mm bearing pocket). https://uoy.atlassian.net/wiki/spaces/TSS/pages/286918165/3DP+Tolerances+and+Fits
