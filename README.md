# AI-Powered Customer Support Automation System

This project implements a LangGraph-based customer support automation system for ABC Technologies. It accepts customer queries, classifies the issue type, routes the request to the correct department, retrieves relevant knowledge from company documents, stores customer history in SQLite, and sends risky requests such as refunds or cancellations to a human supervisor for approval before a final response is sent.

## What the system does

The workflow includes the following steps:
1. Accept a customer query.
2. Classify the intent as Sales, Technical, Billing, Account, or Memory recall.
3. Route the request to the correct support department or memory module.
4. Retrieve relevant information from company documents using a simple RAG pipeline.
5. Generate a draft answer.
6. If the request is high risk, route it to a supervisor for approval.
7. Deliver the final customer response.

## Project structure

- customer_support_system/state.py: defines the state structure used by the LangGraph workflow.
- customer_support_system/graph.py: builds and runs the LangGraph workflow.
- customer_support_system/memory.py: stores and retrieves customer conversations in SQLite.
- customer_support_system/rag.py: retrieves context from company knowledge documents.
- customer_support_system/demo.py: executes the five assignment demo queries.
- customer_support_system/tests/test_graph.py: verifies routing and approval logic.
- customer_support_system/docs/: contains company policy, pricing, technical, and FAQ documents.

## Requirements

- Python 3.13+
- LangGraph
- pytest (optional, for running tests)

## Setup

1. Open the project folder in a terminal.
2. Create and activate a virtual environment (recommended).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install the required dependency.

```powershell
pip install langgraph pytest
```

## Run the demo

Run the main demo script from the project root:

```powershell
python -m customer_support_system.demo
```

This will execute the five sample queries:
- Pricing plan request → Sales
- Password issue → Account
- File upload crash → Technical Support
- Refund request → Billing with human approval
- Previous issue recall → Memory recall

## Run tests

```powershell
pytest -q
```

## Output example

The demo prints the intent, department, approval status, and final response for each query. For example:

```text
=== Query 1 ===
Intent: Sales
Department: Sales
Approval required: False
Final response: Hello David, here is the sales guidance for your request...
```

## Notes

- The SQLite database is stored in memory.db in the project root.
- The workflow diagram and screenshots PDF are available in the submission_artifacts folder.
- The project is also pushed to GitHub at https://github.com/BodanampatiMohith/IBM-Agentic-AI-2
