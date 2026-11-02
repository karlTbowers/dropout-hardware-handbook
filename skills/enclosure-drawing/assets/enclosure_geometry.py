#!/usr/bin/env python3
"""{{BOARD_TITLE}} enclosure geometry: the spec for the enclosure drawing.

Starting point from the handbook's enclosure-drawing skill (spec format: the skill's
references/spec.md). scripts/enclosure_drawing.py, the skill's engine copied into this
repo, draws the views from spec() at docs build time.

Positions come from the PCB itself (footprints() reads {{BOARD}}.kicad_pcb), so the
drawing follows the layout. Everything the enclosure adds is a named assumption below.
Replace every EXAMPLE value; record where each cutout dimension comes from.

Enclosure frame, seen from outside: origin at the front-left-bottom outer corner, x along
the front face, y back from the front face, z up.

    python3 scripts/enclosure_geometry.py       # print the spec
"""
import json
import re
from pathlib import Path

PCB = Path(__file__).resolve().parent.parent / "{{BOARD}}.kicad_pcb"

# Enclosure assumptions: PROVISIONAL until an enclosure is chosen.
WALL = 3.0             # EXAMPLE: wall, floor and lid thickness
EDGE_GAP = 0.5         # EXAMPLE: board edge to the inside of a wall that carries connectors
FLOOR_Z = 6.0          # EXAMPLE: height of the board's bottom face above the outer bottom
LID_GAP = 5.0          # EXAMPLE: tallest part to the inside of the lid
TALLEST = 27.4         # EXAMPLE: tallest part above the board (from its drawing or STEP model)
THICKNESS = 1.6        # board thickness

CUTOUT_TYPES = {
    # EXAMPLE: Amphenol "recommended panel cutout", drawing C-AT13-2P-BMXX rev. A2.
    # Near edge 4.8 above the board, mating axis 13.8.
    "AT13": {"shape": "keyed", "name": "AT13-2P-BM04", "width": 18.16, "full": 14.87, "total": 18.03,
             "tab": 11.18, "corner": 4.32, "near": 13.8 - 4.8, "holes": 25.40, "hole_d": 3.94,
             "seal": [35.20, 27.69]},
}


def footprints():
    """ref -> (x, y, rotation, side) for every footprint on the PCB, in KiCad mm (y down)."""
    text = PCB.read_text()
    out = {}
    for m in re.finditer(r'\(footprint "[^"]*"(.*?)\n\t\)', text, re.S):
        body = m.group(1)
        at = re.search(r'\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', body)
        ref = re.search(r'\(property "Reference" "([^"]+)"', body)
        layer = re.search(r'\n\t\t\(layer "([^"]+)"\)', body)
        if at and ref:
            out[ref.group(1)] = (float(at.group(1)), float(at.group(2)), float(at.group(3) or 0),
                                 "bottom" if layer and layer.group(1) == "B.Cu" else "top")
    return out


def board_outline():
    """(x0, y0, x1, y1) of the Edge.Cuts rectangle, in KiCad mm."""
    m = re.search(r'\(gr_rect\s*\(start ([-\d.]+) ([-\d.]+)\)\s*\(end ([-\d.]+) ([-\d.]+)\).*?\(layer "Edge.Cuts"\)',
                  PCB.read_text(), re.S)
    x0, y0, x1, y1 = map(float, m.groups())
    return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)


def spec():
    bx0, by0, bx1, by1 = board_outline()
    # EXAMPLE mapping for a board mounted component side up, front face along KiCad's bottom
    # edge (largest y). Enclosure x = KiCad x from the left inner wall; y = depth from the front.
    ex = lambda x: x - bx0 + EDGE_GAP + WALL
    ey = lambda y: by1 - y + EDGE_GAP + WALL
    z0 = FLOOR_Z
    z1 = z0 + THICKNESS
    fp = footprints()
    cutouts = []
    for ref, label in (("J1", "OUT1"), ("J2", "OUT2")):          # EXAMPLE: connectors on the front face
        x, y, rot, side = fp[ref]
        # EXAMPLE: the footprint origin is pin 1; the cutout centre is the pin-pair centre (pin 1 + 2.7).
        cutouts.append({"ref": ref, "label": label, "face": "front", "type": "AT13",
                        "x": ex(x + 2.7), "z": z1 + 13.8, "near_edge": "down"})
    outside = {"x": bx1 - bx0 + 2 * (EDGE_GAP + WALL), "y": by1 - by0 + 2 * (EDGE_GAP + WALL),
               "z": z1 + TALLEST + LID_GAP + WALL}
    return {
        "title": "{{BOARD_TITLE}} enclosure",
        "outside": outside,
        "wall": WALL,
        "board": {"x0": ex(bx0), "x1": ex(bx1), "y0": ey(by1), "y1": ey(by0), "z0": z0, "z1": z1,
                  "note": "component side (z1) faces the lid"},
        "levels": [{"z": WALL, "label": "floor, inside"}, {"z": outside["z"] - WALL, "label": "lid, inside"}],
        "cutout_types": CUTOUT_TYPES,
        "cutouts": cutouts,
        "assumptions": {"edge_gap": EDGE_GAP, "lid_gap": LID_GAP},
    }


if __name__ == "__main__":
    print(json.dumps(spec(), indent=1))
