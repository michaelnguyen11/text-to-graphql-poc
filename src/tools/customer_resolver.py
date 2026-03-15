"""Customer resolver tool for LangGraph agents."""

import json
import logging
from typing import Optional

from langchain_core.tools import tool
from unidecode import unidecode

from src.graphql_facade import data_loader

logger = logging.getLogger(__name__)


@tool
def resolve_customer(
    customer_id: Optional[str] = None,
    customer_name: Optional[str] = None,
) -> str:
    """Resolve a customer by ID or name.

    Use this tool when you need to identify which customer the user is asking about.
    Provide either customer_id (e.g., 'Cus1') or customer_name (e.g., 'Nguyen van A').
    Returns JSON with status, customer_id, customer_name, and confidence.

    Args:
        customer_id: The customer ID (e.g., 'Cus1', 'Cus2').
        customer_name: The customer name to search for.
    """
    data_loader.ensure_loaded()

    # Try by ID first
    if customer_id:
        raw = data_loader.get_customer_by_id(customer_id)
        if raw:
            return json.dumps({
                "status": "resolved",
                "customer_id": raw["customer_id"],
                "customer_name": raw.get("customer_name", ""),
                "confidence": 1.0,
                "source": "exact_id",
            }, ensure_ascii=False)

    # Try by name
    if customer_name:
        # Exact match
        matches = data_loader.get_customer_by_name(customer_name)
        if len(matches) == 1:
            raw = matches[0]
            exact = raw.get("customer_name", "").lower().strip() == customer_name.lower().strip()
            return json.dumps({
                "status": "resolved",
                "customer_id": raw["customer_id"],
                "customer_name": raw.get("customer_name", ""),
                "confidence": 1.0 if exact else 0.85,
                "source": "exact_name" if exact else "partial_name",
            }, ensure_ascii=False)
        elif len(matches) > 1:
            return json.dumps({
                "status": "ambiguous",
                "candidates": [
                    {
                        "customer_id": m["customer_id"],
                        "customer_name": m.get("customer_name", ""),
                    }
                    for m in matches
                ],
            }, ensure_ascii=False)

        # Strip honorifics
        qn = customer_name.lower().strip()
        honorifics = ["anh ", "chi ", "em ", "bac ", "ong ", "ba ", "khach hang ", "kh ", "khach "]
        for h in honorifics:
            if qn.startswith(h):
                qn = qn[len(h):].strip()
        
        normalized_query = unidecode(qn)
        all_customers = data_loader.get_all_customers()
        fuzzy_matches = []
        for c in all_customers:
            cname = c.get("customer_name", "")
            if normalized_query in unidecode(cname.lower()):
                fuzzy_matches.append(c)

        if len(fuzzy_matches) == 1:
            raw = fuzzy_matches[0]
            return json.dumps({
                "status": "resolved",
                "customer_id": raw["customer_id"],
                "customer_name": raw.get("customer_name", ""),
                "confidence": 0.75,
                "source": "fuzzy_name",
            }, ensure_ascii=False)
        elif len(fuzzy_matches) > 1:
            return json.dumps({
                "status": "ambiguous",
                "candidates": [
                    {
                        "customer_id": m["customer_id"],
                        "customer_name": m.get("customer_name", ""),
                    }
                    for m in fuzzy_matches
                ],
            }, ensure_ascii=False)

    return json.dumps({
        "status": "not_found",
        "message": "No customer found matching the provided criteria.",
    }, ensure_ascii=False)
