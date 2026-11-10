# Fastener joints in FDM printed parts

Scope: screws, heat-set inserts, nuts and bolts in PLA/PETG printed on a 0.4 mm nozzle (Prusa MK3S+, PrusaSlicer 2.7). All values in mm unless noted. "CAD" means the value to model. "Axis-vertical hole" means the hole axis is along Z (the hole opening faces up or down on the bed); "axis-horizontal hole" means the axis lies in XY. Printed holes come out undersized: 0.1 mm on a Prusa MK2.5 [4], about 0.25 mm on a Prusa CORE One L [2]. Values tagged *derived* are computed from a cited rule, not measured.

## Quick reference

| Item | Size | CAD value | Source |
|---|---|---|---|
| Heat-set insert hole, nominal (CNC Kitchen/Ruthex) | M2 / M2.5 / M3 / M3 short / M4 / M5 | 3.2 / 4.0 / 4.0 / 4.0 / 5.7 / 6.5 | [1] |
| Heat-set insert hole, as printed, axis-vertical | M3 (L 5.7) | 4.2 (nominal +0.2; smaller inserts +0.2 to +0.3) | [2] |
| Insert length (standard / short) | M2 / M2.5 / M3 / M4 / M5 | 3.0 / 4.0 / 5.7 (3.0) / 8.1 (4.0) / 9.5 (5.8) | [1] |
| Insert min wall around hole | M2 / M2.5–M3 / M4 / M5 | 1.3 / 1.6 / 2.1 / 2.6 (others say 3.0 or ≥ d, see below) | [1] |
| Insert blind-hole depth | all | insert length + 1 | [3] |
| Machine screw tapped directly, axis-vertical | M2 / M2.5 / M3 / M4 | 2.10 / 2.50 / 2.70–2.90 / 3.75 | [4][6][15] |
| Machine screw tapped directly, axis-horizontal | M2 / M2.5 / M3 / M4 | 1.84 / 2.30 / 2.72 / 3.55 (PLA) | [6] |
| Plastic-type self-tapper (Bambu BT), axis-vertical, PLA | BT2 / BT2.5 / BT3 | 2.00 / 2.35 / 3.00 | [6] |
| #4 / #6 sheet-metal or wood screw pilot | #4 (2.84 OD) / #6 (3.51 OD) | 2.0–2.3 / 2.5–2.8 (*derived*, 0.7–0.8 × OD; unverified in print) | [7][8] |
| Clearance hole close / normal / loose (ISO 273) | M2 | 2.2 / 2.4 / 2.6 | [10] |
| | M2.5 | 2.7 / 2.9 / 3.1 | [10] |
| | M3 | 3.2 / 3.4 / 3.6 | [10] |
| | M4 | 4.3 / 4.5 / 4.8 | [10] |
| | M5 | 5.3 / 5.5 / 5.8 | [10] |
| | #4 / #6 (in) | 0.116 / 0.1285 / 0.144 ; 0.144 / 0.1495 / 0.1695 | [10] |
| Hex nut across flats (AF) / thickness | M2 / M2.5 / M3 / M4 / M5 | 4.0/1.6, 5.0/2.0, 5.5/2.4, 7.0/3.2, 8.0/4.0 (ISO 4032: 4.7) | [11][25][26] |
| | #4-40 / #6-32 | 6.35 (1/4")/2.38 (3/32"), 7.94 (5/16")/2.78 (7/64") | [14] |
| Hex nut pocket AF (CAD) | all | nut AF + 0.2 to 0.4 (snug to slide-in); Prusa M3: 5.456 (press) | [9][15] |
| Square nut pocket (Prusa M3, DIN 562 nut) | M3 | 5.6 × 2.15 | [15] |
| SHCS head dk max / k (ISO 4762) for counterbores | M2 / M2.5 / M3 / M4 / M5 | 3.98/2.0, 4.68/2.5, 5.68/3.0, 7.22/4.0, 8.72/5.0 | [12] |
| Countersunk dk theoretical (ISO 10642, 90°) | M2 / M2.5 / M3 / M4 / M5 | 4.70 / 5.88 / 6.72 / 8.96 / 11.20 | [13] |

