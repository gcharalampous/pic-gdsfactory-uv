from __future__ import annotations
import gdsfactory as gf
from pic_template.components.rings import ring_racetrack
from pic_template.components.straight import straight_waveguide
from pic_template.pdk.layers import LAYER

@gf.cell
def top() -> gf.Component:
    c = gf.Component("TOP")

    # Create a 3x2 array of ring racetracks with manual placement
    ring = ring_racetrack()
    spacing_x = 200
    spacing_y = 150
    
    for i in range(3):  # columns
        for j in range(2):  # rows
            r = c << ring
            r.move((i * spacing_x, j * spacing_y))

    # Add a straight waveguide below as an example of a simple component
    straight = c << straight_waveguide(length=500)
    straight.movey(c.ymin - 100)

    # Add label
    label = c << gf.components.text("PIC TEMPLATE", size=20, layer=LAYER.TEXT)
    label.move((c.xmin, c.ymax + 50))

    return c
