from __future__ import annotations

from pathlib import Path
import os

from .graph import CustomerSupportGraph


def main() -> None:
    db_path = Path(__file__).resolve().parent.parent / "memory.db"
    graph = CustomerSupportGraph(db_path=str(db_path))
    queries = [
        ("david", "David", "What are the pricing plans available for your software?"),
        ("david", "David", "I forgot my account password."),
        ("david", "David", "My application crashes whenever I upload a file."),
        ("david", "David", "I need a refund for my annual subscription."),
        ("david", "David", "What was my previous support issue?"),
    ]

    for idx, (customer_id, customer_name, query) in enumerate(queries, start=1):
        print(f"\n=== Query {idx} ===")
        result = graph.run(customer_id, customer_name, query)
        print("Intent:", result.get("intent"))
        print("Department:", result.get("department"))
        print("Approval required:", result.get("approval_required"))
        print("Final response:", result.get("final_response"))


if __name__ == "__main__":
    main()