## 1. Choosing a method (measured strength, M3)

| Method | Pull-out PLA | Pull-out PETG | Torque-out | Reuse |
|---|---|---|---|---|
| Screw tapped directly into undersized hole | 142 kg [4] | 118 kg [5] | ~1 N·m, plastic strips [4][5] | few cycles |
| Heat-set insert (Ruthex) | 181 kg [4]; ~1400 N [2] | 119 kg [5] | 3–4 N·m, screw head shears first in PLA [4]; 3 N·m, insert spins out in PETG [5] | many |
| Cheap molding-type insert | 39 kg [4] | n/a | 3–4 N·m [4] | many |
| Helicoil | n/a | 120 kg, 1 N·m: no gain over direct [5] | 1 N·m | many |
| Hex nut, pocket on far side (bottom) | n/a | 166 kg [5] | ~2 N·m (PETG crushes) [5] | unlimited |
| Hex nut, side-loaded slot | n/a | 86 kg (nut shears through) [5] | ~2 N·m [5] | unlimited |

Conditions: [4] Prusament PLA, 100% infill, 0.15 mm layers; [5] PETG, 4 perimeters, 100% infill. Use these to rank methods, not as allowables; 15–40% infill parts are weaker.

Rules of thumb: assemble-once joints: tap directly. Opened repeatedly or torqued above ~1 N·m: heat-set insert. Highest pull-out with cheap hardware: captive nut on the far side so the load pushes the nut into the part. A 1 N·m torque on an M3 already produces >1500 N preload (µ = 0.14) [5], so stripping is the usual failure when tapping plastic directly.

## 2. Screws threaded directly into plastic

**When:** covers, enclosures, brackets assembled once or a few times; light loads.

**Design rules**
- Pilot hole (plastic-specific screws, molded plastics): 0.7 × d for higher strip torque [8]; 0.8 × d is a common general value [7]. Molded-plastic tables for 30° Plas-Fix screws give M3: 2.2–2.6, M4: 3.1–3.5, M5: 3.4–4.1, larger with deeper engagement [7].
- FDM measured values (machine screws, metric coarse): CNC Kitchen used 2.7 for M3 [4]; Prusa's own M3 "self-cutting" hole reported as 2.791 (forum, unverified) [15]; Bambu/MakerWorld gives the table in Quick reference [6]. Axis-horizontal holes are smaller in their table because the layers there are the thing that splits; Bambu advises going one size larger than its axis-horizontal table to avoid interlayer cracking when a hole is in a side wall [6]. Sources disagree by ~0.2 mm; for an MK3S+ start at 2.8 for M3 axis-vertical and print a 0.1 mm-step test coupon.
- PETG: Bambu's PETG HF axis-horizontal holes are 0.1–0.2 smaller than PLA (M3: 2.60 vs 2.72) [6]; PETG is more ductile but weaker than PLA [5].
- Engagement length: 2–2.5 × d for load-bearing joints [6][8], minimum 2 × d [7]; Bambu minimums 4 (M2), 5 (M2.5–M4) [6].
- Boss OD: 2.5–3 × pilot diameter [7] (about 2–2.5 × d). For M3: 7–8 OD. In FDM, give the hole 3+ perimeters (`--set perimeters=4`), so the threads form in solid wall, not infill.
- Low infill trick: cut thin radial slots (0.2 wide, hole-depth long, 1.5–2 extrusion widths from the hole wall) so the slicer wraps perimeters that tie the hole wall into the part [6].
- Lead-in: 45° chamfer or counterbore at the hole mouth to the major diameter; prevents cracking at the top layers [6][7].
- Tightening torque (Bambu recommendation, PLA/PETG): M2 0.13, M2.5 0.20, M3 0.25, M4 0.40 N·m; BT2/2.5/3: 0.15/0.20/0.30 N·m [6]. Direct-tapped M3 strips at ~1 N·m [4][5].
- Plastic-specific thread-forming screws (30° flank, e.g. Plastite-type, Bambu BT) cause less radial stress than machine or sheet-metal screws and tolerate reassembly [6][8][9].
- #4 and #6 sheet-metal/wood screws: no measured FDM data found. Use 0.7–0.8 × OD (*derived*: #4 2.0–2.3, #6 2.5–2.8) plus your printer's undersize, and test.

