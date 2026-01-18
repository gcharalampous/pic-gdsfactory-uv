from __future__ import annotations
import gdsfactory as gf
from pic_template.pdk.cross_section import xs_rib

@gf.cell
def ring_racetrack(
    radius: float = 10.0,
    length_x: float = 20.0,
    gap: float = 0.2,
    bus_length: float = 40.0,
    xs=xs_rib,
) -> gf.Component:
    """Asymmetric racetrack resonator coupled to a straight bus waveguide.
    
    A racetrack is a ring resonator with two curved sections and two straight sections.
    This is commonly used for wavelength filtering and resonant mode selection in
    photonic integrated circuits.
    
    Parameters
    ----------
    radius : float
        Radius of curvature for the curved sections (micrometers).
        Smaller radius = tighter bends = more compact but higher loss.
        Typical range: 5-50 µm depending on foundry.
    
    length_x : float
        Length of the straight sections of the racetrack (micrometers).
        Longer length = higher Q-factor (sharper filtering).
        Typical range: 10-100 µm.
    
    gap : float
        Coupling gap between the ring and bus waveguide (micrometers).
        Smaller gap = stronger coupling = lower Q and wider linewidth.
        Typical range: 0.05-1 µm. Control this to tune resonance depth.
    
    bus_length : float
        Length of the bus waveguide (micrometers).
        Should be long enough to span the racetrack.
        Default 40 µm is suitable for typical designs.
    
    xs
        Cross-section for the waveguides (default: rib waveguide).
        Can be changed to 'strip' for different mode confinement.
    
    Returns
    -------
    gf.Component
        Component containing the racetrack and bus waveguide with ports.
        Ports: ring input/output and bus ports for measurements.
    
    Notes
    -----
    This is a simple coupling design for demonstration. Real designs would
    include optimization for coupling strength, group delay, and fabrication
    tolerances.
    
    Example
    -------
    >>> ring = ring_racetrack(radius=15, length_x=30, gap=0.3)
    >>> ring.write_gds('my_ring.gds')
    """
    c = gf.Component("ring_racetrack")

    ring = c << gf.components.ring_asymmetric(radius=radius, length_x=length_x, cross_section=xs)
    bus = c << gf.components.straight(length=bus_length, cross_section=xs)

    # Simple placement (not precision coupling design—template only)
    bus.x = ring.x
    bus.ymin = ring.ymin - gap - 0.5

    c.add_ports(ring.ports)
    c.add_ports(bus.ports, prefix="bus_")
    return c