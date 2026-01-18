"""Tests for configuration loading and management."""

from pathlib import Path
from pic_template.config import get_config


def test_config_loads_successfully():
    """Test that the default config file loads without errors."""
    config = get_config()
    assert config is not None
    assert isinstance(config, dict)


def test_config_has_required_sections():
    """Test that config contains all required top-level sections."""
    config = get_config()
    
    required_sections = ["project", "build", "gds", "drc"]
    for section in required_sections:
        assert section in config, f"Missing required config section: {section}"


def test_config_project_section():
    """Test that project section has required fields."""
    config = get_config()
    project = config["project"]
    
    assert "name" in project
    assert "description" in project
    assert isinstance(project["name"], str)
    assert len(project["name"]) > 0


def test_config_build_section():
    """Test that build section has required directories."""
    config = get_config()
    build = config["build"]
    
    assert "gds_dir" in build
    assert "reports_dir" in build
    assert isinstance(build["gds_dir"], str)
    assert isinstance(build["reports_dir"], str)


def test_config_gds_section():
    """Test that GDS section has required fields."""
    config = get_config()
    gds = config["gds"]
    
    assert "top_cell" in gds
    assert "filename" in gds
    assert isinstance(gds["top_cell"], str)
    assert isinstance(gds["filename"], str)
    assert gds["filename"].endswith(".gds")


def test_config_drc_section():
    """Test that DRC section has required fields."""
    config = get_config()
    drc = config["drc"]
    
    assert "rules" in drc
    assert "report" in drc
    assert isinstance(drc["rules"], str)
    assert isinstance(drc["report"], str)


def test_config_template_substitution():
    """Test that template variables like {project.name} are substituted."""
    config = get_config()
    
    # The filename should have project.name substituted
    gds_filename = config["gds"]["filename"]
    project_name = config["project"]["name"]
    
    # Should not contain literal template string
    assert "{project.name}" not in gds_filename
    
    # Should contain the actual project name
    assert project_name in gds_filename


def test_config_paths_are_strings():
    """Test that all path configurations are strings."""
    config = get_config()
    
    path_fields = [
        (config["build"], "gds_dir"),
        (config["build"], "reports_dir"),
        (config["gds"], "filename"),
        (config["drc"], "rules"),
        (config["drc"], "report"),
    ]
    
    for section, field in path_fields:
        assert isinstance(section[field], str), f"{field} should be a string"


def test_config_drc_fail_on_violations_is_bool():
    """Test that fail_on_violations is a boolean."""
    config = get_config()
    drc = config["drc"]
    
    if "fail_on_violations" in drc:
        assert isinstance(drc["fail_on_violations"], bool)


def test_config_can_construct_gds_path():
    """Test that we can construct a valid GDS path from config."""
    config = get_config()
    
    gds_dir = config["build"]["gds_dir"]
    gds_filename = config["gds"]["filename"]
    
    gds_path = Path(gds_dir) / gds_filename
    
    # Should be a valid path object
    assert isinstance(gds_path, Path)
    assert str(gds_path).endswith(".gds")


def test_config_drc_paths_have_correct_extensions():
    """Test that DRC file paths have expected extensions."""
    config = get_config()
    drc = config["drc"]
    
    assert drc["rules"].endswith(".drc"), "DRC rules should be .drc file"
    assert drc["report"].endswith(".lyrdb"), "DRC report should be .lyrdb file"
