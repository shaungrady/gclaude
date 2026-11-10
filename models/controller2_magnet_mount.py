"""Two-piece magnetic cabinet wall mount for the AC Infinity Controller 2 (AI-ATC).

Concept
  A (wall piece): wall plate (two hook-and-loop strips on the cabinet's left wall),
    ceiling flange (one strip on the ceiling), two "docks" (blocks at the back of
    the joint, each with a glued 10 x 3 mm magnet), and two diamond-section locating
    pins that lie on the wall plate and point forward out of the docks.
  B (front piece): frame the controller screws to (all 4 screws), shelves, a side
    web against A's wall plate, two blind diamond sockets that slide over A's pins,
    and two magnet pads behind the controller body, each with a 10 x 3 mm magnet
    sealed in during the print (pause).
  B slides straight back (+Z) onto the pins; the magnets pull it the last ~3 mm
  home and hold it against the docks. Nothing flexes.

Use / assembly
  0. Print layout="fit_test" first: B's 4 mm frame (hold it against the controller
     to check the 123 x 67 screw spacing and the pilot size) plus a pin coupon and a
     socket coupon with both magnet pockets. The pin must slide into the socket
     without wobble; a magnet must drop into the B pocket and press into the A pocket.
  1. Polarity: stack all 4 magnets into one column and put a marker dot on the TOP
     face of every magnet while it is in the stack. All dots are now the same pole.
  2. Print B with a pause (M601) at the layer printing at z = 35.4 mm (pocket top at
     35.2 = zj - b_skin; the pause goes on the next 0.2 mm layer). Check it in the
     slicer preview: PrusaSlicer inserts the pause before the selected layer. At the pause, put a drop of CA
     in each pocket and drop the magnets in DOT DOWN (undotted face up, toward A).
     Resume; 4 layers (0.8 mm) close over them.
  3. Glue A's two magnets into the teardrop pockets in the docks' front faces with
     CA, DOT OUT (facing forward, toward B). Push each to the pocket floor; it sits
     ~0.3 mm below the dock face. Check before the glue sets: B's pads must pull
     toward the docks; if one pushes away, flip that A magnet.
  4. Screw the controller to B on the bench (all 4 screws reachable).
  5. Stick A to the cabinet wall (2 large strips along the plate, 19 x 92) and the
     ceiling (1 strip on the flange). Wait for the strip adhesive before loading.
  6. Hold B square to the wall, slide it back onto the pins until the magnets
     snap it home. Leave ~40 mm of cable slack behind the controller.
  To remove: grab the controller and pull straight forward, ~20 to 25 N (2 to 2.5 kgf),
  then slide it 20 mm off the pins.

Load path
  Weight (-Y) and the roll moment from the controller hanging 64 mm out from the
  wall: B's socket faces bear on the pins (shear); the top pin takes the roll
  couple's +X pull (about 4 N), B's lower left face bears on A's wall plate.
  Yaw from bracing the right edge (pulling it forward while pressing buttons):
  the front of B's side web bears on A's wall plate, the pins take +X at the back.
  Pushing back: B's pads bear on the docks. Pulling forward: only the magnets.
  The pins are horizontal, so B cannot slide off under its own weight even
  without magnets; the magnets only resist forward separation.

Print orientations
  A: wall face down (in-use +X up). The pins lie on the plate (45-degree flanks,
     flat 2.4 mm base on the plate), and are loaded along their extrusions. The A
     magnet pockets are horizontal teardrops (tip up) so they print without support.
  B: front face down (z = 0 on the bed). Pad and socket-block undersides are
     45-degree chamfers. The B magnet pockets are closed cavities under a 10.3 mm
     bridge resting ~0.2 mm above the magnet.

Key numbers (refs/joinery/*)
  - Magnets: 10 x 3 mm N52 discs, axial. K&J D62-N52 (9.5 x 3.2) is rated 2.48 kg
    to a steel plate (K&J product page). A coaxial charge model (Br 1.44 T) gives
    2.90 kg for that case, so its outputs are scaled by 0.86. Pair gap here =
    0.8 mm B skin + 0.3 mm A recess = 1.1 mm: model 14.3 N/pair, scaled 12.3 N;
    with Br 1.30 (undergraded "N52") 10.0 N. Two pairs: 20 to 25 N to pull B off
    [derived]. Pull-in at 3 mm gap: ~11 N (self-seating) [derived].
  - Holding: pitch from weight (~0.1 Nm) vs top magnet x 61 mm = 0.6 Nm; roll
    (~0.26 Nm) and yaw are taken by the pins, not the magnets [derived].
  - Clearance: pin to socket 0.12 mm normal to each face (snug/locating fit,
    fdm_fundamentals.md); B side face to A wall plate 0.1 mm.
  - Magnet pockets: B 10.3 mm (vertical hole, prints ~0.1 to 0.3 small, drop-in);
    pause before the first layer above the pocket; pocket top on the 0.2 mm grid;
    CA drop against jumping to the nozzle (adhesives_and_splitting.md sec. 8).
    A pocket 10.3 mm teardrop, glued with CA (pull-out depends on the adhesive, sec. 8).
  - N-grade NdFeB is limited to 80 C (sec. 8); PLA softens first (55 C).
  - Stray field: 28 mT 10 mm from a magnet face on axis, 5 mT at 20 mm [derived,
    analytic on-axis]. The nearest body corner is ~6 mm from B's magnets; parts
    deeper than ~15 mm in see < 10 mT. No relay or Hall sensor is known in the
    controller (unverified).
  - Walls >= 1.2 mm except where asserted otherwise; overhangs 45 degrees.

Dimensions: refs/ac_infinity_controller2.md (manufacturer specs, not yet measured).

In-use frame (mm), same as controller2_slide_mount.py:
  X = width, centered on the controller; x=-plate_w/2 is the cabinet wall
  Y = up; y=0 is the bottom edge of the controller's front plate
  Z = depth, +Z back into the cabinet; z=0 is B's front face (seated)
layout: "print", "assembled" (children [A, B, unit] when show_unit=True),
"fit_test" (B's frame plus pin/socket/magnet-pocket coupons).
"""
import math

