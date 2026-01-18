# Setup Guide

Getting started with the PIC template project.

## Prerequisites

- **Python 3.12+** - [Download Python](https://www.python.org/downloads/)
- **Git** - For version control
- **uv** - Fast Python package manager (auto-installed by `make setup`)

## Installation

### Quick Start (Recommended)

```bash
# Clone the repository
git clone https://github.com/georgios/pic-gdsfactory-uv.git
cd pic-gdsfactory-uv

# Run setup (installs uv, dependencies, and pre-commit hooks)
make setup
```

### Manual Setup

```bash
# Install uv
pip install uv

# Install dependencies
uv sync

# Run tests to verify installation
uv run pytest
```

## Verify Installation

```bash
# Build GDS files
make build

# Run all tests
uv run pytest -v

# Check DRC
uv run python -m pic_template.flows.verify
```

If all commands complete without errors, you're ready to design!

## Project Structure

```
src/pic_template/          # Main package
├── components/            # Photonic component definitions (rings, waveguides)
├── circuits/             # Circuit-level designs (WDM filter, arrays)
├── chips/                # Top-level chip layouts
├── config/               # Configuration (YAML settings, paths)
├── pdk/                  # Process Design Kit (layers, cross-sections)
├── flows/                # Design flows (DRC, verification)
└── utils/                # Utility functions

tests/                     # Test suite (config, ports, parametric, verification)

build/                     # Generated files
├── gds/                  # GDS output files
└── reports/              # DRC and verification reports

klayout/                   # DRC rules and KLayout scripts
```

## Key Commands

### Development

```bash
# Run tests
uv run pytest

# Run specific test file
uv run pytest tests/config_test.py -v

# Run with coverage
uv run pytest --cov=src/pic_template

# Format code
uv run black src/

# Type checking
uv run mypy src/
```

### Design

```bash
# Build GDS (creates build/gds/top.gds)
make build

# View GDS in KLayout
klayout build/gds/top.gds

# Run verification (DRC + geometry checks)
uv run python -m pic_template.flows.verify

# View verification report
cat build/reports/verification_summary.txt
```

### Configuration

Edit `src/pic_template/config/config.yaml` to:
- Change GDS output path
- Configure DRC rules
- Set design parameters

Use environment variable to load alternative configs:
```bash
PICTEMPLATE_CONFIG=config/custom.yaml make build
```

## Troubleshooting

### Import Errors
```bash
# Reinstall package in editable mode
uv sync --reinstall
```

### GDS Not Building
```bash
# Check config file
cat src/pic_template/config/config.yaml

# Check build directory exists
mkdir -p build/{gds,reports}
```

### DRC Failures
```bash
# Install KLayout if not present
sudo apt-get install klayout  # Linux
brew install klayout          # macOS

# Verify KLayout can run
klayout --version
```

## Next Steps

- **Create Components** - See [COMPONENTS.md](COMPONENTS.md)
- **Design Circuits** - See [WORKFLOW.md](WORKFLOW.md)
- **Write Tests** - See project tests/ directory for examples