**Failure modes:** stripping (overtorque, oversized pilot), boss splitting along layers (undersized pilot, axis-horizontal hole, thin wall), and loss of clamp over time. PLA creep relaxes preload under sustained load; I found no measured preload-relaxation data for printed PLA/PETG (gap). Prefer PETG for warm or sustained-load joints and re-torque after a day.

```python
# M3 tapped boss, axis vertical, on top of a plate at z=t
B = (Align.CENTER, Align.CENTER, Align.MIN)
part += Pos(x, y, t) * Cylinder(7.5 / 2, 8, align=B)            # boss OD 2.5 x d
part -= Pos(x, y, t + 8 - 6.5) * Cylinder(2.8 / 2, 6.5, align=B)  # pilot, 6.5 deep (> 2 x d)
part -= Pos(x, y, t + 8 - 0.5) * Cone(2.8 / 2, 3.8 / 2, 0.5, align=B)  # lead-in chamfer
```

## 3. Heat-set threaded inserts

**When:** repeated assembly, torque >1 N·m, or metal threads needed in a thin part.

**Dimensions (CNC Kitchen standard series; Ruthex matches for M3: OD 4.6, hole 4.0, W 1.6)** [1]

| Size | L | Insert OD | Pilot (tip) OD | Hole (nominal) | Min wall W |
|---|---|---|---|---|---|
| M2 | 3.0 | 3.6 | 3.1 | 3.2 | 1.3 |
| M2.5 | 4.0 | 4.6 | 3.9 | 4.0 | 1.6 |
| M3 | 5.7 | 4.6 | 3.9 | 4.0 | 1.6 |
| M3 short | 3.0 | 4.6 | 3.9 | 4.0 | 1.6 |
| M3 "Voron" | 4.0 | 5.0 | 4.25 | 4.4 | 1.3 |
| M4 (short) | 8.1 (4.0) | 6.3 | 5.5 | 5.7 | 2.1 |
| M5 (short) | 9.5 (5.8) | 7.1 | 6.3 | 6.5 | 2.6 |

- Hole size: nominal values are for drilled/ideal holes. As-printed M3 holes needed 4.2 in CAD: at 4.0 a severe plastic burr is pushed below the insert, 4.1 still too tight, 4.2 gave ~90% of max pull-out; pull-out drops sharply above that (drilled holes: drop between 4.1 and 4.2) [2]. For smaller inserts add 0.2–0.3 to CAD [2]. Pull-out falls as the hole grows [2], so don't oversize to make installation easy; size for "pre-seats with slight resistance" [2].
- Third-party conflict: some secondary charts list M4 5.6 and M5 6.4 [not verified]; use the manufacturer value of your insert brand.
- Depth: blind hole = L + 1 so displaced plastic has somewhere to go; a through hole is fine but should not be shorter than the insert [3]. JLC3DP specifies 7.0 deep for a 5.8 M3 insert [24].
- Straight (untapered) holes; no chamfer needed [3]. A 0.3–0.5 entry chamfer is still common to locate the tip (opinion).
- Wall: CNC Kitchen minimum W above [1]; JLC3DP requires 3.0 [24]; Hubs suggests wall ≥ thread d [9]. Use ≥ W from [1] as an absolute floor and 2–3 (≥ d) for load-bearing parts, with 3–4 perimeters so the knurl melts into solid wall.
- Installation: iron 10–20 °C above print temperature (PLA ~225 °C, PETG ~245 °C), melt ~90% of the depth with the tip, finish flush with a flat tool, hold a few seconds because inserts tend to creep back out [3]. CNC Kitchen used 240 °C on PLA [2] and 210 °C in an earlier PLA test [4]; temperature is not critical within that range.
- Load direction: put the insert in the face opposite the clamped part when possible, so the screw pulls the insert into the plastic rather than out of it (reader suggestion [22], same mechanism as the bottom-pocket nut result [5]).
- Axis-horizontal inserts: the hole top sags; use a flat-top or teardrop with the flat at the nominal radius (Section 6) and verify with a test coupon.

