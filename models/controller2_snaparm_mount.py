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
    tooth hanging from the web into the fork. The tooth's back corners are 30 degree
    lead-ins; its front is a 45 degree V that bears on the hooks' 45 degree
    retention faces.

Use / assembly
  0. Print layout="fit_test": B's flat frame (hold it on the controller to check
     screw spacing and pilots) plus a short fork coupon and tooth coupon to feel
     the click and the pull-off force before printing the full parts.
  1. Screw the controller to B on the bench.
  2. Stick A to the cabinet wall (two Large strips, along the plate in the bands
     above and below the fork window; keep the arms free) and to the ceiling.
  3. Slide B straight back onto A's rails until it clicks (~7 N push).
  Remove: pull the controller straight forward (~14 N, see below). The tooth's V
  spreads the arms and B slides out; leave ~40 mm of cable slack.

Load path
  Weight and its twisting moment: dovetail rails (B can't leave the wall or drop).
  Push back (button presses): B's frame seats on the rail fronts.
  Forward pull only: tooth -> hooks -> arms. The hook forces are symmetric in Y,
  so B is not pushed sideways in the dovetails, and no X force reaches the arms.
  The arms are unloaded when seated (0.3 mm Y gap each side, 0.3 mm Z gap).

Print orientations
  A: wall face (bed side, smooth PEI) down; in-use X vertical, layers are in-use YZ
     planes. The arms' length (Z) and deflection (Y) both lie in the layers: the
     "on edge" orientation of snap_fits.md section 2. The hook outlines print as
     exact 2D perimeters.
  B: front face (against the controller plate) down; in-use Z vertical. The tooth
     is rigid; its 45 degree V grows from the frame and a small foot, no supports.

Key numbers (refs/joinery/snap_fits.md formulas, [derived] here)
  Arm: L = 26 mm (root to hook land), h = 2.25 mm (5 x 0.45 extrusion width),
  b = 6.5 mm, constant section, root fillets 1.0 / 1.2 mm (0.44 h / 0.53 h).
  Deflection per arm: hook 1.3 - gap 0.3 = 1.0 mm nominal, 1.14 mm with B's Y play
  (dovetail fit 0.12 / cos 30). Strain eps = y h / (0.67 L^2) = 0.50% nominal,
  0.57% worst, bending stress along the layers; limit 1.2% repeated in-layer PLA.
  The outer slot (2.0 mm) is a hard stop: eps at the stop 0.83% < 2.0% one-time.
  Engagement after play: 1.3 - 0.3 - 0.14 = 0.86 mm (>= 0.5 rule of section 4).
  Forces (E = 2.2 GPa, mu = 0.5, unverified): P = b h^2 E eps / (6 L) = 2.3 N
  per arm; push-on 2 x 1.51 P = 7 N; pull-off at 45 degrees 2 x 3.0 P = 14 N
  (9 to 19 N for mu 0.3 to 0.6).
  Dovetails: baseline values (fit 0.12, flank 30 deg), interlocking_and_press_fits.md
  section 1; tune with controller2_slide_mount's fit_coupon.

Dimensions: refs/ac_infinity_controller2.md (manufacturer specs, not measured).

In-use frame (mm), same as controller2_slide_mount:
  X = width, centered on the controller; x=-plate_w/2 is the cabinet wall side
  Y = up; y=0 is the bottom edge of the controller's front plate
  Z = depth, +Z back into the cabinet; z=0 is B's front face (seated)
layout: "print", "assembled" (children [A, B] or [A, B, unit] with show_unit=True),
"fit_test" (B's flat frame plus snap fork/tooth coupons).
"""
import math

from build123d import Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, extrude, loft


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
    groove_wall: float = 3.0,
    # Dovetail rails (on A)
    rail_h: float = 4.0,
    rail_base: float = 6.0,
    rail_angle: float = 30.0,
    rail_y: float = 18.5,
    lead: float = 1.0,          # 45-degree lead-in on rail fronts and groove mouths
    # Snap fork (arms on A) and tooth (on B)
    arm_len: float = 26.0,      # arm root to hook land center
    arm_h: float = 2.25,        # arm thickness in Y (bending direction), 5 extrusion widths
    arm_above: float = 3.5,     # arm height above A's plate face (total b = wall_t + this)
    arm_slot: float = 2.0,      # outer slot = over-deflection stop
    root_r_in: float = 1.2,     # inner (tension side) root fillet
    tip_gap: float = 0.5,       # arm tips to B's frame back face
    hook: float = 1.3,          # hook height (undercut)
    hook_land: float = 0.6,
    lead_angle: float = 30.0,   # hook lead-in, from the insertion axis
    ret_angle: float = 45.0,    # retention face; <= 45 so B's tooth V prints unsupported
    tooth_w: float = 10.0,      # tooth width in Y
    tooth_gap: float = 0.3,     # tooth side to arm inner face, seated (arms unloaded)
    tooth_flat: float = 2.0,    # straight side length of the tooth
    notch_play: float = 0.3,    # tooth V to hook retention face along Z, seated
    tooth_wall_clear: float = 0.5,  # tooth bottom to A's back (wall) face
    foot_half: float = 2.0,     # foot under the tooth's V tip (supports it in B's print)
    rib_ext: float = 4.0,       # arm's above-plate part continues this far past the root
    E_mpa: float = 2200.0,      # printed PLA modulus (snap_fits.md: 2.2 to 3.3 GPa)
    mu: float = 0.5,            # printed-on-printed friction (unverified)
    # A (wall piece)
    wall_t: float = 3.0,
    depth: float = 100.0,
    ceiling_w: float = 25.0,
    ceiling_t: float = 3.0,
    ceiling_gap: float = 0.5,
    brace: float = 4.0,
    brace_gap: float = 2.0,
    a_relief: float = 0.5,
    strip_w: float = 19.0,      # Large hook-and-loop strip width (two on the wall face)
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
    y_play = fit / math.cos(math.radians(rail_angle))
    arm_b = wall_t + arm_above
    sn = snap_numbers(arm_len, arm_h, arm_b, hook, tooth_gap, y_play, arm_slot,
                      z_root - z_ft, E_mpa, mu, lead_angle, ret_angle)

    # ---- asserts: real geometric and strength constraints ----
    assert layout in ("print", "assembled", "fit_test"), f"unknown layout {layout!r}"
    assert body_w < cut_w and body_h < cut_h, "body must fit the opening"
    assert xw <= xl, "B's side web must sit on the frame's left leg"
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
    assert a_relief > 0, "controller plate would touch A's front edge"
    # Fork sits in B's open channel between the groove blocks, with room to spare
    ch0, ch1 = rys[0] + gh + groove_wall, rys[1] - gh - groove_wall
    assert ch0 + 1 <= yc - d_slot and yc + d_slot <= ch1 - 1, "fork arms hit B's groove blocks"
    # Fork window leaves full-width bands for the two wall strips (no strip on the arms)
    assert yc - d_slot - arm_slot / 2 >= strip_w + 1, "no room for the lower wall strip"
    assert y_top - (yc + d_slot + arm_slot / 2) >= strip_w + 1, "no room for the upper wall strip"
    assert depth - a_relief >= 92 + 2, "wall plate shorter than a Large strip"
    # Arm tops clear B's web even with B pushed against the wall plate
    assert (xg - fit) - x_arm >= 0.3, "arm tops rub B's web"
    # Tooth clears A's wall face (with B pushed toward the wall) and the arms when seated
    assert x_bot - fit > -W, "tooth would stick out of A's wall face"
    assert tooth_gap - y_play >= 0.1, "tooth touches an arm when seated (arms must sit unloaded)"
    # Tooth V grows from B's frame/foot (no floating start in B's print)
    assert z_vtip <= frame_t, f"tooth V tip at z={z_vtip:.2f} floats above the frame"
    assert foot_half >= (frame_t - z_vtip) * tr + 0.2, "foot narrower than the tooth at the frame"
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
    assert ret_angle <= 45, "tooth V would overhang more than 45 deg in B's print"
    assert mu * tr < 1, "retention face would lock (not releasable by pulling)"
    assert arm_h >= 4 * 0.45, "arm thinner than 4 extrusion widths"

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
        th += _box(x_bot, xb + 0.01, yc - foot_half, yc + foot_half, 0, frame_t)
        return th

    # ---------------- B: front piece ----------------
    frame = _box(xb, W, 0, H, 0, frame_t)
    frame -= _box(xl, -xl, cut_b, cut_t, -1, frame_t + 1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            frame -= _zcyl(sx * hx, cy + sy * hy, pilot_d, -1, frame_t + 1)

    if layout == "fit_test":
        # Frame (screw check) + a short fork coupon (A-style, wall face down) + a tooth
        # coupon (B-style, front face down) with a web to hold. Slide the tooth into the
        # fork along the arms to feel the click and the pull-off.
        cz0 = a_relief
        coup_a = _box(-W, xa, yc - d_slot - 4, yc + d_slot + 4, cz0, z_root + rib_ext + arm_above + 3)
        coup_a -= fork_cut(cz0 - 1)
        coup_a += fork_arms()
        coup_b = tooth() + _box(xb, xg + 0.01, yc - foot_half, yc + foot_half, 0, frame_t)
        coup_b += _box(xg, xw + 2, yc - d_slot - 2, yc + d_slot + 2, 0, z_tback + 8)
        f = _lay_flat(frame)
        a = _lay_flat(Rot(0, -90, 0) * coup_a, y_offset=H + 10)
        b = Pos(60, 0, 0) * _lay_flat(coup_b, y_offset=H + 10)
        return Compound(children=[f, a, b])

    B = frame
    B += _box(xg, xw, shelf_t - 0.01, H - shelf_t + 0.01, frame_t - 0.01, b_depth)
    for yr in rys:
        B += _box(xb, xg + 0.01, yr - gh - groove_wall, yr + gh + groove_wall, frame_t - 0.01, b_depth)
        x0 = xb - 1
        B -= _xy_prism([(x0, yr - groove_half(x0)), (xg, yr - gh), (xg, yr + gh), (x0, yr + groove_half(x0))],
                       frame_t, b_depth + 1)
        sec = lambda z, e: Plane.XY.offset(z) * Polygon(
            (x0, yr - groove_half(x0) - e), (xg, yr - gh - e), (xg, yr + gh + e), (x0, yr + groove_half(x0) + e),
            align=None)
        B -= loft([sec(b_depth - lead, 0), sec(b_depth + 0.01, lead)])
    shelf = [(xb, frame_t), (W, frame_t), (W, frame_t + shelf_tip), (xw, b_depth), (xb, b_depth)]
    B += _xz_prism(shelf, 0, shelf_t)
    B += _xz_prism(shelf, H - shelf_t, H)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * hx, cy + sy * hy
            boss = _zcyl(x, y, boss_d, frame_t - 0.01, frame_t + boss_h)
            B += boss & _box(xb, W, 0, H, 0, frame_t + boss_h + 1)
            B -= _zcyl(x, y, pilot_d, -1, frame_t + boss_h + 1)
    B += tooth()

    # ---------------- A: wall piece ----------------
    A = _box(-W, xa, 0, y_top, a_relief, depth)
    A += _box(xa - 0.01, xa + ceiling_w, y_ceil0, y_top, a_relief, depth)
    A += _xy_prism([(xa - 0.01, y_ceil0 - brace), (xa - 0.01, y_ceil0), (xa + brace, y_ceil0)],
                   b_depth + brace_gap, depth)
    for yr in rys:
        A += _xy_prism([(xa - 0.01, yr - rail_half(xa)), (xt, yr - rail_half(xt)),
                        (xt, yr + rail_half(xt)), (xa - 0.01, yr + rail_half(xa))],
                       frame_t + fit, b_depth)
        rz0 = frame_t + fit
        A -= _xz_prism([(xt - lead, rz0 - 0.01), (xt + 0.01, rz0 - 0.01), (xt + 0.01, rz0 + lead)],
                       yr - rail_half(xt) - 1, yr + rail_half(xt) + 1)
    A -= fork_cut(a_relief - 1)
    A += fork_arms()

    if layout == "assembled":
        parts = [A, B]
        if show_unit:
            unit = _box(-body_w / 2, body_w / 2, body_b, body_t, 0, body_d)
            unit += _box(-W, W, 0, H, -plate_t, 0)
            parts.append(unit)
        return Compound(children=parts)

    a = _lay_flat(Rot(0, -90, 0) * A)    # in-use +X becomes print +Z (wall face down)
    b = _lay_flat(B, y_offset=y_top + 10)
    return Compound(children=[a, b])
