from __future__ import annotations

import os
from typing import Any, Dict, List, Literal

from langgraph.graph import StateGraph, END

from .memory import CustomerMemory
from .rag import SimpleRAG
from .state import SupportState


HIGH_RISK_ACTIONS = {
    "refund",
    "subscription cancellation",
    "account closure",
    "compensation",
    "escalation to management",
}


class CustomerSupportGraph:
    def __init__(self, db_path: str = "memory.db") -> None:
        self.memory = CustomerMemory(db_path=db_path)
        self.rag = SimpleRAG()

    def classify_intent(self, state: SupportState) -> SupportState:
        query = state["query"].lower()
        if any(term in query for term in ["price", "pricing", "plan", "plan"]):
            state["intent"] = "Sales"
            state["department"] = "Sales"
        elif any(term in query for term in ["crash", "error", "login", "install", "upload", "config"]):
            state["intent"] = "Technical"
            state["department"] = "Technical Support"
        elif any(term in query for term in ["refund", "invoice", "billing", "payment"]):
            state["intent"] = "Billing"
            state["department"] = "Billing"
        elif any(term in query for term in ["password", "account", "profile", "close", "activate", "deactivate"]):
            state["intent"] = "Account"
            state["department"] = "Account"
        else:
            state["intent"] = "General"
            state["department"] = "General"

        if state.get("customer_name"):
            state["history"] = self.memory.get_history(state["customer_id"])
        return state

    def route_query(self, state: SupportState) -> SupportState:
        if state.get("query", "").lower().startswith("what was my previous"):
            state["memory_recall"] = self.memory.get_last_issue(state["customer_id"])
            state["department"] = "Memory"
            return state

        state["retrieved_context"] = self.rag.retrieve(state["query"])
        state["approval_required"] = any(term in state["query"].lower() for term in HIGH_RISK_ACTIONS)
        state["approval_status"] = "Pending" if state["approval_required"] else "Not Required"
        state["approved"] = False if state["approval_required"] else True
        return state

    def sales_agent(self, state: SupportState) -> SupportState:
        state["draft_response"] = (
            f"Hello {state.get('customer_name', 'there')}, here is the sales guidance for your request: "
            f"We offer Basic at $29/month, Professional at $79/month, and Enterprise at $199/month."
        )
        return state

    def technical_agent(self, state: SupportState) -> SupportState:
        state["draft_response"] = (
            f"Hello {state.get('customer_name', 'there')}, the technical guidance is to clear cache and confirm the file format before retrying."
        )
        return state

    def billing_agent(self, state: SupportState) -> SupportState:
        state["draft_response"] = (
            f"Hello {state.get('customer_name', 'there')}, I have noted your billing request. Refunds and cancellations require human approval."
        )
        return state

    def account_agent(self, state: SupportState) -> SupportState:
        state["draft_response"] = (
            f"Hello {state.get('customer_name', 'there')}, the password reset option can be used through the forgot password link."
        )
        return state

    def memory_agent(self, state: SupportState) -> SupportState:
        state["draft_response"] = (
            f"Hello {state.get('customer_name', 'there')}, your previous support issue was: {state.get('memory_recall') or 'no previous issue recorded'}."
        )
        return state

    def supervisor_agent(self, state: SupportState) -> SupportState:
        if state.get("approval_required"):
            state["supervisor_feedback"] = "Approved by supervisor."
            state["approved"] = True
            state["approval_status"] = "Approved"
        else:
            state["supervisor_feedback"] = "No supervisor review needed."
            state["approved"] = True
            state["approval_status"] = "Approved"
        return state

    def final_response_agent(self, state: SupportState) -> SupportState:
        if state.get("approved"):
            state["final_response"] = state.get("draft_response", "") + " " + (state.get("supervisor_feedback") or "")
        else:
            state["final_response"] = "Your request requires a human supervisor review before a response can be sent."
        return state

    def build_graph(self) -> StateGraph:
        builder = StateGraph(SupportState)
        builder.add_node("classify_intent", self.classify_intent)
        builder.add_node("route_query", self.route_query)
        builder.add_node("sales_agent", self.sales_agent)
        builder.add_node("technical_agent", self.technical_agent)
        builder.add_node("billing_agent", self.billing_agent)
        builder.add_node("account_agent", self.account_agent)
        builder.add_node("memory_agent", self.memory_agent)
        builder.add_node("supervisor_agent", self.supervisor_agent)
        builder.add_node("final_response_agent", self.final_response_agent)

        builder.set_entry_point("classify_intent")
        builder.add_edge("classify_intent", "route_query")

        def route_to_agent(state: SupportState) -> Literal["sales_agent", "technical_agent", "billing_agent", "account_agent", "memory_agent", "final_response_agent"]:
            department = state.get("department", "")
            if department == "Memory":
                return "memory_agent"
            if department == "Sales":
                return "sales_agent"
            if department == "Technical Support":
                return "technical_agent"
            if department == "Billing":
                return "billing_agent"
            if department == "Account":
                return "account_agent"
            return "final_response_agent"

        builder.add_conditional_edges("route_query", route_to_agent)
        builder.add_edge("sales_agent", "supervisor_agent")
        builder.add_edge("technical_agent", "supervisor_agent")
        builder.add_edge("billing_agent", "supervisor_agent")
        builder.add_edge("account_agent", "supervisor_agent")
        builder.add_edge("memory_agent", "supervisor_agent")
        builder.add_edge("supervisor_agent", "final_response_agent")
        builder.add_edge("final_response_agent", END)
        return builder.compile()

    def run(self, customer_id: str, customer_name: str, query: str) -> Dict[str, Any]:
        self.memory.store_message(customer_id, "customer", query)
        app = self.build_graph()
        result = app.invoke({
            "customer_id": customer_id,
            "customer_name": customer_name,
            "query": query,
            "history": [],
        })
        self.memory.store_message(customer_id, "assistant", result.get("final_response", ""))
        return result