**Failure modes:** insert spins (soft or ductile plastic, shallow knurl; seen in ASA and PETG) [4][5]; insert pulls out with a cone of plastic; tilted insert from an uneven push; plastic burr blocking the thread below the insert (hole too small, no depth margin).

```python
# M3x5.7 insert from top face at z=top, as-printed CAD 4.2
d, L = 4.2, 5.7
part -= Pos(x, y, top - (L + 1)) * Cylinder(d / 2, L + 1, align=(Align.CENTER, Align.CENTER, Align.MIN))
```

## 4. Captive nuts and nut traps

**Pocket sizing** (AF = across flats; across corners = AF / cos 30° = 1.155 × AF)

| Size | Nut AF | Nut m | Pocket AF (CAD) | Pocket depth |
|---|---|---|---|---|
| M2 | 4.0 | 1.6 | 4.2–4.4 | 1.8–2.0 |
| M2.5 | 5.0 | 2.0 | 5.2–5.4 | 2.2–2.4 |
| M3 | 5.5 | 2.4 | 5.7–5.9 | 2.6–2.8 |
| M4 | 7.0 | 3.2 | 7.2–7.4 | 3.4–3.6 |
| M5 | 8.0 | 4.0 (DIN 934) / 4.7 (ISO 4032) | 8.2–8.4 | m + 0.2–0.4 |
| #4-40 | 6.35 | 2.38 | 6.55–6.75 | 2.6–2.8 |
| #6-32 | 7.94 | 2.78 | 8.15–8.35 | 3.0–3.2 |

Nut data [11][14][25][26]; pocket = nut + clearance, *derived* from Hubs' 0.2 total (0.1 per side) starting point [9] and the repo rule of +0.3. Prusa's own M3 pockets are reportedly 5.456 AF × 2.4 deep, i.e. a press fit (forum, unverified) [15]. Hex flats print close to nominal because they are straight segments [16], so hex pockets need less allowance than round holes. Check whether your M5 nuts are DIN 934 or ISO 4032 before sizing depth.

**Orientation**
- Axis-vertical pocket opening on the bed (bottom pocket): no overhang for the pocket itself, but the screw hole above it starts on a ceiling. Either (a) model a one-layer sacrificial diaphragm (≥ one full layer height, e.g. 0.2–0.3 at 0.2 layers) and drill/punch it out [18][20]; or (b) the "hanging hole"/sequential-overhang trick: layer 1 above the pocket is two bridges leaving a slot as wide as the screw hole, layer 2 bridges at 90° closing it to a square, then the round hole (or octagon) continues; each layer is one layer-height thick [18][19]. Option (b) needs no post-processing but is weaker than a solid membrane; add ~2 layers of extra material above the nut [18]. PrusaSlicer 2.7 has no automatic counterbore-bridging option (OrcaSlicer does: "partially bridged" or "sacrificial layer") [23], so model it in CAD and make every step land on a layer boundary.
- Axis-horizontal pocket (hex in a side wall): orient the hex with a flat on top. The ceiling is then a bridge of length AF/√3 (M3: 3.3), well under the ~10 bridging limit. A vertex-up hex has 30° roof faces, which sag.
- Side-loaded slot (nut slides in from the side, screw axis vertical): slot width = pocket AF, slot ceiling is a ≤10 mm bridge. It was the weakest method tested (86 kg PETG, nut shears out through the slot) [5]; put the slot on the side away from the load and keep ≥2 mm of material beyond the nut in the load direction.
- Pause-and-embed: pause at the first layer that would cover the pocket; the nut top must sit below that layer [18]. In PrusaSlicer insert a pause (M601) at that height. PETG oozes during pauses; expect a weak first layer after resume [web forum, not measured].

