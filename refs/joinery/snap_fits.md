# Snap-fits and flexure joints for FDM parts (MK3S+, 0.4 mm nozzle, PLA/PETG)

Scope: cantilever, annular and torsion snaps, bayonet/detent latches. Screws, press fits, sliding joints, adhesives and general tolerances are covered in sibling files.

## Quick reference

**Formulas** (rectangular section, other part rigid; ε as a fraction, so 2% = 0.02) [1]:

| Quantity | Formula |
|---|---|
| Permissible undercut, constant thickness h | y = 0.67 ε L² / h |
| Same, thickness tapered linearly to h/2 at hook | y = 1.09 ε L² / h (over 60% more deflection than constant) |
| Root strain for a chosen undercut | ε = y h / (0.67 L²) (constant) or y h / (1.09 L²) (tapered) |
| Deflection force at hook (any taper; h, b at root) | P = b h² E_s ε / (6 L) |
| Mating force (lead angle α) | W = P (μ + tan α) / (1 − μ tan α) |
| Separation force (retention angle α′) | same formula with α′; no release when μ tan α′ ≥ 1 |
| Repeated assembly | use about 60% of the one-time strain [1]; DuPont uses 25 to 50% [2] |
| Both parts equally flexible | each takes half the deflection [1] |

**Allowable strain for printed material.** These are my values, not published snap-fit limits. I derived them by applying Bayer's rule (amorphous resin: about 70% of yield strain; no yield point: about half the elongation at break) [1] to measured data for printed specimens [5–10]. Nobody publishes snap-fit strain limits for printed parts, so treat these as a starting point and test a coupon.

| Material | Printed yield strain, in-plane | Break strain across layers (Z) | One-time, in-plane | Repeated, in-plane | Across layers (avoid) |
|---|---|---|---|---|---|
| PLA | 2.9–3.4% [5,7] | 1.9–2.0% [5,7] | **2.0%** | **1.2%** | 1.0% / 0.6% |
| PETG | 5.1–6.0% [6,9] | 1.4–2.5% [6,9] | **3.5%** | **2.0%** | 0.7–1.2% / 0.5% |
| ABS | 4.1% [8] | 2.0% (no yield) [8] | **2.8%** | **1.7%** | 1.0% / 0.6% |
| TPU 95A | no yield, >560% at break [10] | 82% [10] | 10–20% (unverified) | | |

Sources disagree. Fictiv lists "acceptable strain" of 4–8% for printed PLA and 7% for ABS [4]. Those values are near the elongation at break and are not safe design limits. Fictiv also says to cut allowable strain by 50% for arms built along Z [4], which agrees with the ratio in the table. The TPU value comes from DuPont's Hytrel figures (20% once, 10% repeated) [2], used as a proxy for TPU.

**Printed modulus** (use for E_s; the secant modulus at 1–2% strain is somewhat lower, so the forces below are about ±30%): PLA 2.2–3.3 GPa [5,7], PETG 1.5–1.9 GPa [6,9], ABS 1.7–2.0 GPa [8].

**Friction μ:** no published PLA or PETG values were found. Bayer lists 0.35–0.40 for PBT and 0.45–0.55 for PC on steel, about 1.2× higher for same-material pairs [1]. Use μ = 0.5 for printed-on-printed (unverified).

**Starting dimensions for a PLA cantilever:**
- Print it on edge (see Orientation).
- Root thickness h = 1.8 mm (4 extrusion widths), or 1.35 mm for small parts.
- Taper to h/2, but keep at least 0.9 mm at the tip.
- L ≥ 8h; L/h ≥ 10 for the beam formula to be accurate [3].
- Width b ≥ 5 mm [14].
- Root fillet R = 0.5h to 0.6h [1,14], never sharp. A sharp corner gives a stress concentration factor of 2 [2].
- Lead-in angle 30° [1,2].
- Retention angle 45° for releasable, 90° for permanent [2,4].
- Undercut 0.8–1.2 mm, checked with the formula.

## 1. Cantilever snap-fits

**When to use:** lids, battery doors, PCB retention, joining housing halves. This is the default snap for FDM, because the flexing part can be laid out so that it bends within the layers.

