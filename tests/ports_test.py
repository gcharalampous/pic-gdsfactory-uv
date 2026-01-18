"""Tests for component and circuit port validation."""

from pic_template.components.rings import ring_racetrack
from pic_template.components.straight import straight_waveguide
from pic_template.circuits.wdm_filter import wdm_filter
from pic_template.circuits.waveguide_array import waveguide_array


def test_straight_waveguide_has_required_ports():
    """Test that straight waveguide has both input and output ports."""
    wg = straight_waveguide()
    
    # Should have exactly 2 ports
    assert len(wg.ports) == 2, "Straight waveguide should have 2 ports"
    
    # Check port names
    port_names = [p.name for p in wg.ports]
    assert "o1" in port_names, "Should have o1 port"
    assert "o2" in port_names, "Should have o2 port"


def test_ring_racetrack_has_required_ports():
    """Test that ring racetrack has bus ports."""
    ring = ring_racetrack()
    
    # Should have at least bus ports
    assert len(ring.ports) >= 2, "Ring should have at least 2 ports"
    
    # Check for bus ports
    port_names = [p.name for p in ring.ports]
    assert "bus_o1" in port_names, "Should have bus_o1 port"
    assert "bus_o2" in port_names, "Should have bus_o2 port"


def test_wdm_filter_has_channel_ports():
    """Test that WDM filter exposes ports for each channel."""
    n_channels = 4
    wdm = wdm_filter(n_channels=n_channels)
    
    # Should have 2 ports per channel (in and out)
    expected_port_count = n_channels * 2
    assert len(wdm.ports) == expected_port_count, \
        f"WDM with {n_channels} channels should have {expected_port_count} ports"
    
    # Check port naming convention
    port_names = [p.name for p in wdm.ports]
    for i in range(n_channels):
        assert f"ch{i}_in" in port_names, f"Should have ch{i}_in port"
        assert f"ch{i}_out" in port_names, f"Should have ch{i}_out port"


def test_waveguide_array_has_indexed_ports():
    """Test that waveguide array has correctly indexed ports."""
    n_channels = 6
    array = waveguide_array(n_channels=n_channels)
    
    # Should have 2 ports per channel
    expected_port_count = n_channels * 2
    assert len(array.ports) == expected_port_count, \
        f"Array with {n_channels} channels should have {expected_port_count} ports"
    
    # Check port naming
    port_names = [p.name for p in array.ports]
    for i in range(n_channels):
        assert f"in_{i}" in port_names, f"Should have in_{i} port"
        assert f"out_{i}" in port_names, f"Should have out_{i} port"


def test_all_ports_have_valid_orientations():
    """Test that all component ports have valid orientations."""
    components = [
        straight_waveguide(),
        ring_racetrack(),
    ]
    
    valid_orientations = [0, 90, 180, 270]
    
    for component in components:
        for port in component.ports:
            assert port.orientation in valid_orientations, \
                f"Port {port.name} has invalid orientation {port.orientation}"


def test_straight_waveguide_ports_are_opposite():
    """Test that straight waveguide ports face opposite directions."""
    wg = straight_waveguide()
    
    o1 = wg.ports["o1"]
    o2 = wg.ports["o2"]
    
    # Ports should be 180 degrees apart
    orientation_diff = abs(o1.orientation - o2.orientation)
    assert orientation_diff == 180, \
        "Straight waveguide ports should face opposite directions"


def test_components_return_valid_objects():
    """Test that all components return valid Component objects."""
    components = [
        straight_waveguide(),
        ring_racetrack(),
        wdm_filter(n_channels=2),
        waveguide_array(n_channels=3),
    ]
    
    for component in components:
        assert component is not None
        assert hasattr(component, 'ports'), "Component should have ports attribute"
        assert hasattr(component, 'name'), "Component should have name attribute"


def test_port_widths_are_positive():
    """Test that all ports have positive widths."""
    components = [
        straight_waveguide(),
        ring_racetrack(),
    ]
    
    for component in components:
        for port in component.ports:
            assert port.width > 0, f"Port {port.name} has non-positive width"