**Retaining:** press-fit hex (AF +0 to +0.1), a drop of CA, a pull-in with a long screw, or square nuts (DIN 562 thin square nuts are the same width as hex AF and do not rotate in a slot) [15].

```python
# M3 bottom nut pocket (opening on bed) + one-layer sacrificial diaphragm + clearance hole
af, depth, lh = 5.8, 2.6, 0.2
part -= Pos(x, y, 0) * extrude(RegularPolygon(af / 2, 6, major_radius=False), depth)  # AF along Y
part -= Pos(x, y, depth + lh) * Cylinder(3.4 / 2, h - depth - lh, align=(Align.CENTER, Align.CENTER, Align.MIN))
# the solid layer between z=depth and depth+lh is drilled out after printing
```

## 5. Through-bolts, counterbores, countersinks

- Clearance: ISO 273 close (H12) / normal (H13) / loose (H14) values in Quick reference [10]. Because prints undersize 0.1–0.25 [2][4], model axis-vertical holes at "normal" to get a close fit, and "loose" for a free fit or long holes. Prusa's own M3 through hole is reportedly 3.286 (unverified) [15].
- Counterbore for socket head (ISO 4762): diameter dk max + 0.3–0.5 (M3: 5.68 → 6.0–6.2; M4: 7.22 → 7.6; M5: 8.72 → 9.1), depth k + 0.2 for flush (M3: 3.2) [12]; increments *derived*.
- Countersink (ISO 10642): 90° cone, top diameter dk theoretical + 0.2–0.4 (M3: 6.72 → 7.0; M4 8.96 → 9.3) [13]; the cone depth is (D − hole)/2.
- Printing: on the top face (opening up), counterbores and countersinks print without support. On the bed face, a 90° countersink is exactly 45° and prints fine; a counterbore leaves a flat annular ceiling that needs the sacrificial layer or two-step bridge trick from Section 4. If both faces need heads, flip the design so the head is on top.
- Plastic under the head creeps; use washers or flanged/button heads to cut bearing stress (general practice; no FDM data found).

```python
# M3 SHCS counterbore from the top face at z=top, through hole from the bed
B = (Align.CENTER, Align.CENTER, Align.MIN)
part -= Pos(x, y, 0) * Cylinder(3.4 / 2, top, align=B)
part -= Pos(x, y, top - 3.2) * Cylinder(6.1 / 2, 3.2, align=B)
# countersink on the top face instead: 90 deg cone, 3.4 -> 7.0
part -= Pos(x, y, top - 1.8) * Cone(3.4 / 2, 7.0 / 2, 1.8, align=B)
```

## 6. Horizontal holes and printed-hole accuracy

- Causes of undersize: polygon faceting, ooze on short segments, and corner-cutting on arcs (dominant) [16]; for axis-horizontal holes, the layer staircase intrudes into the circle and the top bridge sags ~0.15 [17].
- Polyhole (axis-vertical): model the hole as a regular polygon with n ≈ 2 × d (mm) sides, minimum 3, with circumradius r / cos(π/n) so the flats touch the true circle; drills from 1 mm up fit [16]. PrusaSlicer 2.7 has no polyhole conversion; model it, or use `--set xy_size_compensation` (shrinks/grows the whole part, not just holes).
- Teardrop (axis-horizontal): circle plus a 45° roof meeting at a point 1.414 × r above center. Flat-top: truncate the roof at r (or r + half a layer) so the top is a short bridge. Required above ~8 diameter (repo rule); smaller holes print without it but sag and come out undersized vertically, so use it on any hole that must fit a pin or insert. "Horihole": hull the teardrop shifted ±½ layer height to compensate the staircase; must be sliced at the design layer height [17].
- Screw holes in side walls: go one size larger than axis-vertical values [6] and use flat-top.

