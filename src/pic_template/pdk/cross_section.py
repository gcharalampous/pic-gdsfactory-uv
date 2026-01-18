from __future__ import annotations
import gdsfactory as gf
from .layers import LAYER

def xs_strip(wg_width: float = 0.5):
    """Strip waveguide cross-section (single-layer silicon core).
    
    A strip waveguide is just the silicon core without a slab underneath.
    High confinement but higher loss. Used for very compact designs.
    
    Parameters
    ----------
    wg_width : float
        Width of the waveguide in micrometers (default 0.5 µm).
        For single-mode operation in silicon at 1.55 µm:
        - 0.4-0.6 µm: strong confinement, low loss
        - >1 µm: weak confinement, multiple modes
    
    Returns
    -------
    gf.CrossSection
        A strip waveguide cross-section ready for use in components.
    """
    return gf.cross_section.cross_section(
        width=wg_width,
        layer=LAYER.WG,
        radius=10,
    )

def xs_rib(wg_width: float = 0.5, slab_width: float = 2.0):
    """Rib waveguide cross-section (silicon core with slab underneath).
    
    A rib waveguide has a raised core with a shallow slab underneath.
    Lower loss than strip (less scattering) but less compact.
    Most common in commercial silicon photonics processes.
    
    Parameters
    ----------
    wg_width : float
        Width of the raised core (default 0.5 µm).
        Controls mode confinement and loss.
    
    slab_width : float
        Width of the shallow slab extending beyond the core (default 2.0 µm).
        Larger slab = lower mode confinement but lower waveguide loss.
        Typical values: 1-4 µm depending on process.
    
    Returns
    -------
    gf.CrossSection
        A rib waveguide cross-section.
    
    Notes
    -----
    The slab layer (LAYER.SLAB150) is defined by a shallow etch in your foundry.
    Check your foundry's design rules for slab depth and its effect on mode
    confinement.
    
    Example
    -------
    >>> xs = xs_rib(wg_width=0.5, slab_width=2.0)
    >>> straight = gf.components.straight(cross_section=xs)
    """
    return gf.cross_section.cross_section(
        width=wg_width,
        layer=LAYER.WG,
        sections=(gf.Section(width=slab_width, layer=LAYER.SLAB150, offset=0),),
        radius=10,
    )
