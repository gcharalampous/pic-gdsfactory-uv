# Design Workflow Guide

Step-by-step guide to designing photonic circuits using the PIC template.

## Design Flow Overview

```
Design Specification
        ↓
Create Components (if needed)
        ↓
Assemble Circuit
        ↓
Generate GDS
        ↓
Verify (DRC + Geometry)
        ↓
Export for Fabrication
```

## Step 1: Design Specification

Define your circuit requirements:

**Example: WDM Filter**
- Input: Single waveguide with multiple wavelengths
- Output: 4 separate channels at different wavelengths
- Mechanism: Ring resonators tuned to λ₁, λ₂, λ₃, λ₄
- Footprint: < 500×500 µm²

Write this as a docstring in your circuit file:

```python
@gf.cell
def wdm_filter() -> Component:
    """Wavelength Division Multiplexer (WDM) filter.
    
    Splits input signal into 4 wavelength channels using
    cascaded ring resonators with different radii.
    
    Specifications:
    - Input: Single-mode waveguide (0.5 µm width)
    - Output: 4 channels (1µm spacing)
    - Tuning: Ring radius controls center wavelength
    - Q-factor: ~5,000 (for telecommunications)
    
    Layout:
    ┌─ Ring 1 (λ₁) ─┐
    │                ├─ Output waveguides
    Bus waveguide    │
    │                ├─ Output waveguides
    └─ Ring 2 (λ₂) ─┘
    """
```

## Step 2: Create Missing Components

If standard components (rings, waveguides) don't exist:

1. Design on paper or simulation tool
2. Implement in `src/pic_template/components/`
3. Test ports and geometry
4. Document parameters

See [COMPONENTS.md](COMPONENTS.md) for detailed guide.

## Step 3: Assemble Circuit

Create circuit file in `src/pic_template/circuits/`:

```python
# src/pic_template/circuits/wdm_filter.py
import gdsfactory as gf
from gdsfactory import Component
from pic_template.components import ring_racetrack, straight_waveguide
from pic_template.pdk import xs_strip

@gf.cell
def wdm_filter() -> Component:
    """Wavelength multiplexer using cascaded rings."""
    c = Component()
    
    # Bus waveguide (input)
    bus = straight_waveguide(length=100.0)
    bus_ref = c << bus
    
    # Ring resonators (tuned to different wavelengths)
    radii = [8.0, 10.0, 12.0, 14.0]  # Different sizes for different λ
    gap = 0.2  # Tight coupling
    
    for i, radius in enumerate(radii):
        ring = ring_racetrack(radius=radius, gap=gap)
        ring_ref = c << ring
        
        # Position ring below bus
        ring_ref.move((30 + i*25, -20.0))
        
        # Connect ring to bus
        ring_ref.connect("o1", bus_ref.ports["o2"])
    
    # Output waveguides (one per ring)
    for i in range(4):
        out_wg = straight_waveguide(length=20.0)
        out_ref = c << out_wg
        out_ref.move((30 + i*25, -40.0))
        # Connect to ring output port...
    
    # Add ports to top-level component
    c.add_port("in1", port=bus_ref.ports["o1"])
    # Add output ports...
    
    return c
```

## Step 4: Connection Methods

### Direct Port Connection

```python
# Connect component B's input to component A's output
b_ref.connect("in1", a_ref.ports["out1"])
```

### Guided Routing

```python
# Connect with a connecting waveguide
from gdsfactory.routing import route

route_info = route(
    component=c,
    port1=ref_a.ports["out1"],
    port2=ref_b.ports["in1"],
    cross_section=xs_strip,
)
```

### Manual Positioning

```python
# Absolute positioning
ring_ref.movex(30.0)  # Move 30 µm in x
ring_ref.movey(-20.0) # Move 20 µm in y
ring_ref.rotate(90)   # Rotate 90°

# Relative positioning
ring_ref.move((30.0, -20.0))
```

## Step 5: Generate GDS

```bash
# Build all circuits and generate GDS
make build

# Output: build/gds/top.gds
```

## Step 6: Verify Design

### Run Full Verification

```bash
# DRC + geometry checks
uv run python -m pic_template.flows.verify

# Output: build/reports/verification_summary.txt
```

### View Specific Results

```bash
# DRC violations
cat build/reports/drc_report.lyrdb

# Geometry check results
cat build/reports/verification_summary.txt

# Inspect GDS in KLayout
klayout build/gds/top.gds
```

### Common DRC Violations and Fixes

| Violation | Cause | Fix |
|-----------|-------|-----|
| WG.1: Width < 0.4 µm | Waveguide too narrow | Increase width to 0.5 µm |
| WG.2: Spacing < 0.2 µm | Waveguides too close | Increase separation to ≥0.3 µm |
| M1.1: Metal too thin | Poor conductivity | Route through wider traces |
| VIA.1: Via not centered | Via misalignment | Check via centering in PDK |