**Design rules**
- Strain is highest at the root. Tapering the thickness from h to h/2 makes the outer-fiber strain uniform along the arm. For the same undercut, it lowers root strain by 0.67/1.09 = 39% [1]. Bayer also allows tapering the width to b/4 instead (y = 0.86 ε L²/h) [1].
- Deflection grows with L² but only with 1/h. If strain is too high, lengthen the arm first. A U- or L-shaped arm adds length inside a small envelope [1,3].
- The classical formula underestimates root strain for short, stubby beams. It is good when L/h > 10 [3]. BASF applies a magnification factor to correct for this and for flexible walls; Fictiv calls it Q, and Q = 1 for a rigid wall [3,4]. I couldn't get the BASF Q values. For L/h < 6, add about 25% margin on strain (my estimate, not from a source).
- Root fillet: Bayer finds the stress-concentration benefit levels off at R/h = 0.6, with a minimum of 0.38 mm (0.015 in) [1]. Hubs recommends R ≥ 0.5h [14]. FDM has no sink marks, so use 0.5–0.6h freely.
- Snaps should be free of stress once assembled [1]. If the arm must stay partly deflected to hold the part tight, see Failure modes.

**Hook geometry**
- **Lead-in angle α:** 30° is the default [1,2]. At μ = 0.5, W/P = 1.51 at 30° and 3.0 at 45°. A smaller angle needs less force but a longer hook.
- **Retention angle α′:** Equal to α gives the same force to assemble and to pull apart [4]. A 45° face gives a releasable joint [2]. A 90° face is permanent and can only be released by deflecting the arm through a window or slot [2,4]. The joint locks under axial pull once μ tan α′ ≥ 1, which is α′ ≥ 63° at μ = 0.5 (from [1]). Above that, pulling breaks the hook or arm instead of releasing it. Even 90° hooks can unhook under high load, because the arm rotates, so put a stop behind the arm if the pull-out load is high.
- **Engagement depth** = undercut y, which is the deflection. Add a land of 0.5 mm or more at the top of the hook so the tip isn't knife-edged.
- **Hook length:** about y/tan α + y/tan α′ + land. For y = 1, α = 30° and α′ = 90°, that is 1.73 + 0 + 0.6 = 2.3 mm.

**Minimal build123d (algebra mode).** The profile is in XY and extruded by the width, so the part prints on edge. The arm runs along +X and the hook sticks out in +Y.

```python
from math import tan, radians
from build123d import *

def cantilever_snap(L=15.0, h=1.8, b=6.0, y=1.0, lead=30.0, ret=90.0,
                    land=0.6, r_root=0.9, wall=3.0):
    lead_len = y / tan(radians(lead))
    ret_len = 0.0 if ret >= 90 else y / tan(radians(ret))
    x_tip = L + ret_len + land + lead_len
    prof = Polygon((0, 0), (x_tip, 0), (x_tip, h),
                   (x_tip - lead_len, h + y),   # lead-in face
                   (L + ret_len, h + y),        # land
                   (L, h),                      # retention face
                   (0, h), align=None)
    part = extrude(Plane.XY * prof, amount=b)
    part += Pos(-wall / 2, h / 2, b / 2) * Box(wall, h + 8.0, b)   # base wall
    root = (part.edges().filter_by(Axis.Z)
            .filter_by_position(Axis.X, -0.01, 0.01)
            .filter_by_position(Axis.Y, -0.01, h + 0.01))
    return fillet(root, radius=r_root)       # both root corners
```
I ran this on build123d 0.13 and it returns a valid solid. To taper the arm, replace `(0, h)` and `(L, h)` with a sloped top edge, for example `(L, h/2)` with the hook rebased on that point.

## 2. Print orientation of snap arms

Prusament PLA tensile yield is 59.3 MPa printed on edge, 50.8 MPa printed flat, and 37.6 MPa printed upright. Elongation at yield in the same orientations is 3.2%, 2.9% and 1.9%. Charpy impact is 13.7, 12.7 and 5.0 kJ/m² [5]. Ultimaker PLA printed upright breaks at 2.0% with no yield, against 7.8% printed flat [7]. PETG upright: 30 MPa and 2.5%, against 47–50 MPa and 5.1% in-plane [6].

