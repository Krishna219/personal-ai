# Personal AI Development Checkpoint

## Current Status

**Milestone 1 — Local LLM Runtime and Python Integration: COMPLETE**

**Next milestone: M2 — LangGraph Foundation**

This checkpoint is the source of truth for the project state at the end of M1.

---

# 1. Project Objective

Build a local-first Personal AI platform with specialized agents for:

- Career
- Engineering / UAV / Embedded / Laboratory
- Finance
- Health / Fitness

Core principles:

- Local ownership of personal data
- Local LLM inference where practical
- Model-independent application architecture
- Structured data as the source of truth
- Retrieval and provenance
- Explicit agent permissions
- Human approval for sensitive/destructive actions
- Deterministic Python functions for calculations
- Testability and evaluation
- Modular domain agents
- Central orchestration only after individual agents are proven

The goal is **not** to build a generic chatbot. The goal is to build a personal engineering system where the LLM is one component of a larger controlled architecture.

---

# 2. Repository State at M1

```text
personal_ai/
├── data/
│   ├── career/
│   ├── engineering/
│   ├── finance/
│   └── health/
├── docs/
│   ├── architecture.md
│   └── CHECKPOINT.md
├── src/
│   └── personal_ai/
│       ├── __init__.py
│       ├── main.py
│       └── llm.py
├── tests/
│   └── __init__.py
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml
```

The project uses the standard Python `src/` layout.

`src/personal_ai/__init__.py` is intentionally empty.

The package is installed in editable mode:

```bash
pip install -e .
```

This allows imports such as:

```python
from personal_ai.llm import generate_response
```

without modifying `sys.path`.

---

# 3. Development Environment

Python:

```text
3.12.3
```

Git:

```text
2.43.0
```

Virtual environment:

```text
.venv/
```

The virtual environment is local to the repository and excluded from Git.

---

# 4. Local LLM Infrastructure

Ollama is installed globally:

```text
/usr/local/bin/ollama
```

Ollama is intentionally a system-level runtime rather than something installed inside the project virtual environment.

Reason:

Ollama is an independent local model runtime that can serve this project and potentially other applications.

The Python Ollama client is installed inside `.venv`.

---

# 5. Current Model

Model:

```text
qwen3:4b
```

Downloaded model size:

```text
2.5 GB
```

Interactive inference was successfully verified.

---

# 6. Hardware / GPU Baseline

NVIDIA driver:

```text
580.178.04
```

GPU:

```text
NVIDIA GeForce 940MX
2 GB VRAM
```

Ollama runtime observation:

```text
qwen3:4b
Runtime size: 3.5 GB
Processor: 72% CPU / 28% GPU
Context: 4096
Runner: llamacpp
```

Therefore:

- NVIDIA driver works.
- Ollama detects the GPU.
- Ollama performs partial GPU offload.
- CPU + GPU inference is the current baseline.
- No additional GPU optimization is required for M1.

This is a baseline to benchmark later if models or hardware change.

---

# 7. Python → Ollama Integration

Python package:

```text
ollama==0.6.3
```

Working architecture:

```text
Personal AI Python code
        ↓
ollama Python client
        ↓
localhost:11434
        ↓
Ollama
        ↓
qwen3:4b
        ↓
CPU + NVIDIA GPU
        ↓
response
```

The Python client returns an Ollama `ChatResponse` Pydantic object.

Application output is accessed through:

```python
response.message.content
```

`ChatResponse` is not a dictionary, so:

```python
response.keys()
```

is not valid.

---

# 8. Package Architecture Decision

The project intentionally uses:

```text
src/
└── personal_ai/
```

with a root-level `pyproject.toml`.

The package is installed using:

```bash
pip install -e .
```

This is preferred over:

- `sys.path` manipulation
- repository-specific `PYTHONPATH` hacks
- importing through `src.personal_ai`

The package boundary should remain clean as the project grows.

---

# 9. Target Personal AI Architecture

```text
                         PERSONAL AI
                              │
                       Central Orchestrator
                              │
             ┌────────────────┼────────────────┐
             │                │                │
          Career         Engineering        Finance
             │                │                │
             └────────────────┼────────────────┘
                              │
                           Health
```

