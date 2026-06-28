from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from customer_support_system.graph import CustomerSupportGraph


def test_sales_query_routes_to_sales_and_approves() -> None:
    graph = CustomerSupportGraph(db_path="/tmp/test_memory.db")
    result = graph.run("cust1", "Asha", "What are the pricing plans available for your software?")
    assert result["department"] == "Sales"
    assert result["final_response"].startswith("Hello Asha")


def test_refund_requires_approval() -> None:
    graph = CustomerSupportGraph(db_path="/tmp/test_memory2.db")
    result = graph.run("cust2", "John", "I need a refund for my annual subscription.")
    assert result["approval_required"] is True
    assert result["approval_status"] == "Approved"
