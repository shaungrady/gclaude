# AC Infinity Controller 2 (AI-ATC) panel mount

Source: `ac_infinity_controller2_AI-ATC_template.pdf`
(https://acinfinity.com/content/templates/AC%20INFINITY%20Thermal%20Controller%20Template%202020.pdf),
extracted from the PDF's vector paths at 1:1 scale. AC Infinity says the template is a reference only;
verify against the real unit before printing anything that has to fit.

All mm. Origin at the plate's top-left corner, +X right, +Y down (as on the page).

| Feature | Value |
| --- | --- |
| Mounting plate outline | 135.0 × 79.0, corner radius 6.0 |
| Panel cutout | 113.0 × 69.0, square corners, centered (11.0 from left/right, 5.0 from top/bottom) |
| Screw holes (4) | centers at (6, 6), (129, 6), (6, 73), (129, 73); pattern 123.0 × 67.0 |
| Screw hole size | drawn 3.5 dia; PDF note says screws are ~2–3 mm |

## Manufacturer website specs (as published)

| Spec | Website | Template PDF | Notes |
| --- | --- | --- | --- |
| Overall | 135 × 79 × 28 | 135 × 79 | match; depth only on website |
| Backside enclosure | 112 × 68 | (not drawn) | body that passes through the panel |
| Required mounting hole | 114 × 70 | 113 × 69 | PDF is line centerline; website gives 1 mm/side clearance vs 0.5 |
| Hole to hole | **120** × 67 | **123** × 67 | **conflict in X (3 mm)**; Y agrees |
| Screw hole dia | 3.0 (0.119 in) | 3.5 drawn dot | use website value; 0.119 in suggests #4 or M3 |
| Display | 47 × 32 | (not drawn) | |

Until the X hole spacing is measured on the real unit, slot the holes in X to span 120–123.

## Resolved from product photo

Source: https://cdn11.bigcommerce.com/s-238e9/images/stencil/2048x2048/products/131/7351/StorePhoto6__86637.1655142942.jpg?c=2
Scaling the front view by the 135 mm plate width puts the hole centers ~123 × 66–67 mm apart,
matching the template. The website's 120 mm is likely wrong. Use **123 × 67**.

All ports (power, sensor, 2× USB-A fan) are on the **back** of the 112 × 68 body. Depth 28 mm overall.

## Measured on the owner's unit (calipers)

| Feature | Measured |
| --- | --- |
| Screw hole spacing | 123 x 67 mm (center to center); matches the template, not the website's 120 |
| Screw hole diameter in the plate | 5.0 mm (larger than the template's 3.5 mm dot and the website's 3.0) |
| Front plate | 134.85 x 79.0 mm, 1.6 mm thick |
| Body behind the plate | 113.15 x 69.0 mm, 26 mm deep (centering on the plate not yet confirmed) |
| Mounting screws (box) | #4-size wood screws, 2.95 mm OD, 10 mm under the head; also machine screws 2.88 mm x 33.5 mm (panel mounting, not used by the printed mount) |
| Port positions, plug sizes, cable diameters | not yet measured |