```python
# Flat-top teardrop hole along world Y, centered at (x, 0, zc); point/flat toward +Z
r = 2.6
td = Circle(r) + Rot(0, 0, 45) * Rectangle(r, r, align=(Align.MIN, Align.MIN))  # teardrop, apex at y=1.414r
td = td & Rectangle(2 * r, 2 * (r + 0.3))                                          # flat top at r + 0.3
part -= Pos(x, 0, zc) * extrude(Plane.XZ * td, amount=L / 2, both=True)           # Plane.XZ local Y = world Z
# polyhole for an axis-vertical d=3.4 hole
import math; n = max(round(2 * 3.4), 3)
poly = RegularPolygon(3.4 / 2 / math.cos(math.pi / n), n)
```

## 7. Modeled (printed) threads

- FDM printed threads below M5 are not recommended [9]; modeled threads are worthwhile mainly for M8+ and coarse custom profiles (lids, knobs).
- Printed PLA screws printed upright (axis vertical) failed at as low as 1.24 N·m, all along layer planes; one printed lying down reached ~16 N·m (145 in-lb), about 2× the best upright one (rough, uncalibrated test) [21]. Orient printed bolts axis-horizontal and printed nuts/holes axis-vertical.
- Add 0.2–0.4 diametral clearance to modeled internal threads and chase them a few times before assembly [9] (clearance value is general practice, not measured). Threads usually aren't the failure point; the surrounding wall cracks or delaminates [27] (secondhand summary; not verified against the original test).
- Thread geometry generators exist outside core build123d (e.g. the separate `bd_warehouse` package); not verified here. For metric threads prefer an insert or nut.

## Gaps and conflicts

- No measured FDM data for #4/#6 sheet-metal or wood screws; values are derived from molded-plastic rules.
- No measured preload relaxation/creep data for printed PLA or PETG bolted joints.
- Direct-tap M3 hole: 2.7 [4], 2.79 [15], 2.9 [6]; insert wall: 1.6 [1] vs 3.0 [24] vs ≥ d [9].
- Bambu hole tables [6] are tuned for Bambu printers and slicers; MK3S+ undersize may differ.

## Sources

