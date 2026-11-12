"""Two-piece cabinet wall mount for the AC Infinity Controller 2 (AI-ATC): dovetail
rails locate and carry B; a snap FORK built into A's wall plate retains it. Both
snap arms bend within A's layers.

Concept
  A (wall piece): wall plate (hook-and-loop strips on the cabinet's left wall),
    ceiling flange (one strip on the ceiling), two dovetail rails running front to
    back (copied from controller2_slide_mount), and between the rails a snap fork:
    two arms cut free from the plate by a window, each a 2.25 x 6.5 mm beam running
    front to back, rooted at the back, with a hook on its inner face. The arms flex
    up and down (in-use Y), parallel to the cabinet wall.
  B (front piece): frame the controller screws to (all 4 screws), shelves, side web
    and dovetail grooves (as the baseline, but the web is solid), plus a rigid
    tooth hanging from the web into the fork, and a mouth key: a loose filler
    (~0.3 mm per side) in the fork window's mouth, in front of the arm tips. It
    closes the visible opening and is a backup vertical stop if the dovetails wear;
    the dovetails do the locating. The tooth's back corners are 30 degree
    lead-ins; its front is a 45 degree V that bears on the hooks' 45 degree
    retention faces.

Use / assembly
  0. Before printing anything, measure the controller's screw spacing with
     calipers: 123 mm (template, photo) or 120 (website). At 120 the wall-side
     pilots break into B's side web (an assert stops the build): redesign first.
     Print layout="fit_test":
     - A thin template of B's frame (1.2 mm): hold it on the controller to check
       the hole positions.
     - A "spine" pair cut from the real parts: A's wall-side strip (plate, both
       rails, snap fork) and B's wall-side strip (grooves, tooth, mouth key, foot,
       wall-side screw bosses). Clamp spine A face down to a board (holding it in
       the hand lets the thin plate flex). Slide spine B on: it should slide
       without binding or wobble, then click. To measure pull-off, drive two box
       screws into spine B's bosses, tie a string between the heads, and pull with
       a luggage scale (estimate 7 to 35 N, i.e. 0.7 to 3.5 kg). Then check that
       spine B still slides: the screws must not bulge the boss wall on the wall
       side into A.
     - A pilot ladder (2.2 to 3.0 mm, notch at the 2.2 end): rungs copy the real
       bosses (7 mm boss on the 4 mm frame, 8 mm through-pilot opening at the bed,
       one side trimmed to the real wall-side wall). Drive a box screw into each;
       pick the smallest that doesn't split or bulge the thin side and holds
       hand-tight; set pilot_d.
     Results: binds -> fit=0.16; wobbles > ~0.3 mm -> fit=0.08 (fit also resizes
     the hook and slots, so reprint both spines). No clear click or < ~7 N ->
     hook=1.6; too hard to push on or > ~40 N to pull off -> arm_h=1.8. Whitening
     at the arm roots after ~10 cycles: stop, redesign.
     Optional: layout="cable_test" (two fingers + a fingertip) to try the real
     cables in the 4 mm slot.
  1. Screw the controller to B on the bench.
  2. Stick A to the cabinet wall (two Large strips, along the plate in the bands
     above and below the fork window; keep the arms free) and to the ceiling.
  3. Slide B straight back onto A's rails until it clicks: push on the controller's
     front plate at its wall-side margin, at mid-height (the ~20 mm strip between
     the plate's wall-side edge and the buttons).
  Remove: unplug or slacken the cables, then take the whole assembly off: pull the
  controller sideways away from the wall (that peels the wall strips; B can't
  leave A in that direction), then down (peels the ceiling strip). Don't pull it
  toward you: that pops the snap and racks B in the rails. On the bench, hold A
  and push B off its rails with both hands close to the rails (thumbs on B's
  wall-side frame). The tooth's V spreads the arms and B slides out.
  (In place there's nothing to pull on near the rails' center: the controller's
  top edge sits 0.5 mm under A's ceiling flange, and pulling anywhere far from the
  rails racks B in them.)

  Why: the rails are at the wall, 42 mm apart, and engage only ~36 mm. A push or
  pull far from the rails' center (in X or in Y) twists B in them like a drawer
  pulled by one corner, and friction locks it (jams beyond roughly L / (3 mu) ~
  24 mm off center, mu ~0.5 unverified); the twist also pries A off the wall.
  The wall-side margin at mid-height is ~5 mm from the rail line in X and on
  center in Y.

  Wall strips: two Large strips (19 x 92 mm) running front to back in the bands
  above and below the fork window: y 0 to 29.8 and 49.2 to 82.5 mm from A's bottom
  edge at the default fit. Keep the arms free.
  Cables: a channel runs along A's top inner corner, under the ceiling flange,
  from just behind B to A's back end. Push cables up through the 4 mm slot
  between the finger lips and the flange (where it's open between the fingertips),
  then tuck it toward the wall and under each fingertip; the fingertips hang below
  the lip crest so the cables can't ride back out. The front ~40 mm of the corner is
  taken by B and the controller, so cables can't pass the mount there.
  Ceiling strip: keep it >= 2 mm in from the flange's front and outer edges (B's
  raised top sits 0.1 mm below the flange top and passes beside it). The flange's
  strip face prints as a vertical wall (fine layer lines, not bed-smooth): sand it
  flat before sticking the strip, and paint the seam elsewhere in PrusaSlicer if
  one lands on it. If the cabinet ceiling runs above ~35 C, print in PETG and use
  VHB or Dual Lock instead.

Note: the code builds everything with the wall at -X and mirrors on output, so
the coordinates in comments and asserts below refer to that internal frame.

Load path
  Weight and its twisting moment: dovetail rails (B can't leave the wall or drop).
  Push back (button presses): B's frame seats on the rail fronts.
  Removal/installation force: apply close to the rails (see above).
  Forward pull only: tooth -> hooks -> arms. The hook forces are symmetric in Y,
  so B is not pushed sideways in the dovetails, and no X force reaches the arms.
  The arms are unloaded when seated (>= 0.2 mm Y gap each side after dovetail
  play, 0.3 mm Z gap at the hooks).

Print orientations
  A: wall face (bed side, smooth PEI) down; in-use X vertical, layers are in-use YZ
     planes. The arms' length (Z) and deflection (Y) both lie in the layers: the
     "on edge" orientation of snap_fits.md section 2. The hook outlines print as
     exact 2D perimeters.
  B: front face (against the controller plate) down; in-use Z vertical. The tooth
     is rigid; its 45 degree V grows from the frame and a small foot, no supports.

Key numbers (refs/joinery/snap_fits.md formulas, [derived] here)
  Arm: L = 26 mm (root to hook land), h = 2.25 mm (5 x 0.45 extrusion width),
  b = 6.5 mm, constant section, root fillets 1.0 / 1.2 mm. The above-plate rib runs
  8 mm past the root so the arm's upper half has in-layer anchorage.
  At fit 0.12: dovetail Y play 0.22 mm (incl. X shift), seated tooth gap 0.42 mm
  (0.2 mm after play), hook 1.39 mm, engagement 0.75 mm after play, worst-case
  strain 0.59% along the layers (limit 1.2% repeated in-layer PLA, [derived]).
  At fit 0.20: hook 1.68 mm, strain 0.74%. The outer slot (>= 2.0 mm) is a hard
  stop against over-bending.
  Forces: formula estimates only (E 2.2 to 3.3 GPa, mu 0.3 to 0.6, arm/hook print
  tolerance +/-0.1 mm give roughly 7 to 35 N pull-off). Measure on the fit_test
  coupon before printing the full parts.
  Clearances follow `fit`: the tooth-to-arm gap and arm-tip gap are derived from
  the dovetail play (including the extra Y play when B shifts in X), and the hook
  height is sized for >= 0.75 mm engagement after that play.
  Dovetails: baseline values (fit 0.12, flank 30 deg), interlocking_and_press_fits.md
  section 1; tune with controller2_slide_mount's fit_coupon.

Dimensions: refs/ac_infinity_controller2.md (manufacturer specs, not measured).

In-use frame (mm) of the delivered parts (layout="assembled"):
  X = width, centered on the controller; x=+plate_w/2 is the cabinet wall side,
      which is on the LEFT when you face the controller (right-handed frame,
      facing +Z with +Y up puts +X on the left)
  Y = up; y=0 is the bottom edge of the controller's front plate
  Z = depth, +Z back into the cabinet; z=0 is B's front face (seated)
layout: "print", "assembled" (children [A, B] or [A, B, unit] with show_unit=True),
"fit_test" (frame template, spine pair, pilot ladder), or "cable_test" (two
cable fingers and a fingertip).
"""
import math

