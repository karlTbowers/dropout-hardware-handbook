# Enclosure geometry spec (engine 1.0)

The board's `scripts/enclosure_geometry.py` defines `spec()`, returning this dict. `enclosure_drawing.py` draws from it and copies it, plus derived values, into `enclosure.json` for the docs page. Millimetres throughout.

## Frame

Seen from outside: origin at the **front-left-bottom outer corner**, `x` along the front face (left to right), `y` back from the front face, `z` up. "Front" is the face the user calls the front; pick it once and keep it.

Each face's view is drawn as seen from outside, and its cutouts are dimensioned from the view's lower-left corner:

| Face | Right in the view | Up in the view | Lower-left corner |
|---|---|---|---|
| `front` | `x` | `z` | front-left-bottom |
| `back` | `x`, mirrored | `z` | back-right-bottom |
| `right` | `y` (front on the left) | `z` | front-right-bottom |
| `left` | `y`, mirrored (front on the right) | `z` | back-left-bottom |
| `top` | `x` | `y` (front at the bottom) | front-left |
| `bottom` | `x`, mirrored | `y` (front at the bottom) | front-right |

You always give positions in enclosure coordinates; the engine mirrors them per face.

## Top level

| Key | Type | Meaning |
|---|---|---|
| `title` | str | Used in view titles, e.g. `"Node60 enclosure"` |
| `outside` | `{x, y, z}` | Outside size |
| `wall` | number | Wall, floor and lid thickness (inside = outside − 2 × wall on each axis) |
| `board` | `{x0, x1, y0, y1, z0, z1, note?}` | Board outline and its two faces' heights; drawn dashed in every view. `note` says which face is the component side |
| `levels` | `[{z, label}]` | Horizontal hidden lines on the wall views, dimensioned as heights: inside floor, inside lid, a shelf |
| `cutout_types` | `{NAME: type}` | One entry per connector or opening style (below) |
| `cutouts` | `[cutout]` | Every opening (below) |
| anything else | any | Copied into `enclosure.json` untouched: put board-specific values the page text needs here (`assumptions`, sources) |

## Cutout types

Every type has `shape` and an optional `name` (the part number, shown on the details sheet). The cutout's **centre** is the point you place: for a keyed or rectangular cutout it is the mating axis, where the screw holes are.

**`keyed`**: a connector panel cutout with a key or a wider band at one end, like the Deutsch/Amphenol AT, ATM and DT families.

| Key | Meaning |
|---|---|
| `width` | Slot width at the edge nearest the board |
| `full` | Length of the full-width part, from the near edge |
| `total` | Overall length, near edge to far edge |
| `tab` | Width of the far part: smaller than `width` for a key tab, larger for a wider band |
| `near` | Centre (mating axis) to the near edge |
| `corner` | Main corner radius; `small_corner` (default 0.8) for the step corners |
| `holes`, `hole_d` | Screw-hole spacing and diameter, on the axis (omit for none) |
| `seal` | `[w, h]`: the flat area the flange seal needs, centred on the axis. Used for overlap and edge checks |

Manufacturer drawings usually dimension the cutout from the board (or from the PCB surface line): `near` = axis height − near-edge height.

**`rect`**: `width`, `height`, `corner`, optional `holes`/`hole_d`/`seal`.

**`round`**: `d` (cutout diameter), optional `screw_square` + `screw` (thread name) + `screw_d` (hole drawn, default 4) for four screws on a square, and `flange` (square flange size, drawn dashed and used for checks).

## Cutouts

| Key | Meaning |
|---|---|
| `ref` | Reference designator (`J904`) |
| `label` | Short use (`OUT1`, `VBAT_IN`) |
| `face` | `front`, `back`, `left`, `right`, `top` or `bottom` |
| `type` | A key of `cutout_types` |
| `x` / `y` / `z` | The centre in enclosure coordinates: the two the face needs (`x` and `z` on front/back, `y` and `z` on left/right, `x` and `y` on top/bottom) |
| `near_edge` | `"up"` or `"down"`: where the cutout's near edge (the one nearest the board) is in the face view. `up` when the board is above the connector (board mounted component side down), `down` for a board mounted component side up. Default `up` |

## Checks

`--check` reports, and the drawing run refuses to draw when:

- a cutout's type or face is unknown;
- a cutout's envelope (its `seal`, flange or screw square, else its outline) leaves its face;
- two envelopes on one face overlap.

It does not know where the board or the inside walls are relative to a cutout's body; check headers against the walls and the floor in the board's own adapter or 3D mockup.