from build123d import Box, Compound, Cone, Cylinder, Plane, Polygon, Pos, Rot, extrude, loft


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, d, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)


def _xy_prism(pts, z0, z1):
    return extrude(Plane.XY.offset(z0) * Polygon(*pts, align=None), amount=z1 - z0, dir=(0, 0, 1))


def _xz_prism(pts, y0, y1):
    # Plane.XZ maps local (u, v) to global (X, Z); its normal is -Y.
    return extrude(Plane.XZ.offset(-y0) * Polygon(*pts, align=None), amount=y1 - y0, dir=(0, 1, 0))


def _lay_flat(shape, x_offset=0.0, y_offset=0.0):
    bb = shape.bounding_box()
    return Pos(-bb.min.X + x_offset, -bb.min.Y + y_offset, -bb.min.Z) * shape


def build(
    plate_w: float = 135.0,     # controller front plate
    plate_h: float = 79.0,
    plate_t: float = 2.0,       # controller plate thickness (unverified)
    body_w: float = 112.0,      # controller body behind the plate
    body_h: float = 68.0,
    body_d: float = 26.0,       # 28 overall minus plate_t (unverified)
    cut_w: float = 114.0,       # opening for the body
    cut_h: float = 70.0,
    hole_dx: float = 123.0,     # controller screw spacing (template + product photo)
    hole_dy: float = 67.0,
    pilot_d: float = 2.6,       # M3 / #4 thread-forming; size to the real screws
    screw_max: float = 12.0,    # longest controller screw
    layer: float = 0.2,
    min_wall: float = 1.2,
    # B (front piece)
    frame_t: float = 4.0,
    boss_d: float = 7.0,
    boss_h: float = 4.0,
    shelf_t: float = 3.0,
    shelf_tip: float = 8.0,
    web_t: float = 2.5,         # B's side web (bears on A's wall plate)
    wall_gap: float = 0.1,      # B's left face to A's wall plate
    body_clear: float = 0.5,    # B to the controller body (sides and back face)
    zj: float = 36.0,           # joint plane: B's back face = A's dock face
    # Locating pins (on A) and sockets (in B)
    pin_hd: float = 4.0,        # half diagonal of the diamond section
    pin_h: float = 6.5,         # pin height off the wall plate (diamond top truncated)
    pin_neck: float = 2.4,      # flat base width on the wall plate
    pin_len: float = 20.0,      # forward of the dock face = engagement
    pin_y: float = 6.5,         # pin centers from the plate's top/bottom edges
    pin_clear: float = 0.12,    # socket clearance normal to each face
    pin_tip_gap: float = 0.5,   # pin tip to socket bottom
    sock_wall: float = 1.7,     # B material beside each socket (Y)
    lead: float = 1.0,          # 45-degree flare on the socket mouths
    # Magnets: 10 x 3 mm N52 discs, axially magnetized
    mag_d: float = 10.0,
    mag_t: float = 3.0,
    mag_y: float = 18.0,        # magnet centers from the plate's top/bottom edges
    mag_x: float = 6.5,         # magnet centers from A's wall plate inner face
    b_pocket_d: float = 10.3,   # drop-in during the print pause
    b_pocket_h: float = 3.2,    # magnet 3.0 +/- 0.1
    b_skin: float = 0.8,        # 4 layers over B's magnets
    a_pocket_d: float = 10.3,   # glued (CA)
    a_pocket_h: float = 3.4,    # magnet sits ~0.3 below A's dock face
    pad_x: float = 13.5,        # B magnet pad width from A's wall plate face
    pad_wall: float = 1.6,      # pad material beside the magnet pocket (Y)
    dock_w: float = 15.5,       # A dock width from the wall plate face
    dock_t: float = 5.0,        # A dock depth behind the joint plane
    # A (wall piece)
    wall_t: float = 3.0,
    depth: float = 100.0,       # wall plate depth
    ceiling_w: float = 25.0,    # ceiling flange width (strip is 19)
    ceiling_t: float = 3.0,
    ceiling_gap: float = 0.5,
    brace: float = 4.0,         # 45-degree brace under the ceiling flange
    a_relief: float = 0.5,      # A starts this far behind B's front face
    strip_w: float = 19.0,      # hook-and-loop large strip
    strip_l: float = 92.0,
    layout: str = "print",
    show_unit: bool = False,
):
    W = plate_w / 2
    H = plate_h
    cy = H / 2
    r2 = math.sqrt(2)
    xa = -W + wall_t                 # A wall plate inner face
    xb = xa + wall_gap               # B's left face
    xw = xb + web_t                  # B's side web inner face
    xbody = -body_w / 2 - body_clear  # nothing of B right of this in front of the body's back
    zbody = body_d + body_clear      # ... unless behind this
    xl = -cut_w / 2
    cut_b, cut_t = cy - cut_h / 2, cy + cut_h / 2
    body_b, body_t = cy - body_h / 2, cy + body_h / 2
    hx, hy = hole_dx / 2, hole_dy / 2
    y_ceil0 = H + ceiling_gap
    y_top = y_ceil0 + ceiling_t
    pys = [pin_y, H - pin_y]
    mys = [mag_y, H - mag_y]
    xm = xa + mag_x
    x_pin_top = xa + pin_h
    z_pin0 = zj - pin_len
    z_sock0 = z_pin0 - pin_tip_gap
    nk = pin_neck / 2

    def pin_profile(y, c):
        """Diamond pin on the wall plate (center xa + pin_hd), grown by c normal to each face."""
        e = c * r2
        xn = xa + nk + c - e                       # neck side meets the lower 45-degree face
        xt = x_pin_top + c
        ht = 2 * pin_hd - (xt - xa) + e            # half width at the truncated top
        x0 = xa - 0.01 if c == 0 else xb - 1.0     # sockets run out through B's left face
        return [(x0, y - nk - c), (xn, y - nk - c), (xa + pin_hd, y - pin_hd - e), (xt, y - ht),
                (xt, y + ht), (xa + pin_hd, y + pin_hd + e), (xn, y + nk + c), (x0, y + nk + c)]

    sock_hw = pin_hd + pin_clear * r2              # socket half width (Y)
    wedge = (xa + nk + pin_clear - pin_clear * r2) - xb  # thinnest B wall beside the socket slot
    za_pad = zbody - (xbody - xw)                  # pad chamfer starts on the web at this z
    xpad = xa + pad_x
    rb, ra = b_pocket_d / 2, a_pocket_d / 2
    zb1 = zj - b_skin                              # B pocket top (the pause goes on the next layer)
    zb0 = zb1 - b_pocket_h
    z_pad_at = lambda x: za_pad + (x - xw)         # pad underside (45 degrees)
    pocket_floor_wall = (zb0 - z_pad_at(xm + rb)) / r2
    zs_sock = z_sock0 - min_wall - (x_pin_top + pin_clear - xw)  # socket block chamfer start
    mag_gap = b_skin + (a_pocket_h - mag_t)
    on_grid = lambda z: abs(z / layer - round(z / layer)) < 1e-6

    assert layout in ("print", "assembled", "fit_test"), f"unknown layout {layout!r}"
    assert body_w < cut_w and body_h < cut_h, "body must fit the opening"
    assert xw <= xl, "B's side web must sit on the frame's left leg"
    assert hx + boss_d / 2 <= W and hx - boss_d / 2 > body_w / 2, "right bosses must clear body and edge"
    assert shelf_t < body_b and H - shelf_t > body_t, "shelves hit the body"
    # Pins and sockets
    assert pin_h < 2 * pin_hd and pin_h > pin_hd, "pin top must truncate the diamond above its widest point"
    assert x_pin_top + pin_clear + min_wall <= xbody, "socket block runs into the controller body"
    assert wedge >= 0.86, f"B wall beside the socket slot {wedge:.2f} mm < 2 perimeters"
    assert pys[0] - sock_hw - sock_wall >= -1e-6, "bottom socket wall runs below B"
    assert screw_max - plate_t < z_sock0 - 1 and frame_t + boss_h + 1 + pilot_d / 2 < z_sock0 - 1, \
        "screw or pilot reaches a socket"
    assert zs_sock >= frame_t, "socket block chamfer starts inside the frame"
    for yp, ym in zip(pys, mys):
        assert abs(ym - yp) >= sock_hw + max(rb, ra) + min_wall, "magnet pocket runs into a pin/socket"
    # Magnets
    assert xm - rb - xb >= 0.86 and xpad - (xm + rb) >= min_wall, "B magnet pocket walls too thin (X)"
    assert pocket_floor_wall >= min_wall, f"B pocket to pad chamfer {pocket_floor_wall:.2f} mm"
    assert z_pad_at(xbody) >= zbody - 1e-6, "pad chamfer hits the controller body"
    assert on_grid(zb1) and on_grid(zj), "B pocket top / skin must land on the layer grid"
    assert b_pocket_h >= mag_t + 0.15 and b_pocket_d >= mag_d + 0.2, "B pocket too tight for a drop-in"
    assert 0.1 <= a_pocket_h - mag_t <= 0.5, "A magnet must sit 0.1 to 0.5 below the dock face"
    assert xm + ra * r2 + min_wall <= xa + dock_w, "A teardrop pocket breaks through the dock top"
    assert dock_t >= a_pocket_h + min_wall, "A dock too thin behind the magnet"
    assert dock_w >= pad_x, "dock must back the whole pad"
    # A
    assert a_relief > 0, "controller plate would touch A's front edge"
    assert depth - a_relief >= strip_l and y_top >= 2 * strip_w + 5, "wall face too small for two strips"
    assert ceiling_w >= strip_w + 2, "ceiling flange too narrow for a strip"
    assert depth >= zj + dock_t + 10, "wall plate too short behind the docks"
    assert ceiling_gap > 0, "B would rub the ceiling flange"

    # ---------------- B: front piece ----------------
    def b_frame():
        f = _box(xb, W, 0, H, 0, frame_t)
        f -= _box(xl, -xl, cut_b, cut_t, -1, frame_t + 1)
        for sx in (-1, 1):
            for sy in (-1, 1):
                f -= _zcyl(sx * hx, cy + sy * hy, pilot_d, -1, frame_t + 1)
        return f

    def b_socket_block(yp, z_lo, z_hi):
        y0, y1 = yp - sock_hw - sock_wall, yp + sock_hw + sock_wall
        y0, y1 = max(y0, 0.0), min(y1, H)
        blk = _xz_prism([(xb, z_lo), (xw, z_lo), (xbody, z_lo + xbody - xw), (xbody, z_hi), (xb, z_hi)],
                        y0, y1)
        blk -= _xy_prism(pin_profile(yp, pin_clear), z_hi - pin_len - pin_tip_gap, z_hi + 1)
        sec = lambda z, c: Plane.XY.offset(z) * Polygon(*pin_profile(yp, c), align=None)
        blk -= loft([sec(z_hi - lead, pin_clear), sec(z_hi + 0.01, pin_clear + lead)])
        return blk

    def b_pad(ym, z_hi):
        y0, y1 = ym - rb - pad_wall, ym + rb + pad_wall
        pad = _xz_prism([(xb, za_pad), (xw, za_pad), (xpad, z_pad_at(xpad)), (xpad, z_hi), (xb, z_hi)],
                        y0, y1)
        pad -= _zcyl(xm, ym, b_pocket_d, z_hi - b_skin - b_pocket_h, z_hi - b_skin)
        return pad

    def a_pin(yp, z_root):
        return _xy_prism(pin_profile(yp, 0), z_root - pin_len, z_root + 0.01)

    def a_pocket(ym, z_face):
        p = _zcyl(xm, ym, a_pocket_d, z_face - 0.01, z_face + a_pocket_h)
        p += _xy_prism([(xm + ra / r2, ym - ra / r2), (xm + ra * r2, ym), (xm + ra / r2, ym + ra / r2)],
                       z_face - 0.01, z_face + a_pocket_h)
        return p

    B = b_frame()
    # Side web, full height between the shelves
    B += _box(xb, xw, shelf_t - 0.01, H - shelf_t + 0.01, frame_t - 0.01, zj)
    # Shelves: full depth at the side web, tapering to the right
    shelf = [(xb, frame_t), (W, frame_t), (W, frame_t + shelf_tip), (xw, zj), (xb, zj)]
    B += _xz_prism(shelf, 0, shelf_t)
    B += _xz_prism(shelf, H - shelf_t, H)
    # Socket blocks (pins) and magnet pads (behind the body)
    for yp in pys:
        B += b_socket_block(yp, zs_sock, zj)
    for ym in mys:
        B += b_pad(ym, zj)
    # Bosses and pilots for all 4 controller screws
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * hx, cy + sy * hy
            boss = _zcyl(x, y, boss_d, frame_t - 0.01, frame_t + boss_h)
            B += boss & _box(xb, W, 0, H, 0, frame_t + boss_h + 1)
            # Pilot 1 mm past the boss, with a 45-degree drill point (the left pilots end
            # half inside the side web, so a flat end would be a small bridge)
            zp = frame_t + boss_h + 1
            rp = pilot_d / 2
            B -= _zcyl(x, y, pilot_d, -1, zp - 0.01)
            B -= Pos(x, y, zp - 0.5 + (rp + 0.5) / 2) * Cone(rp + 0.5, 0, rp + 0.5)
    # Re-cut the sockets (the shelves and bosses overlap them near the top/bottom)
    for yp in pys:
        B -= _xy_prism(pin_profile(yp, pin_clear), z_sock0, zj + 1)

    # ---------------- A: wall piece ----------------
    A = _box(-W, xa, 0, y_top, a_relief, depth)
    A += _box(xa - 0.01, xa + ceiling_w, y_ceil0, y_top, a_relief, depth)
    A += _xy_prism([(xa - 0.01, y_ceil0 - brace), (xa - 0.01, y_ceil0), (xa + brace, y_ceil0)],
                   zj + dock_t, depth)
    dock_h = mag_y + ra + 2
    A += _box(xa - 0.01, xa + dock_w, 0, dock_h, zj, zj + dock_t)
    A += _box(xa - 0.01, xa + dock_w, H - dock_h, y_ceil0 + 0.01, zj, zj + dock_t)
    for yp in pys:
        A += a_pin(yp, zj)
    for ym in mys:
        A -= a_pocket(ym, zj)

    if layout == "fit_test":
        # B's flat frame (screw spacing), plus the bottom joint cut out of the real A
        # and B: one pin + dock + glued-magnet pocket, one socket + pad. The coupon's
        # B pocket is opened so the drop-in fit can be tried before the real print.
        frame = _lay_flat(b_frame())
        yc = mag_y + max(ra, rb) + 2
        ca = A & _box(-W - 1, xa + dock_w + 1, 0, yc, z_sock0 - 2, zj + dock_t)
        cb = B & _box(xb - 1, xpad + 1, 0, yc, frame_t, zj)
        cb -= _zcyl(xm, mys[0], b_pocket_d, zb0, zj + 1)
        ca = _lay_flat(Rot(0, -90, 0) * ca, y_offset=H + 10)
        cb = _lay_flat(cb, x_offset=40, y_offset=H + 10)
        return Compound(children=[frame, ca, cb])

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