from build123d import Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, extrude, loft, mirror


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, d, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)


def _xcyl(y, z, r, x0, x1):
    return Pos((x0 + x1) / 2, y, z) * (Rot(0, 90, 0) * Cylinder(r, x1 - x0))


def _xy_prism(pts, z0, z1):
    return extrude(Plane.XY.offset(z0) * Polygon(*pts, align=None), amount=z1 - z0, dir=(0, 0, 1))


def _xz_prism(pts, y0, y1):
    # Plane.XZ maps local (u, v) to global (X, Z); its normal is -Y.
    return extrude(Plane.XZ.offset(-y0) * Polygon(*pts, align=None), amount=y1 - y0, dir=(0, 1, 0))


def _yz_prism(pts, x0, x1):
    # Plane.YZ maps local (u, v) to global (Y, Z); its normal is +X.
    return extrude(Plane.YZ.offset(x0) * Polygon(*pts, align=None), amount=x1 - x0, dir=(1, 0, 0))


def _round_poly(pts, radii, n=8):
    """Replace polygon corners with circular arcs (radius per vertex; 0 keeps the corner).
    Works for convex and concave corners: the arc is tangent to both adjacent edges."""
    out = []
    m = len(pts)
    for i, (p, r) in enumerate(zip(pts, radii)):
        if r <= 0:
            out.append(p)
            continue
        a, c = pts[i - 1], pts[(i + 1) % m]
        u1 = (a[0] - p[0], a[1] - p[1]); l1 = math.hypot(*u1); u1 = (u1[0] / l1, u1[1] / l1)
        u2 = (c[0] - p[0], c[1] - p[1]); l2 = math.hypot(*u2); u2 = (u2[0] / l2, u2[1] / l2)
        th = math.acos(max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1])))
        t = r / math.tan(th / 2)
        assert t < min(l1, l2) / 2 + 1e-9, "round radius too big for the adjacent edges"
        bx, by = u1[0] + u2[0], u1[1] + u2[1]; bl = math.hypot(bx, by)
        o = (p[0] + bx / bl * r / math.sin(th / 2), p[1] + by / bl * r / math.sin(th / 2))
        t1 = (p[0] + u1[0] * t, p[1] + u1[1] * t)
        t2 = (p[0] + u2[0] * t, p[1] + u2[1] * t)
        a1 = math.atan2(t1[1] - o[1], t1[0] - o[0])
        a2 = math.atan2(t2[1] - o[1], t2[0] - o[0])
        d = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi   # short way round
        out += [(o[0] + r * math.cos(a1 + d * k / n), o[1] + r * math.sin(a1 + d * k / n)) for k in range(n + 1)]
    return out


def _lay_flat(shape, y_offset=0.0):
    bb = shape.bounding_box()
    return Pos(-bb.min.X, -bb.min.Y + y_offset, -bb.min.Z) * shape


def snap_numbers(arm_len, arm_h, arm_b, hook, gap, y_play, slot_w, tip_len, E, mu, lead, ret):
    """Cantilever numbers per refs/joinery/snap_fits.md (constant section)."""
    d_nom = hook - gap
    d_max = d_nom + y_play

    def strain(y, L=arm_len):
        return y * arm_h / (0.67 * L ** 2)

    def wfac(a):
        t = math.tan(math.radians(a))
        return (mu + t) / (1 - mu * t)

    eps = strain(d_nom)
    P = arm_b * arm_h ** 2 * E * eps / (6 * arm_len)
    return dict(defl_nom=d_nom, defl_max=d_max, eps_nom=eps, eps_max=strain(d_max),
                eps_stop=strain(slot_w, tip_len), P=P, push=2 * P * wfac(lead),
                pull=2 * P * wfac(ret), engagement=hook - gap - y_play)


