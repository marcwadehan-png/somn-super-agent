.. _installation:

Installation
============

Prerequisites
-------------

* Python 3.10 or higher
* Windows/Linux/macOS
* 4GB RAM minimum (8GB recommended)
* 2GB disk space

Standard Installation
---------------------

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/marcwadehan-png/somn-agent.git
   cd somn

   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt

Development Installation
-------------------------

.. code-block:: bash

   # Install in development mode
   pip install -e .

   # Run tests
   pytest somn/tests/

Configuration
-------------

1. Copy the example configuration:

   .. code-block:: bash

      cp config/config.example.yaml config/config.yaml

2. Edit ``config/config.yaml`` with your settings:

   .. code-block:: yaml

      model:
        provider: "local"
        model_path: "path/to/model"

      memory:
        data_dir: "data/"
        max_size_gb: 10

      wisdom:
        schools_path: "smart_office_assistant/claws/"

Verification
------------

.. code-block:: bash

   # Run the test suite
   pytest somn/tests/ -v

   # Verify installation
   python -c "from smart_office_assistant import Somn; print('OK')"

Troubleshooting
--------------

**Import errors**: Ensure you're in the project root directory.

**Model not found**: Check the model_path in config.yaml.

**Memory errors**: Increase max_size_gb or clean old data.