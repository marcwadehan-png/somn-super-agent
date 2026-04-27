.. _contributing:

Contributing to Somn
====================

Welcome! We're glad you're interested in contributing to Somn.

Getting Started
---------------

1. Fork the repository
2. Clone your fork: ``git clone https://github.com/marcwadehan-png/somn-agent.git``
3. Create a branch: ``git checkout -b feature/your-feature-name``
4. Make your changes
5. Run tests: ``pytest tests/``
6. Commit and push
7. Create a Pull Request

Development Setup
----------------

.. code-block:: bash

   # Clone and install
   git clone https://github.com/marcwadehan-png/somn-agent.git
   cd somn
   pip install -r requirements.txt
   pip install -r requirements-dev.txt

   # Run pre-commit hooks
   pre-commit install
   pre-commit run --all-files

Code Style
----------

* Follow PEP 8
* Use type hints where possible
* Write docstrings for public functions
* Keep lines under 120 characters

Pull Request Guidelines
------------------------

* Fill out the PR template completely
* Reference related issues
* Include tests for new features
* Update documentation as needed
* Ensure all CI checks pass

Reporting Issues
---------------

* Use GitHub Issues for bugs and feature requests
* Search existing issues before creating new ones
* Provide reproduction steps for bugs
* Include system information (Python version, OS, etc.)

License
-------

By contributing, you agree that your contributions will be licensed under the AGPL v3 License.