DERIVED: dict = {}   # values derived from None defaults by the last build() (read by tools/build.py)


def build(
    plate_w: float = 135.0,     # controller front plate
    plate_h: float = 79.0,
    plate_t: float = 2.0,       # controller plate thickness (unverified)
    body_w: float = 112.0,      # controller body behind the plate
    body_h: float = 68.0,
    body_d: float = 26.0,       # 28 overall minus plate_t (unverified)
    cut_w: float = 114.0,       # opening for the body (AC Infinity cut hole size)
    cut_h: float = 70.0,
    hole_dx: float = 123.0,     # controller screw spacing (template + product photo)
    hole_dy: float = 67.0,
    pilot_d: float = 2.6,       # M3 / #4 thread-forming; size to the real screws
    fit: float = 0.12,          # dovetail clearance normal to each face (baseline coupon)
    min_wall: float = 1.2,
    # B (front piece)
    frame_t: float = 4.0,
    boss_d: float = 7.0,
    boss_h: float = 4.0,
    shelf_t: float = 3.0,
    shelf_tip: float = 8.0,
    b_depth: float = 40.0,      # B front to back (= rail length)
    web_t: float = 2.4,
    groove_wall: float = 3.2,
    # Dovetail rails (on A)
    rail_h: float = 4.0,
    rail_base: float = 6.0,
    rail_angle: float = 30.0,
    rail_y: float = 18.5,
    dove_round: float = 0.5,    # bullnose on the dovetails' outside edges (A's rail tops, B's groove lips)
    dove_fillet: float = None,  # fillet in the matching inside corners (A's rail roots, B's groove floors);
                                # None: min(0.2, dove_round - fit - 0.1) so the bullnose always clears it
    lead: float = 2.0,          # 45-degree lead-in on rail fronts and groove mouths (blind entry)
    # Snap fork (arms on A) and tooth (on B)
    arm_len: float = 26.0,      # arm root to hook land center
    arm_h: float = 2.25,        # arm thickness in Y (bending direction), 5 extrusion widths
    arm_above: float = 3.5,     # arm height above A's plate face (total b = wall_t + this)
    arm_slot: float = None,     # outer slot = over-deflection stop (None: derived from deflection)
    root_r_in: float = 1.2,     # inner (tension side) root fillet
    tip_gap: float = None,      # arm tips to B's frame back face (None: fit + 0.4)
    hook: float = None,         # hook height (None: sized for engagement_target after play)
    engagement_target: float = 0.75,
    hook_land: float = 0.6,
    lead_angle: float = 30.0,   # hook lead-in, from the insertion axis
    ret_angle: float = 45.0,    # retention face; <= 45 so B's tooth V prints unsupported
    tooth_w: float = 10.0,      # tooth width in Y
    tooth_gap: float = None,    # tooth side to arm inner face, seated (None: play + 0.2)
    tooth_flat: float = 2.0,    # straight side length of the tooth
    notch_play: float = 0.3,    # tooth V to hook retention face along Z, seated
    tooth_wall_clear: float = 0.5,  # tooth bottom to A's back (wall) face
    foot_half: float = 2.0,     # foot under the tooth's V tip (supports it in B's print)
    rib_ext: float = 8.0,       # arm's above-plate part continues this far past the root
    key_gap: float = None,      # mouth key to the window's edges (Y), per side (None: dovetail
                                # play + 0.1, so the key never does the locating; 0.32 at fit 0.12)
    key_chamfer: float = 0.5,   # 45-degree lead-in on the key's back edges and the window's front corners
    E_mpa: float = 2200.0,      # printed PLA modulus (snap_fits.md: 2.2 to 3.3 GPa)
    mu: float = 0.5,            # printed-on-printed friction (unverified)
    # A (wall piece)
    wall_t: float = 3.0,
    depth: float = 100.0,
    ceiling_w: float = 25.0,
    ceiling_t: float = 3.0,
    ceiling_gap: float = 0.5,
    # Aesthetics
    flush_top: bool = True,     # B's top shelf rises to just below A's flange top past its end
    top_seam: float = 0.4,      # gap between A's flange end and B's raised top (>= 0.3 stays open)
    top_drop: float = 0.1,      # B's raised top and façade sit this far below A's flange top. With
                                # the ceiling strip kept >= 2 mm in from the flange's front and outer
                                # edges, neither ever passes under the strip; 0.1 hides A's top edge
    b_corner_r: float = 6.0,    # B's outer corners (matches the controller plate's corner radius)
    a_back_r: float = 3.0,      # A's back corners
    a_front_r: float = 2.0,     # A's front-bottom corner
    edge_chamfer: float = 1.0,  # front top edge (A and B alike) and A's front edges
    shelf_curve: bool = True,   # concave shelf profile instead of a straight taper
    facade: bool = True,        # B's front covers A's front edges along the top and wall-side corners
    facade_t: float = 1.6,      # façade thickness (4 extrusion widths' worth of layers)
    facade_gap: float = 0.3,    # façade to A's recessed front (Z)
    facade_ygap: float = 0.45,  # façade corner pieces to A's recess edges (Y): looser than the
                                # dovetail play so the façade never locates B
    brace: float = 4.0,
    brace_gap: float = 2.0,
    # Cable channel along A's top inner corner (under the ceiling flange), behind B
    cable_w: float = 16.0,      # channel width out from the wall plate (to the finger tips)
    cable_h: float = 12.0,      # channel height below the ceiling flange
    cable_entry: float = 4.0,   # slot between the finger lips and the ceiling flange
    finger_n: int = 3,          # >= 2 (fingertips hang between fingers)
    finger_w: float = 6.0,      # finger width along the channel (front to back)
    finger_root: float = 6.0,   # trunk depth below the channel floor at the wall
    finger_tip: float = 3.0,    # trunk depth at the tip (tapered bracket)
    lip_t: float = 3.0,         # lip thickness at its crest
    finger_round: float = 1.5,  # rounds on the finger's outside corners
    finger_fillet: float = 2.0, # fillets where the finger meets the wall plate
    tip_drop: float = 2.0,      # fingertips hang this far below the lip crest (blocks the slot)
    tip_w: float = 5.0,         # fingertip width along the channel
    a_relief: float = 0.5,
    strip_w: float = 19.0,      # Large hook-and-loop strip width (two on the wall face)
    strip_len: float = 92.0,
    layout: str = "print",
    show_unit: bool = False,
):
    W = plate_w / 2
    H = plate_h
    cy = H / 2
    t = math.tan(math.radians(rail_angle))
    xa = -W + wall_t                 # A wall plate inner face
    xb = xa + fit                    # B's left face
    xt = xa + rail_h                 # rail top
    xg = xt + fit                    # groove floor = web inner face
    xw = xg + web_t                  # web outer face
    xl = -cut_w / 2
    cut_b, cut_t = cy - cut_h / 2, cy + cut_h / 2
    body_b, body_t = cy - body_h / 2, cy + body_h / 2
    hx, hy = hole_dx / 2, hole_dy / 2
    rys = [rail_y, H - rail_y]
    y_ceil0 = H + ceiling_gap
    y_top = y_ceil0 + ceiling_t

    def rail_half(x):
        return rail_base / 2 + (x - xa) * t

    def groove_half(x):
        return rail_half(x) + fit / math.cos(math.radians(rail_angle))

    gh = groove_half(xg)

    # Dovetail play seen by the snap in Y: direct play plus the extra Y play that
    # opens up when B shifts away from the wall in X.
    y_play = fit / math.cos(math.radians(rail_angle)) + fit * t / math.cos(math.radians(rail_angle))
    if tooth_gap is None:
        tooth_gap = y_play + 0.2
    if tip_gap is None:
        tip_gap = fit + 0.4
    if hook is None:
        hook = round(tooth_gap + y_play + engagement_target, 2)
    if dove_fillet is None:
        dove_fillet = max(0.0, round(min(0.2, dove_round - fit - 0.1), 2))
    if key_gap is None:
        key_gap = round(y_play + 0.1, 2)
    if arm_slot is None:
        arm_slot = max(2.0, math.ceil(((hook - tooth_gap + y_play) * 1.3 + 0.3) * 20) / 20)
    DERIVED.clear()
    DERIVED.update(tooth_gap=round(tooth_gap, 3), tip_gap=round(tip_gap, 3), hook=hook,
                   arm_slot=arm_slot, key_gap=key_gap, dove_fillet=dove_fillet)

    # ---- snap geometry (d = distance from the fork center line y = yc) ----
    yc = cy
    tl, tr = math.tan(math.radians(lead_angle)), math.tan(math.radians(ret_angle))
    d_face = tooth_w / 2 + tooth_gap          # arm inner face
    d_out = d_face + arm_h                    # arm outer face
    d_slot = d_out + arm_slot                 # outer slot outer edge
    d_hook = d_face - hook                    # hook tip
    z_ft = frame_t + tip_gap                  # arm tips
    z_lt = z_ft + hook / tl                   # top of the lead-in ramp
    z_le = z_lt + hook_land                   # end of the land
    z_re = z_le + hook / tr                   # retention face meets the arm face
    z_root = (z_lt + z_le) / 2 + arm_len      # arms join the plate here
    z_vtip = z_le + notch_play - d_hook / tr  # tooth V tip (on the fork center line)
    z_vout = z_vtip + (tooth_w / 2) / tr      # V meets the tooth sides
    z_tback = z_vout + tooth_flat + hook / tl  # tooth back face
    x_bot = -W + tooth_wall_clear             # tooth bottom (reaches into A's window)
    x_arm = xa + arm_above                    # arm tops
    arm_b = wall_t + arm_above
    sn = snap_numbers(arm_len, arm_h, arm_b, hook, tooth_gap, y_play, arm_slot,
                      z_root - z_ft, E_mpa, mu, lead_angle, ret_angle)

    # ---- asserts: real geometric and strength constraints ----
    assert layout in ("print", "assembled", "fit_test", "cable_test"), f"unknown layout {layout!r}"
    assert body_w < cut_w and body_h < cut_h, "body must fit the opening"
    assert xw <= xl, "B's side web must sit on the frame's left leg"
    # The wall-side pilots run through B's side web: keep a real wall to its outer face.
    # (Fails loudly if the screw spacing turns out to be 120 mm: that needs a redesign.)
    assert xw - (-hole_dx / 2 + pilot_d / 2) >= min_wall, "too little of B's side web left beside the wall-side pilots"
    # ...and keep a wall between those pilots and B's face against A (a screw can bulge it into A)
    boss_wall_ws = (-hole_dx / 2 - pilot_d / 2) - (-plate_w / 2 + wall_t + fit)
    assert boss_wall_ws >= 1.35, f"only {boss_wall_ws:.2f} mm of boss wall on the wall side (< 3 extrusion widths)"
    assert top_seam >= 0.3, "top seam under 0.3 mm prints closed"
    assert flush_top or not facade, "the façade needs flush_top (A's front is recessed behind it)"
    assert hx + boss_d / 2 <= W and hx - boss_d / 2 > body_w / 2, "right bosses must clear body and edge"
    assert shelf_t < body_b and H - shelf_t > body_t, "shelves hit the body"
    for yr in rys:
        g0, g1 = yr - gh - groove_wall, yr + gh + groove_wall
        for sy in (-1, 1):
            by = cy + sy * hy
            assert by + boss_d / 2 < g0 or by - boss_d / 2 > g1, "left boss overlaps a groove block"
    assert rail_y - gh - groove_wall > shelf_t, "groove block runs into the shelf"
    assert groove_wall - lead >= min_wall, "flared groove mouth leaves too thin a wall"
    assert depth >= b_depth + brace_gap + 5, "wall plate too short for the ceiling brace"
    # Each bullnose sits in the other part's filleted corner; the round must exceed the
    # fillet by more than the fit, or the corners touch before the flanks do.
    assert dove_round >= dove_fillet + fit + 0.1, "dovetail round must clear the mating fillet"
    # Mated flank contact (in X): a round in a (90 - angle) corner eats r / tan(half
    # that angle) along the flank; a fillet in a (90 + angle) corner eats r / tan(half).
    ca = math.cos(math.radians(rail_angle))
    acute = dove_round / math.tan(math.radians((90 - rail_angle) / 2)) * ca
    obtuse = dove_fillet / math.tan(math.radians((90 + rail_angle) / 2)) * ca if dove_fillet > 0 else 0.0
    flank_x = min(xt - acute, xg - obtuse) - max(xa + obtuse, xb + acute)
    assert flank_x >= 2.0, f"dovetail rounds leave only {flank_x:.2f} mm of flank contact"
    lip = cable_h - cable_entry                    # lip crest height above the channel floor
    # The lip rises at 45 degrees (the print limit) and needs room for its crest and a flat floor
    assert cable_w - lip - lip_t >= 2 * finger_fillet + 0.5, "channel too narrow for the 45-degree lip plus a flat floor"
    assert finger_n >= 2, "need at least 2 cable fingers (fingertips hang between them)"
    assert finger_root >= finger_tip, "finger trunk must taper toward the tip (prints without overhang)"
    assert lip - tip_drop >= 4.5, "fingertips leave no room for a 4 mm cable above the channel floor"
    assert cable_w <= ceiling_w, "fingertips must hang from the ceiling flange"
    assert cable_entry >= 3.5, "cable entry slot too narrow for USB cables"
    assert b_depth + brace_gap + 6 + finger_w * finger_n < depth - 2, "no room for the cable fingers behind B"
    assert a_relief > 0, "controller plate would touch A's front edge"
    # Fork sits in B's open channel between the groove blocks, with room to spare
    ch0, ch1 = rys[0] + gh + groove_wall, rys[1] - gh - groove_wall
    assert ch0 + 1 <= yc - d_slot and yc + d_slot <= ch1 - 1, "fork arms hit B's groove blocks"
    # Fork window leaves full-width bands for the two wall strips (no strip on the arms)
    assert yc - d_slot >= strip_w + 1, "no room for the lower wall strip"
    assert y_top - (yc + d_slot) >= strip_w + 1, "no room for the upper wall strip"
    assert depth - a_relief >= strip_len + 2, "wall plate shorter than a Large strip"
    assert key_gap > y_play + 0.05, "mouth key would locate B instead of the dovetails (over-constrained)"
    # Arm tops clear B's web even with B pushed against the wall plate
    assert (xg - fit) - x_arm >= 0.3, "arm tops rub B's web"
    # Tooth clears A's wall face (with B pushed toward the wall) and the arms when seated
    assert x_bot - fit > -W, "tooth would stick out of A's wall face"
    assert min(frame_t, z_ft - 0.3) >= a_relief + 2, "mouth key barely enters the window"
    assert tooth_gap - y_play >= 0.1, "tooth touches an arm when seated (arms must sit unloaded)"
    # Tooth V grows from B's frame/foot (no floating start in B's print)
    foot_top = max(frame_t, z_vtip + 0.01)      # foot rises to meet the V tip if it sits behind the frame
    assert foot_half >= (foot_top - z_vtip) * tr + 0.2, "foot narrower than the tooth where they meet"
    assert foot_half <= d_hook - 0.5, "foot too wide to pass between the hooks"
    assert z_ft - (frame_t + fit) >= 0.3, "arm tips touch B's frame/foot when B is pushed back"
    assert z_tback + 2 <= z_root, "tooth does not fit inside the fork"
    assert z_root + rib_ext + arm_above < depth, "arm rib runs off the plate"
    # Snap sizing (snap_fits.md): in-layer PLA limits 1.2% repeated, 2.0% one-time
    assert arm_len / arm_h >= 10, "arm too stubby for the beam formula"
    assert sn["eps_max"] <= 0.012, f"arm strain {sn['eps_max']:.4f} over the 1.2% repeated limit"
    assert sn["eps_stop"] <= 0.020, f"strain at the slot stop {sn['eps_stop']:.4f} over 2.0%"
    assert arm_slot >= sn["defl_max"] * 1.3 + 0.3, "outer slot too narrow for the deflection"
    assert sn["engagement"] >= 0.5, f"engagement {sn['engagement']:.2f} mm after Y play too small"
    assert tooth_gap - y_play >= 0.15, "seated gap after play too small for print error"
    assert ret_angle <= 45, "tooth V would overhang more than 45 deg in B's print"
    assert mu * tr < 1, "retention face would lock (not releasable by pulling)"
    assert arm_h >= 4 * 0.45, "arm thinner than 4 extrusion widths"

    # Geometry below is built with the cabinet wall at -X and mirrored about the YZ
    # plane on output (see _m), so the delivered parts have the wall at +X, which is
    # the viewer's LEFT when facing the controller (+Y up, +Z into the cabinet).
    def _m(shape):
        return mirror(shape, about=Plane.YZ)

    # ---------------- snap features ----------------
    def fork_cut(z0, x0=-W - 1, x1=xa + 0.01):
        """Window through A's plate: outer slots, inner opening, rounded root corners."""
        c = _box(x0, x1, yc - d_slot, yc + d_slot, z0, z_root)
        rs = arm_slot / 2
        for s in (-1, 1):
            c += _xcyl(yc + s * (d_out + rs), z_root, rs, x0, x1)        # outer slot ends
            c += _xcyl(yc + s * (d_face - root_r_in), z_root, root_r_in, x0, x1)  # inner fillets
        c += _box(x0, x1, yc - d_face + root_r_in, yc + d_face - root_r_in, z_root - 0.01, z_root + root_r_in)
        return c

    def fork_arms():
        arms = None
        rib_end = z_root + rib_ext
        for s in (-1, 1):
            y0, y1 = sorted((yc + s * d_face, yc + s * d_out))
            arm = _xz_prism([(-W, z_ft), (x_arm, z_ft), (x_arm, rib_end), (xa - 0.01, rib_end + arm_above + 0.01),
                             (-W, rib_end + arm_above + 0.01)], y0, y1)
            hk = [(yc + s * (d_face + 0.01), z_ft), (yc + s * d_hook, z_lt), (yc + s * d_hook, z_le),
                  (yc + s * d_face, z_re), (yc + s * (d_face + 0.01), z_re)]
            arm += _yz_prism(hk if s > 0 else hk[::-1], -W, x_arm)
            arms = arm if arms is None else arms + arm
        return arms

    def tooth():
        c = hook / tl
        pts = [(yc, z_vtip), (yc + tooth_w / 2, z_vout), (yc + tooth_w / 2, z_tback - c),
               (yc + tooth_w / 2 - hook, z_tback), (yc - tooth_w / 2 + hook, z_tback),
               (yc - tooth_w / 2, z_tback - c), (yc - tooth_w / 2, z_vout)]
        th = _yz_prism(pts[::-1], x_bot, xg + 0.01)
        th += _box(x_bot, xb + 0.01, yc - foot_half, yc + foot_half, 0, foot_top)
        return th

    def mouth_key():
        # Loose filler in the fork window's mouth, in front of the arm tips; never
        # touches the arms. Back edges chamfered as a lead-in (faces up in B's print).
        k = d_slot - key_gap
        top = min(frame_t, z_ft - 0.3)
        c = key_chamfer
        pts = [(yc - k, 0), (yc + k, 0), (yc + k, top - c), (yc + k - c, top),
               (yc - k + c, top), (yc - k, top - c)]
        return _yz_prism(pts, x_bot, xb + 0.01)

    # ---------------- B: front piece ----------------
    frame = _box(xb, W, 0, H, 0, frame_t)
    frame -= _box(xl, -xl, cut_b, cut_t, -1, frame_t + 1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            frame -= _zcyl(sx * hx, cy + sy * hy, pilot_d, -1, frame_t + 1)

    B = frame
    B += _box(xg, xw, shelf_t - 0.01, H - shelf_t + 0.01, frame_t - 0.01, b_depth)
    for yr in rys:
        B += _box(xb, xg + 0.01, yr - gh - groove_wall, yr + gh + groove_wall, frame_t - 0.01, b_depth)
        x0 = xb - 1
        # Groove cut with B's lip edges bullnosed (concave corners of the cut at x = xb)
        # and the groove floor corners filleted (convex corners of the cut at x = xg).
        e = 3 * dove_round + 1.0
        gpts = [(x0, yr - groove_half(xb) - e), (xb, yr - groove_half(xb) - e), (xb, yr - groove_half(xb)),
                (xg, yr - gh), (xg, yr + gh), (xb, yr + groove_half(xb)), (xb, yr + groove_half(xb) + e),
                (x0, yr + groove_half(xb) + e)]
        B -= _xy_prism(_round_poly(gpts, [0, 0, dove_round, dove_fillet, dove_fillet, dove_round, 0, 0]),
                       frame_t, b_depth + 1)
        sec = lambda z, e: Plane.XY.offset(z) * Polygon(
            (x0, yr - groove_half(x0) - e), (xg, yr - gh - e), (xg, yr + gh + e), (x0, yr + groove_half(x0) + e),
            align=None)
        B -= loft([sec(b_depth - lead, 0), sec(b_depth + 0.01, lead)])
    if shelf_curve:
        # Concave sweep from the far end up to the wall side (quadratic Bezier): reads
        # as a bracket rather than a brace. In B's print it's the shelf's top edge.
        p0, p2 = (W, frame_t + shelf_tip), (xw, b_depth)
        p1 = (xw + 25, frame_t + shelf_tip + 6)
        sweep = [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                  (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1])
                 for t in [i / 16 for i in range(17)]]
        shelf = [(xb, frame_t), (W, frame_t)] + sweep + [(xb, b_depth)]
    else:
        shelf = [(xb, frame_t), (W, frame_t), (W, frame_t + shelf_tip), (xw, b_depth), (xb, b_depth)]
    B += _xz_prism(shelf, 0, shelf_t)
    B += _xz_prism(shelf, H - shelf_t, H)
    x_flush = xa + ceiling_w + top_seam                # B's raised top starts past A's flange
    if flush_top:
        yr_ = y_top - top_drop
        raised = _xz_prism(shelf, H - 0.01, yr_) + _box(xb, W, H - 0.01, yr_, 0, frame_t)
        B += raised & _box(x_flush, W + 1, H - 1, yr_ + 1, -1, b_depth + 1)
    yB_top = y_top - top_drop if flush_top else H
    # B's outer corners (far from the wall): radius matching the controller plate's
    for yc_, sy_ in ((b_corner_r, -1), (yB_top - b_corner_r, 1)):
        cut = _box(W - b_corner_r, W + 1, yc_, yc_ + sy_ * (b_corner_r + 1), -1, b_depth + 1) \
            if sy_ > 0 else _box(W - b_corner_r, W + 1, yc_ - b_corner_r - 1, yc_, -1, b_depth + 1)
        cut -= _zcyl(W - b_corner_r, yc_, 2 * b_corner_r, -2, b_depth + 2)
        B -= cut
    # Façade: B's front face continues over A's front edges along the top (in front of
    # A's ceiling flange and wall plate) and down into the wall-side corners, where
    # the controller plate's rounded corners would otherwise show A's edge.
    if facade:
        fz = facade_t
        B += _box(-W, x_flush + 0.01, H - 0.01, yB_top, 0, fz)                  # top strip
        B += _box(-W, xb + 0.01, H - b_corner_r, H + 0.01, 0, fz)               # top wall-side corner
        B += _box(-W, xb + 0.01, 0, b_corner_r, 0, fz)                          # bottom wall-side corner
    # Front top edge chamfer, across the full width when the façade covers A
    if flush_top:
        c = edge_chamfer
        x0c = -W - 1 if facade else x_flush - 1
        B -= _yz_prism([(yB_top - c, -0.01), (yB_top + 0.01, -0.01), (yB_top + 0.01, c)], x0c, W + 1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * hx, cy + sy * hy
            boss = _zcyl(x, y, boss_d, frame_t - 0.01, frame_t + boss_h)
            B += boss & _box(xb, W, 0, H, 0, frame_t + boss_h + 1)
            B -= _zcyl(x, y, pilot_d, -1, frame_t + boss_h + 1)
    B += tooth()
    B += mouth_key()

    # ---------------- A: wall piece ----------------
    A = _box(-W, xa, 0, y_top, a_relief, depth)
    A += _box(xa - 0.01, xa + ceiling_w, y_ceil0, y_top, a_relief, depth)
    A += _xy_prism([(xa - 0.01, y_ceil0 - brace), (xa - 0.01, y_ceil0), (xa + brace, y_ceil0)],
                   b_depth + brace_gap, depth)
    for yr in rys:
        # Rail with its top edges bullnosed and its roots filleted into the plate.
        e = 3 * dove_fillet + 1.0
        rpts = [(xa - 1, yr - rail_half(xa) - e), (xa, yr - rail_half(xa) - e), (xa, yr - rail_half(xa)),
                (xt, yr - rail_half(xt)), (xt, yr + rail_half(xt)), (xa, yr + rail_half(xa)),
                (xa, yr + rail_half(xa) + e), (xa - 1, yr + rail_half(xa) + e)]
        A += _xy_prism(_round_poly(rpts, [0, 0, dove_fillet, dove_round, dove_round, dove_fillet, 0, 0]),
                       frame_t + fit, b_depth)
        rz0 = frame_t + fit
        A -= _xz_prism([(xt - lead, rz0 - 0.01), (xt + 0.01, rz0 - 0.01), (xt + 0.01, rz0 + lead)],
                       yr - rail_half(xt) - 1, yr + rail_half(xt) + 1)
    # Cable fingers: bracket-shaped arms out from the wall plate under the ceiling
    # flange, behind B. A tapered trunk (deep at the wall, filleted into the plate)
    # carries a flat channel floor; a rounded lip curls up at 45 degrees to leave a
    # `cable_entry` slot below the flange. In A's print (wall face down) the profile
    # only narrows or widens at <= 45 degrees going up, so no supports.
    y_floor = y_ceil0 - cable_h                       # channel floor
    x_tip = xa + cable_w
    x_rise = x_tip - lip_t - lip                      # where the lip starts rising
    e = finger_fillet * 3 + 1
    fpts = [(xa - 1, y_floor - finger_root - e), (xa, y_floor - finger_root - e),
            (xa, y_floor - finger_root),               # trunk underside meets the plate (fillet)
            (x_tip, y_floor - finger_tip),             # tip, underside corner (round)
            (x_tip, y_floor + lip),                    # tip, crest outer corner (round)
            (x_tip - lip_t, y_floor + lip),            # crest inner corner (round)
            (x_rise, y_floor),                         # foot of the lip (fillet)
            (xa, y_floor),                             # channel floor meets the plate (fillet)
            (xa, y_floor + e), (xa - 1, y_floor + e)]
    r_, f_ = finger_round, finger_fillet
    finger = _round_poly(fpts, [0, 0, f_, r_, r_, r_, r_, f_, 0, 0])
    z0f, z1f = b_depth + brace_gap + 6, depth - 2 - finger_w
    zfs = [z0f + (z1f - z0f) * (i / max(finger_n - 1, 1)) for i in range(finger_n)]
    for zf in zfs:
        A += _xy_prism(finger, zf, zf + finger_w)
    # Fingertips: fins hanging from the ceiling flange between the fingers, reaching
    # `tip_drop` below the lip crest near the slot, so a cable resting in the channel
    # can't ride up and out over the lips. Their underside rises at 45 degrees toward
    # the wall (room to tuck a cable in under them) and they grow out of the flange
    # at 45 degrees in A's print.
    x_t = xa + cable_w - 1                            # fingertip outer face, just inside the lips
    y_target = y_floor + lip - tip_drop               # wanted low point (after rounding)

    def tip_profile(y_v):
        x_meet = x_t - (y_ceil0 - y_v)                # 45-degree underside meets the flange
        pts = [(x_meet - 2, y_top - 0.5), (x_t, y_top - 0.5), (x_t, y_v), (x_meet, y_ceil0),
               (x_meet - 2, y_ceil0)]
        return _round_poly(pts, [0, 0, 1.2, 1.5, 0])

    # The round on the tip raises its low point; drop the sharp vertex to compensate.
    lift = min(p[1] for p in tip_profile(y_target)) - y_target
    tip_prof = tip_profile(y_target - lift)
    assert abs(min(p[1] for p in tip_prof) - y_target) < 0.02, "fingertip low point off target"
    for za, zb in zip(zfs, zfs[1:]):
        zm = (za + finger_w + zb) / 2
        A += _xy_prism(tip_prof, zm - tip_w / 2, zm + tip_w / 2)
    A -= fork_cut(a_relief - 1)
    for s_ in (-1, 1):   # 45-degree lead-in at the window's front corners
        y0 = yc + s_ * d_slot
        tri = [(y0, a_relief - 0.01), (y0 + s_ * key_chamfer, a_relief - 0.01), (y0, a_relief + key_chamfer)]
        A -= _yz_prism(tri, -W - 0.01, xa + 0.01)     # _yz_prism extrudes along +X either winding
    A += fork_arms()
    # A's corners and front edges
    xa0, xa1 = -W - 1, xa + ceiling_w + 1
    for (yc_, zc_, r_, ys, zs) in ((a_back_r, depth - a_back_r, a_back_r, -1, 1),
                                   (y_top - a_back_r, depth - a_back_r, a_back_r, 1, 1),
                                   (a_front_r, a_relief + a_front_r, a_front_r, -1, -1)):
        y0_, y1_ = sorted((yc_, yc_ + ys * (r_ + 1)))
        z0_, z1_ = sorted((zc_, zc_ + zs * (r_ + 1)))
        A -= _box(xa0, xa1, y0_, y1_, z0_, z1_) - _xcyl(yc_, zc_, r_, xa0 - 1, xa1 + 1)
    c = edge_chamfer
    zf = a_relief
    if not facade:   # with the façade these edges are inside the recess below
        # front top edge (plate + flange), along X
        A -= _yz_prism([(y_top - c, zf - 0.01), (y_top + 0.01, zf - 0.01), (y_top + 0.01, zf + c)], xa0, xa1)
        # flange's front-underside edge, along X
        A -= _yz_prism([(y_ceil0 - 0.01, zf - 0.01), (y_ceil0 + c, zf - 0.01), (y_ceil0 - 0.01, zf + c)],
                       xa + 0.5, xa1)
    # plate's front inner edge, along Y (below the flange)
    A -= _xz_prism([(xa - c, zf - 0.01), (xa + 0.01, zf - 0.01), (xa + 0.01, zf + c)], -1, y_ceil0)
    if facade:
        # Step A's front back where B's façade covers it
        zr = facade_t + facade_gap
        A -= _box(-W - 1, x_flush - top_seam + 1, H - facade_ygap, y_top + 1, -1, zr)
        A -= _box(-W - 1, xa + 0.01, H - b_corner_r - facade_ygap, H, -1, zr)
        A -= _box(-W - 1, xa + 0.01, -1, b_corner_r + facade_ygap, -1, zr)
        # small chamfer on the recessed front's top edge so no sliver shows above the façade
        cr = 0.5
        A -= _yz_prism([(y_top - cr, zr - 0.01), (y_top + 0.01, zr - 0.01), (y_top + 0.01, zr + cr)],
                       -W - 1, x_flush - top_seam + 1)
    # Relief in A's plate opposite B's wall-side bosses, so a screw that bulges the
    # thin boss wall can't make B rub on A
    for sy in (-1, 1):
        yb = cy + sy * hy
        A -= _box(xa - 0.3, xa + 0.01, yb - boss_d / 2 - 1, yb + boss_d / 2 + 1,
                  frame_t - 0.5, frame_t + boss_h + 1)

    if layout == "fit_test":
        # B's flat frame (screw spacing and pilots) + a "spine" pair cut from the real
        # parts: A's wall-side strip (plate, rails, snap fork; no ceiling flange,
        # brace or cable fingers) and B's wall-side strip (grooves, tooth, mouth key,
        # wall-side bosses). Tests the dovetail fit, the click and the pull-off.
        z_end = max(b_depth, z_root + rib_ext + arm_above) + 1     # keep the arms' full ribs
        spine_a = A & _box(-W - 1, xa + max(rail_h, arm_above) + 1, -1, H, -1, z_end)
        spine_b = B & _box(-W - 1, xw + 0.5, -1, H, -1, b_depth + 1)   # full tooth, key, foot
        assert len(spine_a.solids()) == 1 and len(spine_b.solids()) == 1, "a spine fell apart"
        # Pilot ladder: 8 mm deep vertical holes, 2.2 to 3.0 mm (left to right; the
        # notch marks the 2.2 end). Drive a box screw into each; pick the smallest
        # that takes the screw without splitting and holds hand-tight; set pilot_d.
        ladder_d = [2.2, 2.4, 2.6, 2.8, 3.0]
        # Each rung copies a real boss: a boss_d boss on the frame_t frame, pilot through
        # both from the bed; the -X side is trimmed to the real wall-side boss wall.
        half = boss_d / 2 + 2                                         # rung half-size (Y, +X)
        step = half + (max(ladder_d) / 2 + boss_wall_ws) + 3           # rungs don't touch
        lad = None
        for i, d_ in enumerate(ladder_d):
            cx_ = i * step
            wall_cut = d_ / 2 + boss_wall_ws                          # hole center to the trimmed face
            rung = _box(cx_ - wall_cut, cx_ + half, -half, half, 0, frame_t)
            rung += _zcyl(cx_, 0, boss_d, frame_t - 0.01, frame_t + boss_h)
            rung &= _box(cx_ - wall_cut, cx_ + 2 * half, -2 * half, 2 * half, -1, frame_t + boss_h + 1)
            rung -= _zcyl(cx_, 0, d_, -1, frame_t + boss_h + 1)
            lad = rung if lad is None else lad + rung
        x_end = (len(ladder_d) - 1) * step + half
        lad += _box(-(ladder_d[0] / 2 + boss_wall_ws), x_end, half - 1, half + 2, 0, 2)   # back bar
        lad -= _box(-(ladder_d[0] / 2 + boss_wall_ws) - 1, 2, half + 0.5, half + 2.1, -1, 3)  # notch: 2.2 end
        assert len(lad.solids()) == 1, "pilot ladder fell apart"
        # Hole-position template: B's frame outline, 1.2 mm thick
        tmpl = _box(xb, W, 0, H, 0, 1.2) - _box(xl, -xl, cut_b, cut_t, -1, 2)
        for sx in (-1, 1):
            for sy in (-1, 1):
                tmpl -= _zcyl(sx * hx, cy + sy * hy, pilot_d, -1, 2)
        f = _lay_flat(_m(tmpl))
        a_ = _lay_flat(Rot(0, 90, 0) * _m(spine_a))                     # wall face (+X) down
        b_ = _lay_flat(_m(spine_b))                                     # front face down
        y1 = f.bounding_box().max.Y + 10
        a_ = Pos(0, y1, 0) * a_
        b_ = Pos(a_.bounding_box().max.X + 10, y1, 0) * b_
        l_ = Pos(b_.bounding_box().max.X + 10, y1, 0) * _lay_flat(lad)
        return Compound(children=[f, a_, b_, l_])

    if layout == "cable_test":
        # A short section of A with two cable fingers and the fingertip between them,
        # to try the real cables in the slot. Prints wall face down like A.
        zf0, zf1 = zfs[0] - 2, zfs[1] + finger_w + 2
        cab = A & _box(-W - 1, xa + cable_w + 1, y_floor - finger_root - 6, y_top + 1, zf0, zf1)
        assert len(cab.solids()) == 1, "cable coupon fell apart"
        return Compound(children=[_lay_flat(Rot(0, 90, 0) * _m(cab))])

    A, B = _m(A), _m(B)                  # wall to +X: the viewer's left
    if layout == "assembled":
        parts = [A, B]
        if show_unit:
            unit = _box(-body_w / 2, body_w / 2, body_b, body_t, 0, body_d)
            unit += _box(-W, W, 0, H, -plate_t, 0)
            parts.append(unit)
        return Compound(children=parts)

    a = _lay_flat(Rot(0, 90, 0) * A)     # in-use -X becomes print +Z (wall face, at +X, down)
    b = _lay_flat(B, y_offset=y_top + 10)
    return Compound(children=[a, b])
