# PIC Template

A Python-based template for designing Photonic Integrated Circuits (PICs) using **gdsfactory**.

## Overview

This repository provides a starter scaffold for photonic chip design and layout. It includes:

- **Reusable photonic components** (ring resonators, waveguides, etc.)
- **Custom PDK** (Process Design Kit) with layer definitions and cross-section specifications
- **Example chip designs** demonstrating component assembly
- **GDS output pipeline** for chip fabrication

Perfect for researchers and engineers building photonic devices, filters, modulators, and integrated photonic systems.

## Installation

### Prerequisites
- Python 3.12 or higher
- `uv` package manager ([install uv](https://docs.astral.sh/uv/getting-started/installation/))

### Setup

```bash
git clone https://github.com/yourusername/pic-gdsfactory-uv.git
cd pic-gdsfactory-uv
make setup
```

This project uses `uv` for fast, reliable dependency management and is configured with the `uv_build` backend.

## Quick Start

### Using Make (Recommended)

```bash
# Generate GDS files
make build

# View design interactively
make show

# Run design rule check (DRC)
make drc

# Run DRC and open violations in KLayout
make drc-gui
```

### Available Make Commands

```bash
make setup      # Install/sync environment from lockfile
make build      # Export GDS files to build/gds/
make show       # Open interactive viewer for top() design
make test       # Run unit tests
make lint       # Check code quality with ruff
make drc        # Run design rule check (requires klayout)
make drc-gui    # Run DRC and open report in KLayout
make clean      # Remove all generated files
make help       # Show all available targets
```

## Project Structure

```
pic-gdsfactory-uv/
├── src/pic_template/
│   ├── components/             # Photonic building blocks (ring_racetrack, straight_waveguide)
│   ├── chips/                  # Top-level chip designs (top.py example)
│   ├── circuits/               # Higher-level circuit assemblies (extensible)
│   ├── flows/                  # Design workflows (DRC, verification, simulation)
│   ├── pdk/                    # Process Design Kit (layers, cross-sections)
│   ├── config/                 # Project configuration (config.yaml)
│   └── utils/                  # Utility functions
├── tests/                      # Unit tests
├── scripts/                    # Build scripts (build_top.py)
├── docs/                       # Documentation (extensible)
├── build/                      # Generated files (git-ignored)
│   ├── gds/                    # GDS files for fabrication
│   └── reports/                # DRC and verification reports
├── Makefile                    # Build automation
├── pyproject.toml              # Project configuration
├── README.md
└── LICENSE
```

## Features
Educational**: Detailed docstrings and comments throughout to learn photonic design
- **Custom PDK support**: Define your own waveguide cross-sections and layer stack
- **Centralized configuration**: Manage all paths and settings in `config/config.yaml`
- **Design rule checking**: Integrated DRC workflow with KLayout
- **GDS export**: Generate layout files ready for fabrication
- **Interactive visualization**: View designs with gdsfactory's built-in tools

## Configuration

All project paths and settings are defined in `src/pic_template/config/config.yaml`:

```yaml
gds:
  top: "build/gds/top.gds"

drc:
  rules: "klayout/drc_simple_test.drc"
  report: "build/reports/drc_report.lyrdb"
  fail_on_violations: false
```

**To use a different project/foundry**, create a new config file and set the environment variable:
```bash
PICTEMPLATE_CONFIG=config/config_foundry_a.yaml make build
```

## Example Components

The template includes two example components to learn from:

### Ring Racetrack (`components/rings.py`)
A coupled resonator for wavelength filtering. Parameters:
- `radius`: Bend radius (affects compactness and loss)
- `length_x`: Straight section length (affects Q-factor)
- `gap`: Coupling gap to bus (affects resonance depth)

### Straight Waveguide (`components/straight.py`)
A simple interconnect waveguide - the minimal component structure to copy when creating your own.

Both include detailed docstrings explaining the physics and typical parameter ranges.

## Dependencies

- **gdsfactory** - Photonic CAD framework
- **pydantic** - Data validation
- **pyyaml** - Configuration file handling

See `pyproject.toml` for full dependency list.

## Documentation

For detailed guides on advanced topics, see the `docs/` directory (extensible).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Related Resources

- [gdsfactory documentation](https://gdsfactory.github.io/)
- [Photonic design resources](https://en.wikipedia.org/wiki/Photonic_integrated_circuit)