1. CNC Kitchen threaded insert dimension table (via 3DJake): https://www.3djake.uk/cnc-kitchen/threaded-insert-set-xl ; Ruthex M3 (via 3DJake): https://www.3djake.com/ruthex/threaded-insert-m3-100-pieces
2. CNC Kitchen, "Are Our Heat-Set Insert Datasheets Wrong?": https://www.cnckitchen.com/blog/are-our-heat-set-insert-datasheets-wrong
3. CNC Kitchen, tips and tricks for threaded inserts: https://www.cnckitchen.com/blog/tipps-amp-tricks-fr-gewindeeinstze-im-3d-druck-3awey
4. CNC Kitchen, "Threaded Inserts for 3D Prints: Cheap vs Expensive": https://www.cnckitchen.com/blog/threaded-inserts-for-3d-prints-cheap-vs-expensive
5. CNC Kitchen, "Helicoils vs Threaded Inserts vs Embedded Nuts": https://www.cnckitchen.com/blog/helicoils-threaded-insets-and-embedded-nuts-in-3d-prints-strength-amp-strength-assessment
6. MakerWorld (Bambu Lab forum), "How to Design Screw Holes for 3D Printing?": https://forum.bambulab.com/t/how-to-design-screw-holes-for-3d-printing/217352
7. TR Fastenings, Plas-Fix 45 installation guide: https://www.trfastenings.com/Knowledge-Base/Fasteners-for-Plastic/Plas-Fix-45-installation
8. JC Fasteners, Plastite / thread-forming screw technical guide: https://www.jcfasteners.com/wp-content/uploads/2020/01/Plastite-Screw-Guide.pdf
9. Hubs, "How to assemble 3D printed parts with threaded fasteners": https://www.hubs.com/knowledge-base/how-assemble-3d-printed-parts-threaded-fasteners/
10. Albany County Fasteners, clearance hole chart (ISO 273 and inch): https://www.albanycountyfasteners.com/media/6b/b8/g0/1764944339/clearance-hole-chart.pdf ; medium series confirmed by TR Fastenings: https://www.trfastenings.com/Knowledge-Base/Engineering-Data/tapping-sizes-and-clearance-holes
11. Westfield Fasteners, DIN 934 hex nut dimensions: https://www.westfieldfasteners.co.uk/Standards/Nut_Hex_M.html
12. Westfield Fasteners, ISO 4762 / DIN 912 socket head cap screw: https://westfieldfasteners.co.uk/Standards/ScrewBolt-SHCap-M.html
13. Westfield Fasteners, ISO 10642 countersunk socket screw: https://westfieldfasteners.co.uk/Standards/ScrewBolt-SHCsk-M.html
14. Aspen Fasteners, #4-40 hex machine screw nut: https://www.aspenfasteners.com/4-40-hex-machine-screw-nuts-steel-plain/ ; Spaenaur catalog (#6-32): https://static.datasheets.com/doc/4500201-spaenaur-hn-2002-ds.pdf
15. Prusa forum, "precise dimensions of screw holes and nut pockets" (user post, attributed to Prusa parts): https://forum.prusa3d.com/forum/english-forum-general-discussion-announcements-and-releases/designers-and-engineers-here-are-the-precise-dimensions-of-screw-holes-and-nut-pockets
16. nophead (HydraRaptor), "Polyholes": https://hydraraptor.blogspot.com/2011/02/polyholes.html
17. nophead (HydraRaptor), "Horiholes": https://hydraraptor.blogspot.com/2020/07/horiholes_36.html
18. nophead (HydraRaptor), "Buried nuts and hanging holes": https://hydraraptor.blogspot.com/2014/03/buried-nuts-and-hanging-holes.html
19. Hackaday, "3D Printing Bores Without Support" (Maker's Muse sequential overhangs): https://hackaday.com/2023/05/28/3d-printing-bores-without-support
20. Hackaday, "Sacrificial Bridge Avoids 3D Printed Supports": https://hackaday.com/2017/10/17/sacrificial-bridge-avoids-3d-printed-supports
21. Hackaday, "Torque Testing 3D Printed Screws": https://hackaday.com/2024/12/03/torque-testing-3d-printed-screws
22. Hackaday, "Thomas Sanladerer Gets New Threads" (article and reader comments): https://hackaday.com/2024/01/06/thomas-sanladerer-gets-new-threads
23. OrcaSlicer wiki, bridging settings (counterbore hole bridging): https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_bridging
24. JLC3DP, threaded insert service design requirements: https://jlc3dp.com/help/article/threaded-insert-service
25. OMDL ISO 4032 fastener data table (M2–M4): https://royasutton.github.io/omdl-snapshot/docs/html/omdl-v1.0/group__database__component__fastener__iso__4032.html
26. Proto-Pic metric hex nut table (M5 ISO 4032 thickness 4.7): https://proto-pic.co.uk/product/machine-hex-nut-m3-25-pack
27. Hackaday, "Threaded 3D Printed Part Comparison" (2019, CNC Kitchen test summary): https://hackaday.com/2019/03/26/threaded-3d-printed-part-comparison