Orientations from best to worst:
1. **On edge (best).** Arm length and deflection are both in the XY plane, and the width b runs along Z. The tension and compression faces are continuous perimeters running along the arm, and the fillet and hook profile print as accurate 2D outlines. The ramps are vertical walls, so there are no overhangs.
2. **Flat.** The arm lies on the bed and deflects in Z. Stress runs along the layers, but the outer fibers are top and bottom solid infill, usually laid at ±45°, which is weaker than perimeters [5]. A hook that points up has staircased ramps, and one that points down needs support.
3. **Upright (avoid).** The arm runs along Z. Bending puts tension straight across the layer interfaces, and the stair-step surface adds notches that concentrate stress [11]. This is the classic snap that breaks off at a layer line on first assembly.

Klahn et al. make the key point for FDM: the direction an arm deflects does not have to match the direction the parts are joined. Lay the beam perpendicular to the joining direction so it bends within the layers, and make the arm or the mating part the piece that rotates [11]. In practice, if a box lid snaps down along Z, put the arms on the lid's side walls so they deflect in X or Y, with the hooks pointing sideways. Don't put vertical arms on the box.

**If an arm must bend across the layers:**
- Design to ≤1.0% strain for one-time assembly and ≤0.5–0.6% for repeated assembly in PLA (from the table).
- Lengthen the arm. In the worked example below, the same 1 mm undercut needs L ≈ 16.4 mm at 1.0% strain in a constant-thickness arm.
- Taper the arm and use a generous fillet.
- Use PETG, which has the higher Z yield strain in Prusa's data [6].
- Or split the flexure off into a separate part printed on edge.

Layer-adhesion settings belong to the anisotropy file.

## 3. Worked example: PLA cantilever (checked against [1])

Arm printed on edge with L = 15 mm, h = 1.8 mm, b = 6 mm, undercut y = 1.0 mm, α = 30°, μ = 0.5, E_s = 2.0 GPa (assumed).

- **Constant-thickness arm.**
  - Strain: ε = 1.0 × 1.8 / (0.67 × 15²) = **1.19%**. That is under the 2.0% one-time limit and right at the 1.2% repeated limit.
  - Deflection force: P = 6 × 1.8² × 2000 × 0.0119 / (6 × 15) = **5.2 N**.
  - Mating force: W = 5.2 × 1.51 = **7.8 N**.
  - With a 45° retention face, separation = 5.2 × 3.0 = **15.5 N**. With a 90° face it does not release.
- **Tapered 1.8 → 0.9 mm.**
  - ε = 1.0 × 1.8 / (1.09 × 225) = **0.73%**, P = 3.2 N, W = 4.8 N, separation at 45° = 9.5 N.
  - This gives margin for repeated use and for lateral float.
- **The same constant arm printed upright:** 1.19% is above the 1.0% across-layer limit, so it is likely to crack.
- **Maximum undercut** at 2.0% (one-time, constant): y = 0.67 × 0.02 × 225 / 1.8 = 1.68 mm.

## 4. Snap retention vs clearance and play

