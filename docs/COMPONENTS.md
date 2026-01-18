# Component Development Guide

How to design and use photonic components in the PIC template.

## Component Basics

Components are reusable building blocks - the fundamental unit in gdsfactory. Each component:
- Defines geometry (GDS polygons)
- Specifies ports (connection points)
- Takes parameters (dimensions, materials, etc.)

## Example Components

### Ring Resonator (`src/pic_template/components/rings.py`)

A wavelength-selective component using a curved waveguide coupled to a bus.

```python
from gdsfactory import Component
from pic_template.pdk import xs_strip

@gf.cell
def ring_racetrack(
    radius: float = 10.0,
    length_x: float = 5.0,
    gap: float = 0.2,
) -> Component:
    """Coupled ring resonator."""
    # Implementation creates curved waveguide + bus with gap
    return c
```

**Key Parameters:**
- `radius` - Bend curvature (10 µm typical, smaller = tighter curves)
- `length_x` - Straight section length (affects Q-factor)
- `gap` - Coupling gap to bus waveguide (0.1-0.5 µm range)

**Ports:**
- `o1` - Input from bus
- `o2` - Output to bus

### Straight Waveguide (`src/pic_template/components/straight.py`)

Basic interconnect waveguide.

```python
@gf.cell
def straight_waveguide(
    length: float = 10.0,
    cross_section: str = "strip",
) -> Component:
    """Straight waveguide."""
    return c
```

**Ports:**
- `o1` - Input (left)
- `o2` - Output (right)

## Creating New Components

### Step 1: Define the Function

Create a Python file in `src/pic_template/components/`:

```python
# src/pic_template/components/coupler.py

import gdsfactory as gf
from gdsfactory import Component
from pic_template.pdk import xs_strip, LAYER

@gf.cell
def directional_coupler(
    length: float = 10.0,
    gap: float = 0.5,
    width: float = 0.5,
) -> Component:
    """Directional coupler - 2x2 waveguide junction.
    
    Args:
        length: Coupling section length (µm)
        gap: Gap between parallel waveguides (µm)
        width: Waveguide width (µm)
    
    Returns:
        Component with ports: in1, in2, out1, out2
    """
    c = Component()
    
    # Draw top waveguide
    top_poly = [
        (0, gap/2 + width/2),
        (length, gap/2 + width/2),
        (length, gap/2 - width/2),
        (0, gap/2 - width/2),
    ]
    c.add_polygon(top_poly, layer=LAYER.WG)
    
    # Draw bottom waveguide
    bot_poly = [
        (0, -gap/2 - width/2),
        (length, -gap/2 - width/2),
        (length, -gap/2 + width/2),
        (0, -gap/2 + width/2),
    ]
    c.add_polygon(bot_poly, layer=LAYER.WG)
    
    # Add ports
    c.add_port("in1", port=gf.Port(
        name="in1",
        center=(0, gap/2 + width/2),
        width=width,
        orientation=180,
        layer=LAYER.WG,
    ))
    c.add_port("in2", port=gf.Port(
        name="in2",
        center=(0, -gap/2 - width/2),
        width=width,
        orientation=180,
        layer=LAYER.WG,
    ))
    c.add_port("out1", port=gf.Port(
        name="out1",
        center=(length, gap/2 + width/2),
        width=width,
        orientation=0,
        layer=LAYER.WG,
    ))
    c.add_port("out2", port=gf.Port(
        name="out2",
        center=(length, -gap/2 - width/2),
        width=width,
        orientation=0,
        layer=LAYER.WG,
    ))
    
    return c
```

### Step 2: Export the Component

Update `src/pic_template/components/__init__.py`:

```python
from .coupler import directional_coupler

__all__ = [
    "directional_coupler",
    # ... other components
]
```

### Step 3: Use in Circuits

```python
# src/pic_template/circuits/my_circuit.py
from pic_template.components import directional_coupler

@gf.cell
def coupler_circuit():
    c = gf.Component()
    coupler = directional_coupler(length=15.0, gap=0.3)
    c << coupler
    return c
```

### Step 4: Test the Component

