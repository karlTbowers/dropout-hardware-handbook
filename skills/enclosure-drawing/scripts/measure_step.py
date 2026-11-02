#!/usr/bin/env python3
"""Measure a connector's height above the board from its STEP model (enclosure-drawing skill).

Manufacturer drawings often give the panel cutout but not how high it sits above the
board. The library's 3D models sit in the footprint frame (board top at z = 0), so a
slice through the part's mating shroud gives its extents, and the shroud centre is the
mating axis. Run with the library's CadQuery environment:

    ~/.cache/dropout/klt-venv/bin/python measure_step.py MODEL.step [--y0 -27 --y1 -18]

Without --y0/--y1 it prints the whole body's bounding box. With them it prints the
bounding box of the slice between those y values (footprint frame; the mating face is
usually toward -y in a KiCad model) and the shroud centre: width along x, height along z.
Record what you measured, and from which model, next to the value in the board's spec.
"""
import argparse

import cadquery as cq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step")
    ap.add_argument("--y0", type=float)
    ap.add_argument("--y1", type=float)
    a = ap.parse_args()
    shape = cq.importers.importStep(a.step)
    bb = shape.val().BoundingBox()
    print(f"body: x {bb.xmin:.2f}..{bb.xmax:.2f}  y {bb.ymin:.2f}..{bb.ymax:.2f}  z {bb.zmin:.2f}..{bb.zmax:.2f}"
          f"  (height above the board {bb.zmax:.2f})")
    if a.y0 is None or a.y1 is None:
        return
    y0, y1 = sorted((a.y0, a.y1))
    big = 4 * max(bb.xlen, bb.zlen, 50)
    cut = cq.Workplane().box(big, y1 - y0, big).translate(((bb.xmin + bb.xmax) / 2, (y0 + y1) / 2, 0))
    s = shape.intersect(cut).val().BoundingBox()
    print(f"slice y {y0}..{y1}: x {s.xmin:.2f}..{s.xmax:.2f} ({s.xlen:.2f} wide, centre {(s.xmin + s.xmax) / 2:.2f})"
          f"  z {s.zmin:.2f}..{s.zmax:.2f} ({s.zlen:.2f} tall, centre {(s.zmin + s.zmax) / 2:.2f} = axis height)")


if __name__ == "__main__":
    main()
