"""Simple straight waveguide component - a minimal example to copy."""

from __future__ import annotations
import gdsfactory as gf
from pic_template.pdk.cross_section import xs_rib


@gf.cell
def straight_waveguide(
    length: float = 100.0,
    xs=xs_rib,
) -> gf.Component:
    """Simple straight waveguide for interconnects.
    
    This is a minimal example showing the simplest possible component.
    Use this as a template to create your own custom components.
    
    Parameters
    ----------
    length : float
        Length of the waveguide in micrometers (default 100 µm).
        Longer waveguides incur more propagation loss.
        Typical values for testing: 10-1000 µm.
    
    xs
        Cross-section definition (default: rib waveguide).
        Controls the waveguide shape and layer stack.
    
    Returns
    -------
    gf.Component
        A straight waveguide with input and output ports.
    
    Example
    -------
    Create a 50 µm straight waveguide:
    >>> wg = straight_waveguide(length=50)
    >>> wg.write_gds('straight.gds')
    
    Use in a larger design:
    >>> from pic_template.chips.top import top
    >>> c = gf.Component('test')
    >>> wg = c << straight_waveguide(length=100)
    """
    return gf.components.straight(length=length, cross_section=xs)