Create `tests/coupler_test.py`:

```python
import pytest
from pic_template.components import directional_coupler

def test_coupler_ports():
    """Verify coupler has 4 ports."""
    coupler = directional_coupler()
    assert len(coupler.ports) == 4
    assert "in1" in coupler.ports
    assert "out1" in coupler.ports

def test_coupler_ports_aligned():
    """Input and output ports should be at same y."""
    coupler = directional_coupler(gap=0.5)
    assert coupler.ports["in1"].y == coupler.ports["out1"].y
```

## Component API Reference

### gdsfactory Essentials

```python
import gdsfactory as gf
from gdsfactory import Component, Port

# Create component
@gf.cell
def my_component() -> Component:
    c = Component()
    
    # Add polygon (GDS shape)
    polygon = [(0, 0), (10, 0), (10, 5), (0, 5)]
    c.add_polygon(polygon, layer=LAYER.WG)
    
    # Add port (connection point)
    port = Port(
        name="o1",
        center=(10, 2.5),
        width=0.5,
        orientation=0,  # 0=right, 90=up, 180=left, 270=down
        layer=LAYER.WG,
    )
    c.add_port("o1", port=port)
    
    # Reference another component
    other = another_component()
    ref = c << other
    ref.move((20, 0))  # Move by (x, y)
    ref.rotate(90)     # Rotate by angle
    
    # Connect ports
    c.connect("o2", ref.ports["i1"])
    
    return c
```

### Port Naming Convention

Use consistent port naming:
- `in_<number>` - Input ports (e.g., in_1, in_2)
- `out_<number>` - Output ports (e.g., out_1, out_2)
- `ch<number>_in/out` - Channel ports (e.g., ch1_in, ch1_out)
- `o1, o2, o3, o4` - Generic optical ports (numbered)

## Physics Considerations

### Ring Resonator Q-Factor

Q-factor (quality) depends on:
- **Radius**: Larger radius = higher Q (less bending loss)
- **Gap**: Smaller gap = higher Q (less coupling loss)
- **Straight length**: Longer = higher Q (less scattering)

Typical values:
- High-Q cavity: radius=30µm, gap=0.1µm, Q~10,000
- Coupling ring: radius=10µm, gap=0.3µm, Q~1,000

### Waveguide Width

Standard width: **0.5 µm**
- Smaller (0.3 µm) - Higher loss, better confinement
- Larger (0.8 µm) - Lower loss, multi-mode risk

### Bend Loss

Bending loss increases exponentially as radius decreases:
- 5 µm radius - ~0.1 dB/90° bend
- 1 µm radius - ~1 dB/90° bend (avoid!)

## Common Patterns

### Add a Grating Coupler

```python
def my_component_with_coupler():
    c = Component()
    
    # Main circuit
    core = my_circuit()
    c << core
    
    # Grating coupler for I/O
    gc = gf.components.grating_coupler_te()
    gc_ref = c << gc
    gc_ref.connect("o1", core.ports["out1"])
    
    return c
```

### Create Parametric Family

```python
@gf.cell
def ring_sweep(radius: float = gf.CONF.radius) -> Component:
    """Ring with variable radius."""
    return ring_racetrack(radius=radius, length_x=5.0)

# Generate multiple versions
radii = [5.0, 10.0, 15.0, 20.0]
rings = [ring_sweep(radius=r) for r in radii]
```

## Layer and Cross-Section Management

See `src/pic_template/pdk/layers.py` and `src/pic_template/pdk/cross_section.py`:

```python
from pic_template.pdk import LAYER, xs_strip, xs_rib

# Access layer definitions
WG_LAYER = LAYER.WG          # (1, 0)
DOPING_LAYER = LAYER.DOPING  # (7, 0)

# Use predefined cross-sections
c.add_port("o1", cross_section=xs_strip, width=0.5)
```

## Next Steps

- Review existing components in [src/pic_template/components/](../src/pic_template/components/)
- Study [WORKFLOW.md](WORKFLOW.md) for circuit design
- Run component tests: `uv run pytest tests/ports_test.py -v`
