# Contributing to Singularity AI Layer

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/cosmic-hydra/singularity-ailayer.git
   cd singularity-ailayer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Code Quality

### Linting and Formatting

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

### Type Checking

We use [mypy](https://mypy.readthedocs.io/) for type checking:

```bash
mypy core/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov-report=html

# Run specific test file
pytest tests/test_config.py -v
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Run the test suite** to ensure nothing is broken

4. **Commit your changes** with clear, descriptive messages

5. **Push and create a Pull Request**

## Coding Standards

- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Follow PEP 8 style guidelines (enforced by Ruff)
- Keep functions focused and small
- Write unit tests for new functionality

## Commit Messages

Use clear, descriptive commit messages:

- `feat: Add new voice recognition feature`
- `fix: Resolve window focus issue on Windows 11`
- `docs: Update installation instructions`
- `test: Add tests for configuration module`
- `refactor: Simplify action parsing logic`

## Questions?

If you have questions, please open an issue or start a discussion.