### Geometry Checks

Verified automatically:
- ✅ Component bounding boxes defined
- ✅ All ports have correct orientations
- ✅ Port widths match cross-section
- ✅ No unconnected ports
- ✅ Port names consistent with PDK

## Step 7: Iterate and Optimize

### Parametric Testing

```python
# Test across parameter ranges
import pytest

@pytest.mark.parametrize("radius", [5.0, 10.0, 15.0, 20.0])
def test_ring_resonators(radius):
    """Test rings with different radii."""
    ring = ring_racetrack(radius=radius)
    
    # Check all ports exist
    assert len(ring.ports) == 2
    
    # Check bounding box reasonable
    bbox = ring.bbox()
    assert bbox.width > radius * 1.5  # Room for bends
```

Run parametric tests:
```bash
uv run pytest tests/parametric_test.py -v
```

### Optimize for Performance

**Reduce Footprint:**
```python
# Smaller radius = tighter bends (but more loss)
ring = ring_racetrack(radius=8.0)  # Compact
# vs
ring = ring_racetrack(radius=15.0)  # Low-loss
```

**Reduce Loss:**
```python
# Larger radius = less bending loss
# Larger gap = less coupling loss
ring = ring_racetrack(radius=20.0, gap=0.3)
```

**Improve Spectral Response:**
```python
# Smaller gap = sharper spectral features
# Longer straight section = higher Q
ring = ring_racetrack(radius=12.0, length_x=8.0, gap=0.1)
```

## Step 8: Export for Fabrication

### Prepare Submission Package

```bash
# Copy GDS
cp build/gds/top.gds ../fabrication/chip_v1.gds

# Copy verification report
cp build/reports/verification_summary.txt ../fabrication/verification_v1.txt

# Copy design notes
cat > ../fabrication/design_notes_v1.md << EOF
# Design: WDM Filter v1

## Specifications
- Center wavelengths: 1550, 1560, 1570, 1580 nm
- Q-factor: ~5000
- Footprint: 400×300 µm²

## Key Parameters
- Ring radii: 8, 10, 12, 14 µm
- Coupling gap: 0.2 µm
- Waveguide width: 0.5 µm

## Verification Status
- DRC: PASS
- Geometry: PASS
- Fabrication ready: YES
EOF
```

## Common Workflow Patterns

### Add Version Tracking

```python
@gf.cell
def wdm_filter_v2() -> Component:
    """WDM Filter v2 - optimized for lower loss."""
    # Changes from v1:
    # - Increased ring radius 8→10 µm
    # - Tighter coupling gap 0.2→0.15 µm
    # - Longer bus 100→150 µm
```

### Create Design Variants

```python
def wdm_filter_compact():
    """Small footprint, higher loss."""
    return wdm_filter_impl(radius=8.0, gap=0.3, length=80.0)

def wdm_filter_lowloss():
    """Large footprint, low loss."""
    return wdm_filter_impl(radius=15.0, gap=0.2, length=120.0)

def wdm_filter_highq():
    """Optimized for high Q-factor."""
    return wdm_filter_impl(radius=20.0, gap=0.1, length=150.0)
```

### Document Changes

In `docs/DESIGNS.md`:
```markdown
# Design History

## v2.0 - WDM Filter (2026-01)
- 4-channel multiplexer
- Ring radii: 10, 12, 14, 16 µm
- Loss: ~2 dB insertion
- Footprint: 500×300 µm²

## v1.0 - WDM Filter (2025-12)
- Initial design
- Ring radii: 8, 10, 12, 14 µm
- Loss: ~3 dB insertion
- Issues: High bend loss
```

## Testing Your Design

```bash
# Add to tests/workflow_test.py
def test_wdm_filter_structure():
    """Verify WDM filter layout."""
    wdm = wdm_filter()
    
    # Check size reasonable
    bbox = wdm.bbox()
    assert bbox.width < 500  # µm
    assert bbox.height < 400  # µm
    
    # Check ports
    assert "in1" in wdm.ports
    assert len([p for p in wdm.ports if "out" in p]) == 4

def test_wdm_filter_drc():
    """Run DRC on WDM filter."""
    wdm = wdm_filter()
    # Build and check
    # (verification_summary will show DRC status)
```

## Next Steps

- Study existing circuits: [src/pic_template/circuits/](../src/pic_template/circuits/)
- Review test examples: [tests/](../tests/)
- Consult [COMPONENTS.md](COMPONENTS.md) when creating new parts
- See [SETUP.md](SETUP.md) for command reference
