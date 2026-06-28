# AI-Powered Customer Support Automation System

This project implements a LangGraph-based customer support automation workflow with:
- Intent classification and department routing
- Retrieval-augmented generation from knowledge documents
- SQLite-based conversation memory
- Human-in-the-loop approval for high-risk requests
- A supervisor agent that validates and improves responses

## Project Structure
- customer_support_system/state.py: state schema for the graph
- customer_support_system/memory.py: SQLite conversation memory
- customer_support_system/rag.py: simple RAG document retrieval
- customer_support_system/graph.py: LangGraph workflow implementation
- customer_support_system/demo.py: demo runner for the five assignment queries
- customer_support_system/tests/test_graph.py: sample regression tests

## Setup
1. Install Python 3.13+
2. Install the dependency:
   ```bash
   pip install langgraph
   ```
3. Run the demo:
   ```bash
   python -m customer_support_system.demo
   ```

## Demo Queries
- Pricing plan request -> Sales
- Password issue -> Account
- Crash during upload -> Technical Support
- Refund request -> Billing + human approval
- Previous issue recall -> Memory recall

## Notes
The memory database is stored in `memory.db` in the project root.
