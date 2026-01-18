"""Configuration management for PIC template projects.

Load configuration from YAML file to make it easy to switch between
different projects or foundries.
"""

from pathlib import Path
import yaml


def load_config(config_file: Path = None) -> dict:
    """Load configuration from YAML file.
    
    Parameters
    ----------
    config_file : Path, optional
        Path to config YAML file. If None, uses default location.
    
    Returns
    -------
    dict
        Configuration dictionary
    
    Raises
    ------
    FileNotFoundError
        If config file doesn't exist
    """
    if config_file is None:
        config_file = Path(__file__).parent / "config.yaml"
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    # Process template variables (e.g., {project.name})
    project_name = config.get("project", {}).get("name", "pic_template")
    config_str = yaml.dump(config)
    config_str = config_str.replace("{project.name}", project_name)
    config = yaml.safe_load(config_str)
    
    return config


def get_config() -> dict:
    """Get default configuration."""
    return load_config()
