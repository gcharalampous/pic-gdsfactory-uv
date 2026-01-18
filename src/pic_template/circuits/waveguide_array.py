"""Multi-channel waveguide array circuit.

Demonstrates parallel waveguide channels arranged in a grid pattern.
This is a fundamental building block for WDM systems, phased arrays,
and multi-channel signal distribution.

This circuit shows:
- Array composition patterns
- 2D spatial arrangement
- Multi-port signal distribution
- Regular channel spacing
"""

from __future__ import annotations
import gdsfactory as gf
from gdsfactory.typings import ComponentSpec
from pic_template.components.straight import straight_waveguide
from pic_template.pdk.cross_section import xs_strip


@gf.cell
def waveguide_array(
    n_channels: int = 4,
    length: float = 100.0,
    spacing: float = 10.0,
    cross_section: ComponentSpec = xs_strip,
) -> gf.Component:
    """Multi-channel waveguide array.
    
    Arranges N parallel waveguides with uniform spacing. Useful for:
    - Multi-wavelength systems where different wavelengths use different channels
    - Phased arrays for beam steering
    - Parallel signal paths in signal distribution networks
    
    Parameters
    ----------
    n_channels : int
        Number of parallel waveguides.
    length : float
        Length of each waveguide (µm).
    spacing : float
        Center-to-center spacing between adjacent channels (µm).
    cross_section : ComponentSpec
        Waveguide cross-section.
    
    Returns
    -------
    gf.Component
        Waveguide array with labeled input/output ports.
    
    Notes
    -----
    Port naming convention:
    - "in_{i}" : input port for channel i
    - "out_{i}" : output port for channel i
    """
    c = gf.Component(f"waveguide_array_{n_channels}ch")
    
    # Create and place waveguides
    for i in range(n_channels):
        wg = straight_waveguide(length=length, xs=cross_section)
        ref = c << wg
        
        # Place at y-offset
        ref.movey(i * spacing)
        
        # Add input/output ports with channel numbering
        c.add_port(f"in_{i}", port=ref.ports["o1"])
        c.add_port(f"out_{i}", port=ref.ports["o2"])
    
    return c


if __name__ == "__main__":
    c = waveguide_array(n_channels=6, spacing=15.0)
    c.show()
