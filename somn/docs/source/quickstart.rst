.. _quickstart:

Quick Start Guide
=================

Get up and running with Somn in 5 minutes.

Basic Usage
-----------

**1. Initialize Somn**

.. code-block:: python

   from smart_office_assistant import Somn

   # Create instance
   somn = Somn()

   # Initialize the system
   await somn.initialize()

**2. Process a Task**

.. code-block:: python

   # Analyze a problem
   result = await somn.analyze(
       "How to optimize team productivity?"
   )

   print(result.solution)
   print(f"Confidence: {result.confidence}")

**3. Get Recommendations**

.. code-block:: python

   # Get wisdom-based recommendations
   recommendations = await somn.get_recommendations(
       context={"task": "project_planning"},
       max_results=5
   )

   for rec in recommendations:
       print(f"- {rec.text}")

Advanced Usage
--------------

Multi-Model Mode
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Enable A/B dual-model mode
   somn = Somn(
       model_config={
           "primary": "model_a",
           "secondary": "model_b",
           "fallback_enabled": True
       }
   )

Reasoning Mode Selection
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Use specific reasoning engine
   result = await somn.analyze(
       "Complex multi-step problem",
       reasoning_engine="GoT"  # Options: LongCoT, ToT, GoT, ReAct
   )

Batch Processing
~~~~~~~~~~~~~~~

.. code-block:: python

   # Process multiple tasks
   tasks = ["task1", "task2", "task3"]
   results = await somn.batch_process(tasks)

   for task, result in zip(tasks, results):
       print(f"{task}: {result.status}")

Configuration Examples
----------------------

Minimal Config
~~~~~~~~~~~~~~

.. code-block:: yaml

   # config/minimal.yaml
   model:
     provider: "local"
     model_path: "./models/llama-3b"

   memory:
     data_dir: "./data"
     max_size_gb: 5

Full Config
~~~~~~~~~~~

See :doc:`installation` for complete configuration options.

Common Tasks
------------

**Task: Research Query**

.. code-block:: python

   result = await somn.research(
       query="What are the best practices for X?",
       depth="comprehensive"
   )

**Task: Document Analysis**

.. code-block:: python

   result = await somn.analyze_document(
       path="./documents/report.pdf",
       summary_length=500
   )

**Task: Code Review**

.. code-block:: python

   result = await somn.review_code(
       code_path="./src/main.py",
       standards=["pep8", "security"]
   )

Next Steps
----------

* Read the :doc:`architecture` overview
* Explore the :doc:`api/index` documentation
* Check :doc:`guides/index` for detailed guides