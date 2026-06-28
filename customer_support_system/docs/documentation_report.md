# Documentation Report

## Workflow Summary
The system accepts customer support queries, classifies the intent, routes the request to the appropriate department, retrieves content from knowledge documents, stores conversation history in SQLite, and promotes high-risk requests to a human supervisor for approval before sending a final response.

## Implementation Highlights
- LangGraph state machine for orchestration
- Rule-based intent detector with departmental routing
- Simple RAG retrieval over company documents
- SQLite memory for customer history recall
- Supervisor approval node for refund and cancellation requests

## Demonstration Evidence
The demo script prints the department routing, approval requirement, and final response for each of the five required queries.
