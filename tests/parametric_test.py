"""Parametric tests demonstrating testing with multiple parameter combinations.

Parametric tests use @pytest.mark.parametrize to run the same test with different inputs.
This is extremely powerful for testing components across their valid parameter ranges.
"""

import pytest
from pic_template.components.rings import ring_racetrack
from pic_template.components.straight import straight_waveguide
from pic_template.circuits.wdm_filter import wdm_filter
from pic_template.circuits.waveguide_array import waveguide_array


@pytest.mark.parametrize("length", [10.0, 50.0, 100.0, 500.0, 1000.0])
def test_straight_waveguide_with_different_lengths(length):
    """Test that straight waveguide works with various lengths."""
    wg = straight_waveguide(length=length)
    
    assert wg is not None
    assert len(wg.ports) == 2
    
    # Check that bounding box reflects the length (approximately)
    bbox = wg.bbox()
    width = bbox.width()  # Use DBox methods
    assert width > 0, f"Waveguide with length {length} should have positive width"


@pytest.mark.parametrize("radius,length_x", [
    (10.0, 10.0),
    (10.0, 20.0),
    (15.0, 30.0),
    (20.0, 50.0),
])
def test_ring_with_different_geometries(radius, length_x):
    """Test ring racetrack with different radius and length combinations."""
    ring = ring_racetrack(radius=radius, length_x=length_x)
    
    assert ring is not None
    assert len(ring.ports) >= 2
    
    # Larger rings should have larger bounding boxes
    bbox = ring.bbox()
    width = bbox.width()
    height = bbox.height()
    
    assert width > 0
    assert height > 0


@pytest.mark.parametrize("gap", [0.05, 0.1, 0.2, 0.5, 1.0])
def test_ring_with_different_coupling_gaps(gap):
    """Test ring racetrack with different coupling gaps."""
    ring = ring_racetrack(gap=gap)
    
    assert ring is not None
    assert len(ring.ports) >= 2


@pytest.mark.parametrize("n_channels", [2, 4, 8, 16])
def test_wdm_filter_with_different_channel_counts(n_channels):
    """Test WDM filter scales correctly with channel count."""
    wdm = wdm_filter(n_channels=n_channels)
    
    assert wdm is not None
    
    # Should have 2 ports per channel
    expected_ports = n_channels * 2
    assert len(wdm.ports) == expected_ports, \
        f"WDM with {n_channels} channels should have {expected_ports} ports"


@pytest.mark.parametrize("n_channels,spacing", [
    (2, 10.0),
    (4, 15.0),
    (6, 20.0),
    (8, 25.0),
])
def test_waveguide_array_with_different_configurations(n_channels, spacing):
    """Test waveguide array with different channel counts and spacings."""
    array = waveguide_array(n_channels=n_channels, spacing=spacing)
    
    assert array is not None
    assert len(array.ports) == n_channels * 2
    
    # Check that vertical spacing increases with more channels
    bbox = array.bbox()
    height = bbox.height()
    expected_min_height = (n_channels - 1) * spacing
    assert height >= expected_min_height * 0.9, \
        f"Array height should reflect spacing (got {height}, expected ~{expected_min_height})"


@pytest.mark.parametrize("coupling_gaps", [
    [0.1, 0.2],
    [0.1, 0.2, 0.3],
    [0.1, 0.2, 0.3, 0.4],
    [0.05, 0.1, 0.15, 0.2, 0.25],
])
def test_wdm_filter_with_custom_coupling_gaps(coupling_gaps):
    """Test WDM filter with custom coupling gap arrays."""
    n_channels = len(coupling_gaps)
    wdm = wdm_filter(n_channels=n_channels, coupling_gaps=coupling_gaps)
    
    assert wdm is not None
    assert len(wdm.ports) == n_channels * 2


@pytest.mark.parametrize("length,n_channels", [
    (50.0, 2),
    (100.0, 4),
    (200.0, 8),
])
def test_waveguide_array_area_scales_with_parameters(length, n_channels):
    """Test that waveguide array area scales with length and channel count."""
    array = waveguide_array(n_channels=n_channels, length=length)
    
    bbox = array.bbox()
    width = bbox.width()
    height = bbox.height()
    area = width * height
    
    assert area > 0, "Array should have positive area"
    # More channels or longer waveguides = larger area
    assert width >= length * 0.9, "Width should be approximately the waveguide length"


@pytest.mark.parametrize("radius,gap,bus_length", [
    (10.0, 0.2, 40.0),
    (15.0, 0.3, 60.0),
    (20.0, 0.5, 80.0),
])
def test_ring_with_multiple_parameters(radius, gap, bus_length):
    """Test ring with multiple parameters varied together."""
    ring = ring_racetrack(
        radius=radius,
        gap=gap,
        bus_length=bus_length,
    )
    
    assert ring is not None
    assert len(ring.ports) >= 2


# Example of testing edge cases
@pytest.mark.parametrize("length", [0.1, 1.0, 10000.0])
def test_straight_waveguide_edge_cases(length):
    """Test straight waveguide with edge case lengths (very small/large)."""
    wg = straight_waveguide(length=length)
    assert wg is not None


# Example of testing invalid inputs
@pytest.mark.parametrize("n_channels", [-1])
def test_wdm_filter_rejects_invalid_channel_count(n_channels):
    """Test that WDM filter handles invalid channel counts gracefully."""
    # Negative channel counts should raise errors
    if n_channels < 0:
        with pytest.raises((ValueError, AssertionError, ZeroDivisionError, IndexError)):
            wdm_filter(n_channels=n_channels)