Development order:

```text
Individual agent
      ↓
Agent tools + retrieval
      ↓
Agent evaluation
      ↓
Multiple domain agents
      ↓
Central router/orchestrator
      ↓
Cross-agent workflows
```

Do not begin by building a complicated multi-agent architecture.

---

# 10. Domain Agents

## Career Agent

Knowledge:

- Master resume
- Previous resumes
- Experience
- Projects
- Skills
- Achievements
- Certifications
- Education
- Job descriptions
- Interview preparation
- Career evidence

Example workflow:

```text
Job Description
      ↓
Requirement extraction
      ↓
Career evidence retrieval
      ↓
Requirement ↔ evidence mapping
      ↓
Tailored resume / interview preparation
      ↓
Claim validation
```

Important rule:

Generated career claims must be grounded in stored career evidence.

Unsupported achievements or skills must not be invented.

---

## Engineering Agent

Knowledge:

- UAV
- Embedded systems
- Electronics
- MATLAB / Simulink
- EV powertrain systems
- Simulation
- Datasheets
- Schematics
- BOMs
- Firmware
- Git repositories
- Laboratory documentation
- Debugging records

Future tools may include:

- Read-only repository inspection
- Technical document retrieval
- Engineering calculations
- Configuration inspection
- Approved analysis tools

Actions such as modifying firmware, flashing hardware or executing potentially destructive system commands require explicit approval.

---

## Finance Agent

Data should primarily be structured.

Examples:

- Transactions
- Assets
- Investments
- Income
- Expenses
- Savings
- Financial goals

Calculations should be performed by deterministic Python functions.

The LLM should explain and interpret results rather than being trusted for financial arithmetic.

Initial system:

- Read-only/manual imports
- No autonomous trading
- No movement of money

---

## Health / Fitness Agent

Knowledge:

- Medical records
- Laboratory reports
- Prescriptions
- Appointments
- Measurements
- Fitness records
- Workout information

Constraints:

- Structured measurements where appropriate
- Dates and units
- Source/provenance
- Strong access boundaries
- No autonomous diagnosis
- No autonomous prescribing
- Primarily summarization, organization and decision support

Health data must not become general-purpose context for unrelated agents.

---

# 11. Common Infrastructure

Target architecture:

```text
                    Domain Agents
                         │
                         ↓
                Agent / Workflow Layer
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
          Retrieval     Tools     State
              │          │          │
              └──────────┼──────────┘
                         ↓
                  Core Infrastructure
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
   LLM Runtime        Database          Permissions
       │                                   │
       ↓                                   ↓
    Ollama                            Audit / Policy
       │
       ↓
   Local Models
```

Potential future components:

- LangGraph
- LangChain where useful
- Local vector database
- Hybrid retrieval
- Structured database
- Document ingestion
- Tool registry
- Permissions
- Audit logging
- Evaluation framework

Do not introduce all components simultaneously.

---

# 12. Agent Framework

Each agent should conceptually provide:

```text
Input
  ↓
Understand request
  ↓
Retrieve relevant context
  ↓
Execute deterministic tools if required
  ↓
Generate response
  ↓
Validate
  ↓
Return result + provenance
```

LangGraph will eventually manage explicit workflow state.

Conceptual state:

```python
state = {
    "user_request": ...,
    "domain": ...,
    "retrieved_context": ...,
    "tool_results": ...,
    "draft_response": ...,
    "sources": ...,
    "validation": ...,
}
```

The exact state schema will be designed during M2.

---

# 13. Retrieval Strategy

Initial retrieval should be simple and understandable.

Preferred progression:

```text
Local files
   ↓
Simple retrieval
   ↓
Metadata / provenance
   ↓
Hybrid retrieval
   ↓
Vector search when justified
```

Do not introduce a vector database simply because the system is called RAG.

First prove the workflow.

---

# 14. Tools

Tools are deterministic capabilities available to an agent.

### Career

- Search career documents
- Extract resume evidence
- Compare job description requirements
- Generate resume output

### Engineering

- Search technical documents
- Read repository files
- Perform engineering calculations
- Inspect configuration
- Run approved analysis tools

### Finance

