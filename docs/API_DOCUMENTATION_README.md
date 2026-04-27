# Somn API Documentation

This directory contains auto-generated API documentation for the Somn project.

## Building the Documentation

```bash
# Install dependencies
pip install sphinx sphinx-rtd-theme sphinx-autodoc2 napoleon

# Build documentation
cd docs
make html

# Or use sphinx-build directly
sphinx-build -b html source build
```

## Documentation Structure

```
docs/
├── source/           # Sphinx source files
│   ├── conf.py       # Sphinx configuration
│   ├── index.rst     # Main index
│   ├── api/          # Auto-generated API docs
│   └── guides/       # Manual guides
├── build/            # Generated HTML output
└── Makefile         # Build automation
```

## Adding Documentation

### For Modules

Add docstrings in the following format:

```python
def function_name(param: type) -> return_type:
    """
    Brief description of function.

    Extended description if needed.

    Args:
        param: Description of parameter

    Returns:
        Description of return value

    Raises:
        ExceptionType: When this exception is raised

    Example:
        >>> result = function_name(value)
    """
```

### For Classes

```python
class MyClass:
    """
    Brief description of class.

    Extended description of class purpose and usage.

    Attributes:
        attr1: Description of first attribute
        attr2: Description of second attribute
    """

    def method(self, arg: str) -> bool:
        """
        Method description.

        Args:
            arg: Description of argument

        Returns:
            True if successful
        """
```

## Auto-generate from Code

The documentation is auto-generated from docstrings in the source code.
Run the build process after modifying docstrings to update the docs.

## Checking Coverage

```bash
# Check docstring coverage
python -m pydocstyle smart_office_assistant/src
```

## Quick Start

1. Install sphinx: `pip install sphinx sphinx-rtd-theme`
2. Initialize: `sphinx-quickstart docs`
3. Configure: Edit `docs/source/conf.py`
4. Build: `sphinx-build -b html docs/source docs/build`