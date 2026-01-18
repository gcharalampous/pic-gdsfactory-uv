from __future__ import annotations
from gdsfactory.typings import Layer
from gdsfactory.technology import LayerMap

class LAYER(LayerMap):
    """Layer definitions for photonic integrated circuits.
    
    Each layer is defined as a tuple (layer_number, data_type).
    Layer numbers are foundry-specific - you must update these for your process!
    
    This template is based on a generic silicon photonics process from:
    Lukas Chrostowski, Michael Hochberg, "Silicon Photonics Design",
    Cambridge University Press 2015, page 353
    
    CUSTOMIZATION GUIDE:
    1. Replace layer numbers with your foundry's layer stack
    2. Add/remove layers as needed for your process
    3. Typical process layers in silicon photonics:
       - WG: Silicon waveguide core
       - SLAB: Shallow etch regions for slab modes
       - N/P/PP: Doping layers for modulators/detectors
       - M1/M2: Metal layers for heaters and connections
       - VIA: Via layers for interconnects
       - TEXT: Annotation layer for labels (doesn't get fabricated)
    
    You can find your foundry's layer stack in their design rules (GDS2 layer map).
    """

    # Core substrate
    WAFER: Layer = (999, 0)

    # Silicon waveguide layers
    WG: Layer = (1, 0)
    WGCLAD: Layer = (111, 0)
    SLAB150: Layer = (2, 0)
    SLAB90: Layer = (3, 0)
    DEEPTRENCH: Layer = (4, 0)
    GE: Layer = (5, 0)
    UNDERCUT: Layer = (6, 0)
    WGN: Layer = (34, 0)
    WGN_CLAD: Layer = (36, 0)

    # Doping layers (for modulators, detectors)
    N: Layer = (20, 0)
    NP: Layer = (22, 0)
    NPP: Layer = (24, 0)
    P: Layer = (21, 0)
    PP: Layer = (23, 0)
    PPP: Layer = (25, 0)
    GEN: Layer = (26, 0)
    GEP: Layer = (27, 0)

    # Metal and heater layers
    HEATER: Layer = (47, 0)
    M1: Layer = (41, 0)
    M2: Layer = (45, 0)
    M3: Layer = (49, 0)
    VIAC: Layer = (40, 0)
    VIA1: Layer = (44, 0)
    VIA2: Layer = (43, 0)
    PADOPEN: Layer = (46, 0)

    # Annotation and special layers (non-fabricated)
    DICING: Layer = (100, 0)
    NO_TILE_SI: Layer = (71, 0)
    PADDING: Layer = (67, 0)
    DEVREC: Layer = (68, 0)
    FLOORPLAN: Layer = (64, 0)
    TEXT: Layer = (66, 0)
    PORT: Layer = (1, 10)
    PORTE: Layer = (1, 11)
    PORTH: Layer = (70, 0)
    SHOW_PORTS: Layer = (1, 12)
    LABEL_SETTINGS: Layer = (202, 0)
    DRC_MARKER: Layer = (205, 0)
    LABEL_INSTANCE: Layer = (206, 0)

    # Simulation/measurement layers
    SOURCE: Layer = (110, 0)
    MONITOR: Layer = (101, 0)