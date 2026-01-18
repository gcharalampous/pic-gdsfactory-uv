"""Tests for DRC and geometry verification."""

import pytest
from pathlib import Path
from pic_template.components.straight import straight_waveguide
from pic_template.components.rings import ring_racetrack
from pic_template.circuits.wdm_filter import wdm_filter
from pic_template.flows.geometry_check import GeometryChecker, verify_component
from pic_template.config import get_config


def test_geometry_checker_on_straight_waveguide():
    """Test geometry checker with straight waveguide."""
    wg = straight_waveguide(length=100)
    checker = GeometryChecker(wg)
    
    # Run individual checks
    assert checker.check_port_count(expected_count=2)
    assert checker.check_port_widths()
    assert checker.check_port_orientations()


def test_geometry_checker_detects_no_ports():
    """Test that checker detects missing ports."""
    import gdsfactory as gf
    empty = gf.Component("empty")
    checker = GeometryChecker(empty)
    
    # Should fail port count check
    assert not checker.check_port_count()
    assert len(checker.violations) > 0


def test_geometry_checker_run_all():
    """Test running all checks at once."""
    wg = straight_waveguide()
    results = verify_component(wg)
    
    assert "component_name" in results
    assert "checks" in results
    assert "violations" in results
    assert "passed" in results
    
    # Straight waveguide should pass all checks
    assert results["passed"]


def test_geometry_checker_on_ring():
    """Test geometry checker with ring racetrack."""
    ring = ring_racetrack()
    results = verify_component(ring)
    
    # Ring should have valid geometry
    assert results["checks"]["port_count"]
    assert results["checks"]["port_widths"]
    assert results["checks"]["port_orientations"]


def test_geometry_checker_on_circuit():
    """Test geometry checker with WDM filter circuit."""
    wdm = wdm_filter(n_channels=2)
    results = verify_component(wdm)
    
    # WDM should have correct number of ports
    assert results["checks"]["port_count"]


def test_drc_rules_file_exists():
    """Test that DRC rules files exist."""
    simple_drc = Path("klayout/drc_simple_test.drc")
    enhanced_drc = Path("klayout/drc_enhanced.drc")
    
    assert simple_drc.exists(), "Simple DRC file not found"
    assert enhanced_drc.exists(), "Enhanced DRC file not found"


def test_drc_script_can_run():
    """Test that DRC flow script can be imported without errors."""
    from pic_template.flows import run_drc
    
    # Should be able to import
    assert hasattr(run_drc, 'run')


def test_drc_config_valid():
    """Test that DRC configuration is valid."""
    config = get_config()
    drc_config = config["drc"]
    
    # Check required fields
    assert "rules" in drc_config
    assert "report" in drc_config
    
    # Check that rules file exists
    rules_path = Path(drc_config["rules"])
    assert rules_path.exists(), f"DRC rules file {rules_path} not found"


def test_port_width_validation():
    """Test that port width checker works correctly."""
    wg = straight_waveguide()
    checker = GeometryChecker(wg)
    
    # Should pass with default waveguide
    assert checker.check_port_widths(min_width=0.3, max_width=2.0)
    
    # Should fail if we set impossible constraints
    assert not checker.check_port_widths(min_width=10.0)
    assert len(checker.violations) > 0


def test_bounding_box_constraints():
    """Test bounding box constraint checking."""
    wg = straight_waveguide(length=100)
    checker = GeometryChecker(wg)
    
    # Should pass with reasonable limits
    assert checker.check_bounding_box(max_width=200, max_height=200)
    
    # Should fail with tight limits
    checker2 = GeometryChecker(wg)
    assert not checker2.check_bounding_box(max_width=10, max_height=10)


@pytest.mark.parametrize("component_func,expected_ports", [
    (straight_waveguide, 2),
    (ring_racetrack, 2),  # Has bus_o1 and bus_o2
])
def test_component_port_counts(component_func, expected_ports):
    """Test that components have expected port counts."""
    comp = component_func()
    
    # Allow >= expected_ports since some components may have additional ports
    assert len(comp.ports) >= expected_ports


def test_verification_summary_format():
    """Test that verification results have expected format."""
    wg = straight_waveguide()
    results = verify_component(wg)
    
    # Check structure
    assert isinstance(results, dict)
    assert isinstance(results["checks"], dict)
    assert isinstance(results["violations"], list)
    assert isinstance(results["passed"], bool)
    assert isinstance(results["component_name"], str)
    
    # Each check should be a boolean
    for check_name, check_result in results["checks"].items():
        assert isinstance(check_result, bool), f"{check_name} should be bool"
