.. _testing:

Testing Guide
============

Running Tests
-------------

.. code-block:: bash

   # Run all tests
   pytest tests/ -v

   # Run specific test file
   pytest tests/test_core.py -v

   # Run with coverage
   pytest tests/ --cov=smart_office_assistant --cov-report=html

   # Run in parallel
   pytest tests/ -n auto

Test Structure
--------------

::

   tests/
   ├── test_core.py          # Core functionality
   ├── test_intelligence.py  # Intelligence modules
   ├── test_memory.py        # Memory system
   ├── test_claws.py         # Wisdom claws
   ├── test_knowledge.py     # Knowledge cells
   └── test_integration.py   # Integration tests

Writing Tests
-------------

.. code-block:: python

   def test_example():
       """Test description."""
       result = some_function()
       assert result == expected_value

Continuous Integration
---------------------

All tests run automatically on:
* Every push to main/develop
* Every pull request

Coverage reports are generated and uploaded to Codecov.