from __future__ import annotations
import gdsfactory as gf
from pic_template.circuits import wdm_filter, waveguide_array
from pic_template.pdk.layers import LAYER

@gf.cell
def top() -> gf.Component:
    """Top-level photonic integrated circuit.
    
    Demonstrates use of circuit building blocks:
    - WDM filter with 4 wavelength channels
    - Waveguide array for multi-channel distribution
    """
    c = gf.Component("TOP")

    # Create WDM filter as main signal processing block
    wdm = c << wdm_filter(n_channels=4)
    wdm.movex(50)
    
    # Add waveguide array as output distribution
    array = c << waveguide_array(n_channels=4, spacing=50.0)
    array.movex(300)
    
    # Add label
    label = c << gf.components.text("PIC TEMPLATE v2", size=20, layer=LAYER.TEXT)
    label.move((c.xmin, c.ymax + 50))

    return c
