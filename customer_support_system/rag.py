from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any


class SimpleRAG:
    def __init__(self, docs_dir: str | Path = "customer_support_system/docs") -> None:
        self.docs_dir = Path(docs_dir)
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self._seed_documents()

    def _seed_documents(self) -> None:
        self.docs_dir.joinpath("company_policy.txt").write_text(
            "Company policy: Refunds require supervisor approval. Subscription cancellations require review."
        )
        self.docs_dir.joinpath("pricing_guide.txt").write_text(
            "Pricing plans: Basic $29/month, Professional $79/month, Enterprise $199/month."
        )
        self.docs_dir.joinpath("technical_manual.txt").write_text(
            "Technical manual: Application crashes during file upload can be caused by corrupted cache or unsupported formats."
        )
        self.docs_dir.joinpath("faq.txt").write_text(
            "FAQ: Password reset can be completed by using the forgot password link."
        )

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        query_lower = query.lower()
        results: List[Dict[str, Any]] = []
        for path in sorted(self.docs_dir.glob("*.txt")):
            content = path.read_text(encoding="utf-8")
            if any(keyword in query_lower for keyword in ["refund", "cancellation", "policy", "pricing", "plan", "password", "crash", "upload", "login", "billing", "account"]):
                if any(keyword in content.lower() for keyword in ["refund", "price", "plan", "password", "crash", "upload", "billing", "account", "policy"]):
                    results.append({"source": path.name, "content": content})
        if not results:
            return [{"source": "faq.txt", "content": "No specific document matched the request."}]
        return results
