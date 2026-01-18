"""Circuits are reusable complex photonic elements combining multiple components.

Example circuits demonstrating hierarchical design patterns:
- wdm_filter: Cascaded ring resonators for wavelength filtering
- waveguide_array: Multi-channel parallel waveguides
"""

from pic_template.circuits.wdm_filter import wdm_filter
from pic_template.circuits.waveguide_array import waveguide_array

__all__ = ["wdm_filter", "waveguide_array"]
