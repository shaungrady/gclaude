# Joinery reference for FDM parts (Prusa MK3S+, 0.4 mm nozzle)

Researched November 2026. Every number in these docs carries a source tag; values
marked [derived] or [unverified] are calculations or single unconfirmed sources.
Treat clearances as starting points and calibrate with a coupon on this printer.

| Doc | Use it for |
| --- | --- |
| [fdm_fundamentals.md](fdm_fundamentals.md) | Read first. Fit clearances, hole accuracy, layer stepping, anisotropy (strength and strain across layers), overhang/bridge limits, minimum walls and gaps, creep and heat, perimeters around holes, joint checklist |
| [fasteners.md](fasteners.md) | Screws into plastic (pilot sizes), heat-set inserts, nut traps, through-bolts, counterbores/countersinks, horizontal holes, printed threads |
| [snap_fits.md](snap_fits.md) | Cantilever snap equations and allowable strain (in-layer vs across-layer), hook angles, orientation, snap retention vs joint play, annular/torsion snaps, bayonets, detents, failure modes |
| [interlocking_and_press_fits.md](interlocking_and_press_fits.md) | Dovetails (play vs flank angle, layer stepping), T-slots, rails, pins/dowels, press fits, crush ribs, bearing seats, keyed/puzzle joints, wedges/cams, which joint carries which load, fit coupons |
| [adhesives_and_splitting.md](adhesives_and_splitting.md) | CA/epoxy/MMA/solvent by material, thermal welding, glue joint geometry, splitting oversized parts, PrusaSlicer cut-tool connectors, embedding hardware/magnets, adhesive mounting (Command, Dual Lock, VHB, hook-and-loop) |

## Known weak spots and conflicts across the docs

- **Sliding/snug fit clearance for separately printed parts:** no primary measurements found. Sources range 0.15 to 0.5 mm per side; print a coupon.
- **Snap-fit strain limits for printed plastic:** none published. The snap_fits.md table is derived from printed-specimen data (PLA ~1.0% across layers, ~1.2 to 2.0% in-layer). Fictiv's 4 to 8% figures are near break strain; don't use them.
- **Across-layer strength ratio:** PLA 0.33 to 0.73, PETG 0.38 to 0.60 of in-layer, depending on source. Strain to failure across layers (~2%) is consistent.
- **M3 pilot hole for direct threading:** 2.7 to 2.9 mm depending on source (2.7 has CNC Kitchen pull-out data behind it).
- **Wall around heat-set inserts:** 1.6 to 3.0 mm depending on source.
- **Press-fit interference:** 0.1 to 0.3 mm is supported; a 0.4 to 0.6 mm figure has no test behind it and risks cracking PLA.
- **Creep:** printed PLA at ~30% of its strength broke within hours at 25 C (one study). Keep sustained loads low; let snaps sit unloaded once assembled.
- **Adhesive mounting on printed surfaces:** no manufacturer ceiling guidance for Command strips; no adhesive-strength data with stated bond area on printed PLA/PETG.
