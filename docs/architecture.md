# Personal AI Agent Framework

## Purpose

The Personal AI platform consists of specialized domain agents operating
over controlled personal knowledge and tools.

The architecture is intentionally incremental.

---

## Agent Layers

```text
┌─────────────────────────────────────────────┐
│              User Interface                 │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│           Orchestrator / Router             │
└──────────────────────┬──────────────────────┘
                       ↓
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Career       Engineering       Finance
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                     Health

Each agent contains:

    Agent
      │
      ├── State
      ├── Prompt / policy
      ├── Retrieval
      ├── Tools
      ├── Validation
      └── Output
