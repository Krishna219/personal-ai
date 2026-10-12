# Personal AI Agent Framework

## Purpose

The Personal AI platform consists of specialized domain agents operating over controlled personal knowledge and tools.

The architecture is intentionally incremental.

---

# 1. High-Level Architecture

```text
┌─────────────────────────────────────────────┐
│                 User Interface              │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│              Orchestrator / Router          │
└──────────────────────┬──────────────────────┘
                       ↓
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Career       Engineering       Finance
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                     Health
```

The system should not begin as a complex multi-agent system.

Development sequence:

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

---

# 2. Agent Contract

Each domain agent should conceptually provide:

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

The agent should not be a monolithic prompt.

---

# 3. Agent State

LangGraph will manage explicit workflow state.

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

The exact schema should be designed during M2 rather than assumed now.

---

# 4. Domain Agents

## Career

Primary knowledge:

- Profile
- Education
- Experience
- Projects
- Achievements
- Skills
- Certifications
- Resumes
- Job descriptions
- Interview preparation
- Career evidence

Core requirement:

**Generated career claims must be grounded in stored evidence.**

Example:

```text
Job Description
      ↓
Requirement extraction
      ↓
Career evidence retrieval
      ↓
Requirement ↔ evidence mapping
      ↓
Tailored output
      ↓
Claim validation
```

---

## Engineering

Primary knowledge:

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

Potential tools:

- Technical document search
- Repository inspection
- Engineering calculations
- Configuration inspection
- Approved analysis tools

Potentially destructive actions require explicit approval.

---

## Finance

Primary data:

- Transactions
- Assets
- Investments
- Income
- Expenses
- Savings
- Financial goals

Architecture rule:

**Calculations belong to deterministic Python functions.**

The LLM explains and interprets results.

Initial capabilities should be read-only/manual-import oriented.

No autonomous trading or money movement.

---

## Health / Fitness

Primary knowledge:

- Medical records
- Laboratory reports
- Prescriptions
- Appointments
- Measurements
- Fitness records
- Workout information

Architecture constraints:

- Structured measurements where appropriate
- Dates and units
- Provenance
- Strong access boundaries
- No autonomous diagnosis
- No autonomous prescribing
- Primarily summarization, organization and decision support

Health data must not become general-purpose context for unrelated agents.

---

# 5. Retrieval

Initial retrieval progression:

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

Do not introduce a vector database before the basic grounded workflow is proven.

Retrieval should return not just text, but enough metadata to identify the source.

---

# 6. Tools

Tools are deterministic capabilities exposed to an agent.

Examples:

### Career

- Search career documents
- Extract evidence
- Compare job requirements
- Generate resume output

### Engineering

- Search technical documents
- Read repository files
- Perform calculations
- Inspect configuration
- Run approved analysis tools

### Finance

- Import transactions
- Calculate portfolio metrics
- Calculate savings rates
- Run deterministic projections

### Health

- Search records
- Extract measurements
- Summarize reports
- Organize appointments

---

# 7. Permissions

Each agent should have a defined data and tool boundary.

```text
Career Agent       → Career data
Engineering Agent  → Engineering data
Finance Agent      → Finance data
Health Agent       → Health data
```

Permissions should be enforced in application/tooling architecture.

They should not rely solely on the LLM being instructed not to access something.

---

# 8. LLM Abstraction

Agents should not directly depend on one particular LLM provider or model.

Current implementation:

```text
Agent
  ↓
LLM abstraction
  ↓
Ollama
  ↓
Qwen3 4B
```

Future model/runtime changes should occur below the agent layer.

This preserves model independence.

---

# 9. Workflow / Orchestration

## M2

Start with:

```text
START
  ↓
generate_response
  ↓
END
```

Then progressively introduce:

```text
START
  ↓
classify / understand
  ↓
retrieve
  ↓
tool
  ↓
generate
  ↓
validate
  ↓
END
```

Only after individual workflows are reliable should central routing be introduced.

---

# 10. Central Orchestrator

Eventually:

```text
User
 ↓
Orchestrator
 ↓
Domain selection
 ↓
Domain Agent
 ↓
Retrieval / Tools
 ↓
Result
```

Potentially later:

```text
User
 ↓
Orchestrator
 ↓
Multiple domain agents
 ↓
Controlled cross-agent workflow
 ↓
Validated result
```

Cross-domain access should be explicit rather than automatic.

---

# 11. Safety / Control Model

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

Sensitive or destructive operations should not initially be autonomous.

Examples:

- Financial transactions
- Health decisions
- System modifications
- Firmware flashing
- Data deletion
- External communications

---

# 12. Provenance

Important generated outputs should be traceable to their sources.

Conceptually:

```text
Source document
      ↓
Retrieved evidence
      ↓
Agent reasoning
      ↓
Generated result
      ↓
Source references
```

This is particularly important for:

- Career claims
- Engineering specifications
- Financial calculations
- Health records

---

# 13. Evaluation

Each agent should eventually have:

- Representative test questions
- Expected behavior
- Ground-truth sources
- Retrieval tests
- Tool tests
- Output validation
- Regression tests

Evaluation should allow comparison when:

- Models change
- Prompts change
- Retrieval changes
- Tools change
- Agent workflows change

---

# 14. Current Implementation Boundary

Completed at M1:

```text
Python project
      ↓
Ollama
      ↓
Qwen3 4B
      ↓
Python inference
```

Next:

```text
LangGraph
      ↓
State
      ↓
Nodes
      ↓
Edges
      ↓
Local LLM workflow
```

Then:

```text
Career knowledge
      ↓
Retrieval
      ↓
Career Agent
```

---

# 15. Guiding Principle

The Personal AI platform should be treated as an **engineering system**, not merely an LLM wrapper.

The architecture is:

```text
Data
 ↓
Knowledge
 ↓
Retrieval
 ↓
Stateful workflow
 ↓
Agent
 ↓
Tools
 ↓
Validation
 ↓
Grounded result
```

The LLM provides reasoning/generation capability inside this system.