- Import transactions
- Calculate portfolio metrics
- Calculate savings rates
- Run deterministic projections

### Health

- Search medical records
- Extract measurements
- Summarize reports
- Organize appointments

---

# 15. Permissions

Each agent should receive only the data and capabilities required for its domain.

Example:

```text
Career Agent       → Career data
Engineering Agent  → Engineering data
Finance Agent      → Finance data
Health Agent       → Health data
```

Permission boundaries are an architectural feature, not merely a prompt instruction.

---

# 16. Safety / Control Model

Default execution model:

```text
READ
 ↓
REASON
 ↓
PROPOSE
 ↓
HUMAN APPROVAL
 ↓
ACT
```

Do not initially allow autonomous sensitive/destructive actions.

Examples requiring particular caution:

- Financial transactions
- Health decisions
- System modifications
- Firmware flashing
- Deleting data
- Sending external communications

---

# 17. Evaluation

Each important agent should eventually have:

- Representative test questions
- Expected behavior
- Ground-truth sources
- Retrieval tests
- Tool tests
- Output validation
- Regression tests

Model replacement should be evaluated rather than accepted based only on subjective impressions.

---

# 18. Milestone Status

## M0 — Repository Bootstrap

**COMPLETE**

Completed:

- Git repository
- GitHub remote
- Python virtual environment
- Project structure
- `.gitignore`
- README
- Initial architecture documentation

---

## M1 — Local LLM Runtime and Python Integration

**COMPLETE**

Completed:

- Ollama installation
- Global Ollama runtime
- Qwen3 4B model
- Interactive inference
- NVIDIA driver verification
- GPU offload verification
- Python Ollama client
- `pyproject.toml`
- Editable package installation
- Python → Ollama → Qwen3 integration

Successful project-level execution:

```bash
python3 -m personal_ai.main
```

---

## M2 — LangGraph Foundation

**NEXT**

Objective:

Build the smallest useful stateful local-LLM workflow.

Initial graph:

```text
START
  ↓
generate_response
  ↓
END
```

Use the existing Ollama/Qwen3 integration.

Focus on understanding:

- Graph
- State
- Nodes
- Edges
- START / END
- Workflow execution
- Model integration

Do not build the complete multi-agent architecture during M2.

---

## M3 — Grounded Career Agent

**AFTER M2**

Objective:

Build the first genuinely useful domain agent.

Initial Career knowledge base:

```text
data/career/
├── profile.md
├── education.md
├── experience/
├── projects/
├── achievements/
├── skills/
└── resume_versions/
```

Initial workflow:

```text
User request
      ↓
Career Agent
      ↓
Retrieve relevant career evidence
      ↓
LLM reasoning / generation
      ↓
Grounded response
      ↓
Evidence / source references
```

Start with simple local Markdown/document retrieval.

Upgrade to hybrid/vector retrieval only when justified.

---

# 19. Next Development Session

Resume from:

**M2 — LangGraph Foundation**

Do NOT repeat:

- Ollama installation
- Qwen3 download
- NVIDIA driver troubleshooting
- Python environment setup
- Package-layout discussion

Those are complete.

Next session should focus on:

1. Understanding LangGraph
2. Connecting LangGraph to the existing local LLM layer
3. Designing the state object
4. Building the first graph
5. Testing the graph
6. Understanding why the graph architecture is useful
7. Preparing the transition to the Career Agent

---

# 20. Git Checkpoint

The intended M1 Git checkpoint is:

```bash
git add .
git commit -m "Complete milestone 1 local LLM integration"

git tag -a milestone-1-local-llm \
  -m "Milestone 1: local LLM runtime and Python integration"

git push origin main
git push origin milestone-1-local-llm
```

Verify:

```bash
git status
git log --oneline --decorate -5
git tag
```

Expected state:

```text
working tree clean
```

If the M1 commit/tag has already been created, do not recreate it.

---

# 21. Development Philosophy

The intended system is:

```text
Personal Data
      ↓
Structured Knowledge
      ↓
Retrieval
      ↓
Domain Agent
      ↓
LLM Reasoning
      ↓
Tools / Deterministic Computation
      ↓
Grounded Result
      ↓
Human Approval when required
```

The LLM is one component of the system, not the system itself.