- **Lateral float reduces engagement.** If the mating part can shift by c away from the hook (sliding-fit clearance, undersized holes), the bite drops from y to y − c. Keep y − (total lateral play) ≥ 0.5 mm. This is my rule of thumb and is unverified.
- **Lateral float toward the hook raises strain.** The arm then deflects by y + c during assembly. Check ε at y + c. In the example, with c = 0.2 mm the constant arm reaches 1.43%, over the repeated limit, while the tapered arm reaches 0.88%.
- **Locate with locators, retain with snaps.** Guide the parts with ribs, pins or lips, and use the snap only to resist separation. Klahn's FDM lid used locators around its rim for exactly this [11]. A snap that also has to locate the part gets loaded sideways and relaxes.
- **Axial rattle.** A 90° hook leaves whatever axial gap was designed in. You can take it out with a sloped retention face and a small residual deflection (DuPont's "partially loaded" lugs [2]), but in PLA that preload relaxes (see Failure modes). Either accept a gap of about 0.1–0.2 mm, use PETG, or preload with a separate compliant rib instead of the snap arm.
- **Cumulative tolerance.** On printed parts, the undercut and the arm-to-window clearance carry about ±0.1–0.2 mm of error. Annular snaps with undercuts under 0.5 mm are therefore unreliable.

## 5. Annular snap-fits

**When to use:** round caps, lamp covers and similar parts where a 360° seal or uniform retention matters [1].

**Design rules [1]:**
- Permissible undercut y = ε d when one part is rigid. When both parts are equally flexible, the undercut can be twice that.
- Transverse force P = y d E_s X, where X is a geometric factor from Bayer's charts.
- Mating force W = P (μ + tan α)/(1 − μ tan α).
- A groove more than 1.8√(d t) from the end of the tube behaves as "remote", and the force rises up to about 3×.
- DuPont: 30° lead-in, a 45° return angle suits most uses, and 90° is permanent [2]. Its table gives undercut e = 0.25–0.35 mm at d = 10 mm, about 3% of d, for a steel shaft in an acetal hub [2].

**Printing:**
- Print with the axis vertical. Hoop strain then runs along the perimeters, which is the strong direction.
- A 45° return face and a 30°-from-vertical lead-in print without support.
- PLA at 1.2–2% on d = 20 mm allows only 0.24–0.4 mm of undercut, which is about the size of the print error. For PLA, slot the hub into fingers so it behaves as cantilevers [1], or use PETG.

```python
def shaft_with_bead(d=20.0, y=0.3, z_bead=8.0, lead=30.0, ret=45.0, length=12.0):
    r, a, c = d / 2, y / tan(radians(lead)), y / tan(radians(ret))
    half = Polygon((0, 0), (r, 0), (r, z_bead - c), (r + y, z_bead),
                   (r + y, z_bead + 0.4), (r, z_bead + 0.4 + a),
                   (r, length), (0, length), align=None)
    return revolve(Plane.XZ * half, axis=Axis.Z)   # prints upright
```

## 6. Torsion snaps

**When to use:** a latch that holds against pull but releases when a lever is pressed, such as a rocker on a lid [1,11].

**Design rules [1]:**
- Permissible twist φ_pm = 180 γ_pm l / (π r) in degrees, for a circular bar of length l and radius r.
- Permissible shear strain γ_pm ≈ (1 + ν) ε_pm ≈ 1.35 ε_pm.
- Torque: P₁ l₁ = γ G I_p / r, × 2 for two bars, with G = E_s / (2(1 + ν)) and I_p = π r⁴ / 2.
- Example: PLA at ε = 2%, l = 8 mm, r = 1.5 mm gives φ = 8.3°.

**Printing:** a horizontal torsion bar shears its layer interfaces. Use the across-layer strain (1% gives 4.1°) and a long bar. My geometric reasoning, unverified: rectangular bars print more cleanly than round ones, but the round-bar formula then doesn't apply exactly.

## 7. Bayonet, quarter-turn and detent latches

I found no engineering source with numbers for printed bayonets. The guidance here is derived from the cantilever equations.

- **Layout:**
  - Use 2–3 pins on the cylinder that run in L-slots.
  - The axial lock comes from a detent at the end of the slot: a bump that rides on a cantilever, or a cantilever tab that drops into a notch.
  - Design the detent as a hook with α = α′ (30–45°) so it releases in both directions by torque.
  - Hold torque ≈ W × detent radius, using W from the snap formula.
  - Size the cantilever with the strain limits above.
- **Axial preload** (no rattle) should come from a dedicated compliant tab, not the pins. In PLA, expect it to relax.
- **Printing:**
  - Print with the axis vertical.
  - Chamfer the underside of the pins at 45° (it would otherwise be an overhang).
  - Keep slot ceilings to short bridges.
  - Put the detent cantilever in the XY plane so it deflects radially within the layers.
  - Slot clearance: see the tolerance file.

**Living hinges:** these only matter here as joint pivots. PLA is poor for repeated flexing. PETG survives limited cycles, and polypropylene is the right material but is outside the PLA/PETG scope. No measured hinge data for printed PLA or PETG was found.

## 8. Failure modes

- **Stress relaxation and creep (PLA).** Printed PLA loses 11–14% of its stress within 500 s at a fixed strain at room temperature [12]. Relaxation is higher in bending than in tension, and ±45° rasters relax least [13]. Any snap left deflected, and any snap preloaded against rattle, loses clamp force within hours to days. Design snaps to sit unloaded once assembled [1], and use PETG where preload must persist.
- **Heat.** PLA has HDT 55 °C and Tg 55–60 °C [5]. PETG has HDT 68 °C [6]. Ultimaker rates PLA to about 59 °C [7]. In a car, near motors, or in sun, PLA snaps take a set and lose retention. Use PETG or ABS there.
- **Fatigue.** The repeated-use factors are 60% (Bayer) [1] and 25–50% (DuPont, acetal and nylon) [2]. I found no fatigue data for printed snap arms, so test them when they cycle more than about 10 times.
- **Brittle fracture at layer lines.** This is the dominant failure for arms built upright. PLA Charpy impact upright is 5.0 kJ/m² against 13.7 on edge [5].
- **Root cracking.** Causes are a sharp root (stress factor 2 [2]), an arm that is too short (DuPont shows short acetal lugs breaking [2]), or over-deflection. Add a hard stop behind the arm so users can't bend it past y.
- **Hook shear-off.** A 90° hook loaded in pull shears across its base. In flat or upright prints the hook is a few layers tall, so print on edge.

## Sources

1. Bayer MaterialScience (now Covestro), "Snap-Fit Joints for Plastics: A Design Guide" (Table 1 equations, Table 2 strains, Table 3 friction, examples I/II, torsion and annular sections). https://cdn.sparkfun.com/assets/home_page_posts/1/4/1/0/Plastic_Snap_fit_design.pdf
2. DuPont, "General Design Principles for DuPont Engineering Polymers", Module I, pp. 83–86 (snap-fits, Table 9.03, Table 9.04). https://academic.sun.ac.za/mad/catalogs/dfmguidelines/dupontgeneraldesignprinciples.pdf
3. C. Lee (BASF), "Snapfit design, Part 3: improved cantilever design", UL Prospector. https://ulprospector.ul.com/1248/snapfit-3/
4. Fictiv, "How to Design Snap Fit Components" (printed-material strain table, 50% reduction for Z). https://www.fictiv.com/articles/how-to-design-snap-fit-components
5. Prusa Polymers, Prusament PLA Technical Data Sheet v1.0 (printed specimens, MK3). https://cdn.shopify.com/s/files/1/1745/6181/files/PRUSA_PLA_TechSheet_ENG.pdf
6. Prusa Polymers, Prusament PETG Technical Data Sheet. https://cdn.shopify.com/s/files/1/1745/6181/files/PETG_TechSheet_ENG.pdf
7. Ultimaker PLA TDS v5.00 (XY / YZ / Z printed specimens). https://www.alloys.com.au/Documents/Ultimaker-PLA-TDS-v5.00.pdf
8. Ultimaker ABS TDS v5.00. https://www.alloys.com.au/Documents/Ultimaker-ABS-TDS-v5.00.pdf
9. Ultimaker CPE (copolyester, PETG-family) TDS v5.00. https://www.alloys.com.au/Documents/Ultimaker-CPE-TDS-v5.00.pdf
10. Ultimaker TPU 95A TDS v5.00. https://www.alloys.com.au/Documents/Ultimaker-TPU95A-TDS-v5.00.pdf
11. C. Klahn, D. Singer, M. Meboldt, "Design Guidelines for Additive Manufactured Snap-Fit Joints", Procedia CIRP 50 (2016) 264–269. https://publikationen.bibliothek.kit.edu/1000142464
12. A. Bertocco et al., "Stress Relaxation Behavior of Additively Manufactured Polylactic Acid (PLA)", Materials 15 (2022) 3509. https://www.iris.unina.it/retrieve/e268a733-d186-4c8f-e053-1705fe0a812c/materials-15-03509-v2.pdf
13. "Stress relaxation of 3D printed PLA of various infill orientations under tensile and bending loadings", J. Appl. Polym. Sci. (2023), doi:10.1002/app.54463. https://onlinelibrary.wiley.com/doi/full/10.1002/app.54463
14. Hubs (Protolabs Network), "How to design snap-fit joints for 3D printing". https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/
