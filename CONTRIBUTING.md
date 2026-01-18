# Contributing to PIC Template

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**: `git clone https://github.com/yourusername/pic-gdsfactory-uv.git`
3. **Setup environment**: `make setup`

## Development Workflow

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes**
3. **Run tests**: `make test`
4. **Check code quality**: `make lint`
5. **Build and verify**: `make build`
6. **Commit with clear messages**: `git commit -m "Add feature X"`
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create a Pull Request** on GitHub

## Code Style

- Follow PEP 8 conventions
- Use type hints where possible
- Add docstrings to functions and classes
- Run `make lint` before committing

## Adding Components

1. Create a new file in `src/pic_template/components/`
2. Follow the structure of existing components (see `straight.py` for a minimal example)
3. Include detailed docstrings explaining parameters and physics
4. Add tests if applicable

## Modifying the PDK

To change the Process Design Kit for a different foundry:

1. Update layer numbers in `src/pic_template/pdk/layers.py`
2. Update waveguide definitions in `src/pic_template/pdk/cross_section.py`
3. Create a new config in `src/pic_template/config/config_your_foundry.yaml`
4. Test with `make build`

## Testing

- Run tests with `make test`
- Write tests in `tests/` directory
- Use pytest conventions
- All new features should include tests

## Documentation

- Update README.md for major changes
- Add docstrings to all public functions
- Include examples in docstrings when helpful

## Questions?

Open an issue on GitHub or start a discussion. We're happy to help!

## License

By contributing, you agree your work will be licensed under the MIT License.
