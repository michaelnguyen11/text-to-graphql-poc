"""Plan validation tool for LangGraph agents."""

import json
import logging
from typing import Any

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

SUPPORTED_INTENTS = {
    "customer_overview",
    "field_lookup",
    "product_holdings_snapshot",
    "assets_liabilities_snapshot",
    "income_expenses_snapshot",
    "aum_trend",
    "nbo_summary",
}

SUPPORTED_BLOCKS = {
    "demographics",
    "product_holdings",
    "assets",
    "liabilities",
    "average_aum",
    "income_expenses",
    "next_best_offers",
}


@tool
def validate_plan(plan_json: str) -> str:
    """Validate a query plan before executing it.

    Checks that the intent is supported, blocks are valid,
    and time scope is within bounds.

    Args:
        plan_json: JSON string of the query plan to validate.
    """
    try:
        plan = json.loads(plan_json)
    except json.JSONDecodeError as e:
        return json.dumps({
            "status": "denied",
            "reason": f"Invalid JSON: {e}",
        })

    # If the LLM returned a list of plans (multi-part query), handle it
    if isinstance(plan, list):
        logger.warning("Planner returned a list of plans. Processing the first one.")
        if not plan:
            return json.dumps({
                "status": "denied",
                "reason": "Plan list is empty",
            })
        plan = plan[0]

    # Ensure plan is a dictionary
    if not isinstance(plan, dict):
        return json.dumps({
            "status": "denied",
            "reason": f"Expected JSON object, got {type(plan).__name__}",
        })

    # Validate intent
    intent = plan.get("intent", "")
    if intent not in SUPPORTED_INTENTS:
        return json.dumps({
            "status": "unsupported",
            "reason": f"Intent '{intent}' is not supported. Supported: {sorted(SUPPORTED_INTENTS)}",
        })

    # Validate blocks
    blocks = plan.get("requested_blocks", [])
    invalid_blocks = [b for b in blocks if b not in SUPPORTED_BLOCKS]
    if invalid_blocks:
        return json.dumps({
            "status": "denied",
            "reason": f"Invalid blocks: {invalid_blocks}. Supported: {sorted(SUPPORTED_BLOCKS)}",
        })

    # Validate time scope
    time_scope = plan.get("time_scope", {})
    time_mode = time_scope.get("mode", "latest")
    if time_mode == "month_range":
        months = time_scope.get("months", 3)
        if not (1 <= months <= 24):
            return json.dumps({
                "status": "denied",
                "reason": f"Months must be between 1 and 24, got {months}",
            })

    # Validate customer selector
    selector = plan.get("customer_selector", {})
    if not selector.get("mode") and not plan.get("resolved_customer_id"):
        return json.dumps({
            "status": "clarify",
            "reason": "No customer identified. Please specify a customer ID or name.",
        })

    # Check clarification flag
    if plan.get("clarification_needed"):
        return json.dumps({
            "status": "clarify",
            "reason": plan.get("clarification_question", "Clarification is needed."),
        })

    return json.dumps({
        "status": "approved",
        "intent": intent,
        "blocks": blocks or ["all"],
    })
