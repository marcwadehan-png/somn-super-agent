.. _architecture:

System Architecture
==================

Overview
--------

Somn follows a layered architecture with clear separation of concerns.

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────┐
   │                    Presentation Layer                       │
   │              (User Interface / API Gateway)                  │
   └─────────────────────────────────────────────────────────────┘
                               ↓
   ┌─────────────────────────────────────────────────────────────┐
   │                     Agent Core Layer                         │
   │         (SomnCore, AgentCore, UnifiedIntelligence)          │
   └─────────────────────────────────────────────────────────────┘
                               ↓
   ┌─────────────────────────────────────────────────────────────┐
   │                   Intelligence Layer                         │
   │  (SuperWisdomCoordinator, GlobalWisdomScheduler, Dispatch) │
   └─────────────────────────────────────────────────────────────┘
                               ↓
   ┌─────────────────────────────────────────────────────────────┐
   │                     Wisdom Layer                            │
   │           (776+ Sages, 35 Schools, 422 Positions)          │
   └─────────────────────────────────────────────────────────────┘
                               ↓
   ┌─────────────────────────────────────────────────────────────┐
   │                    Learning Layer                           │
   │    (UnifiedLearningOrchestrator, ROI, Feedback System)     │
   └─────────────────────────────────────────────────────────────┘
                               ↓
   ┌─────────────────────────────────────────────────────────────┐
   │                    Memory Layer                             │
   │      (NeuralMemorySystem, SemanticMemory, Knowledge)        │
   └─────────────────────────────────────────────────────────────┘

Core Components
---------------

AgentCore
~~~~~~~~~

The main entry point handling user interactions.

.. code-block:: python

   class AgentCore:
       """Central agent orchestrator."""

       def __init__(self, config: dict):
           self.somn_core = SomnCore(config)
           self.intelligence = UnifiedIntelligenceCoordinator()

       async def process(self, query: str) -> Response:
           """Process user query."""
           context = await self._analyze_context(query)
           solution = await self.somn_core.resolve(context)
           return self._format_response(solution)

SomnCore
~~~~~~~~

The core reasoning and decision-making component.

.. code-block:: python

   class SomnCore:
       """Core reasoning engine with tier-based processing."""

       def __init__(self, config: dict):
           self.wisdom = SuperWisdomCoordinator()
           self.scheduler = GlobalWisdomScheduler()
           self.reasoning = ReasoningMethodFusionEngine()

       async def resolve(self, context: Context) -> Solution:
           """Resolve problem using wisdom and reasoning."""
           analysis = await self.wisdom.analyze(context)
           plan = await self.scheduler.coordinate(analysis)
           return await self.reasoning.execute(plan)

Wisdom System
-------------

The wisdom system coordinates 776+ sage claws across 35 schools.

.. code-block:: text

   Problem Analysis
        ↓
   Department Classification
        ↓
   School Selection (35 schools)
        ↓
   Sage Matching (776+ claws)
        ↓
   Claw Execution
        ↓
   Result Synthesis

Supported Schools
~~~~~~~~~~~~~~~~~

1. **Confucian (儒家)**: Ethics, governance, social harmony
2. **Daoist (道家)**: Naturalness, simplicity, spontaneity
3. **Legalist (法家)**: Rule of law, efficiency, control
4. **Military (兵家)**: Strategy, tactics, warfare
5. **Mohist (墨家)**: Universal love, pragmatism
6. **Agricultural (农家)**: Agriculture, economy
7. **Yin-Yang (阴阳家)**: Cosmology, balance
8. **Diplomatic (纵横家)**: Diplomacy, rhetoric
9. ... and 26 more schools

Reasoning Engines
-----------------

LongCoT (Long Chain of Thought)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For complex multi-step reasoning:

.. code-block:: python

   # Breaks down complex problems into sequential steps
   result = await reasoning.long_cot.analyze(
       problem,
       max_depth=15
   )

ToT (Tree of Thoughts)
~~~~~~~~~~~~~~~~~~~~~~

For exploring multiple solution paths:

.. code-block:: python

   # Generates and evaluates multiple branches
   result = await reasoning.tot.analyze(
       problem,
       beam_width=3
   )

GoT (Graph of Thoughts)
~~~~~~~~~~~~~~~~~~~~~~~

For complex interdependent reasoning:

.. code-block:: python

   # Creates reasoning graph with dependencies
   result = await reasoning.got.analyze(
       problem,
       max_nodes=100
   )

ReAct (Reasoning + Acting)
~~~~~~~~~~~~~~~~~~~~~~~~~~

For practical problem-solving with tools:

.. code-block:: python

   # Combines reasoning with tool execution
   result = await reasoning.react.solve(
       problem,
       tools=[search, calculator, file_reader]
   )

Memory System
-------------

Hierarchical memory with three tiers:

.. code-block:: text

   ┌──────────────────┐
   │ Working Memory   │  (Session context)
   │   ~100 items     │
   └──────────────────┘
            ↓
   ┌──────────────────┐
   │ Semantic Memory  │  (Concepts, patterns)
   │   ~10K items     │
   └──────────────────┘
            ↓
   ┌──────────────────┐
   │ Episodic Memory  │  (Past experiences)
   │   ~100K events   │
   └──────────────────┘

Learning System
---------------

Three-tier learning architecture:

1. **Perception Layer**: Raw input processing
2. **Reflection Layer**: Pattern extraction and synthesis
3. **Evolution Layer**: Strategy improvement

.. code-block:: python

   class UnifiedLearningOrchestrator:
       """Coordinates all learning activities."""

       def learn(self, experience: Experience) -> None:
           """Process and learn from experience."""
           perceived = self.perception.process(experience)
           reflected = self.reflection.analyze(perceived)
           self.evolution.evolve(reflected)

Data Flow
---------

.. code-block:: text

   User Input
       ↓
   Input Processing
       ↓
   Context Building
       ↓
   Problem Analysis
       ↓
   ┌────────────────────────────────────────────┐
   │         Wisdom Coordination                │
   │  ┌────────────────────────────────────┐   │
   │  │  School Selection → Sage Matching   │   │
   │  │  → Claw Execution → Result Synthesis│   │
   │  └────────────────────────────────────┘   │
   └────────────────────────────────────────────┘
       ↓
   Solution Generation
       ↓
   Learning Feedback
       ↓
   Response Output