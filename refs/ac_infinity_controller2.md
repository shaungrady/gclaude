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
