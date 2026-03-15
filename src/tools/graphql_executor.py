"""GraphQL executor tool for LangGraph agents."""

import json
import logging
from typing import Any, Optional

from langchain_core.tools import tool

from src.graphql_facade import data_loader

logger = logging.getLogger(__name__)


def _format_amount(value: Any) -> str:
    """Format currency amount for display."""
    if value is None:
        return "N/A"
    try:
        return f"{float(value):,.0f} VND"
    except (ValueError, TypeError):
        return str(value)


def _execute_customer_info(customer_id: str) -> dict:
    """Execute customerInfo query."""
    raw = data_loader.get_customer_by_id(customer_id)
    if not raw:
        return {"error": f"Customer {customer_id} not found"}
    return {
        "operation": "customerInfo",
        "data": raw,
    }


def _execute_finance_latest(customer_id: str) -> dict:
    """Execute financeProfileLatest query."""
    raw = data_loader.get_finance_profile_latest(customer_id)
    if not raw:
        return {"error": f"No finance data for {customer_id}"}
    return {
        "operation": "financeProfileLatest",
        "data": raw,
    }


def _execute_finance_series(customer_id: str, metric: str, months: int) -> dict:
    """Execute financeMetricSeries query."""
    from src.graphql_facade.schema import METRIC_FIELD_MAP

    profiles = data_loader.get_finance_profiles_series(customer_id, months)
    field = METRIC_FIELD_MAP.get(metric, "aum_eop_amount")

    points = []
    for p in profiles:
        dk = p.get("date_key", "")
        val = p.get(field)
        parts = dk.split("/")
        month_label = f"{parts[1]}/{parts[2]}" if len(parts) == 3 else dk
        points.append({"month": month_label, "date_key": dk, "value": val})

    # Compute trend
    trend = "UNKNOWN"
    if len(points) >= 2:
        first = points[0].get("value")
        last = points[-1].get("value")
        if first is not None and last is not None:
            diff = last - first
            threshold = abs(first) * 0.02 if first != 0 else 0
            if diff > threshold:
                trend = "UP"
            elif diff < -threshold:
                trend = "DOWN"
            else:
                trend = "FLAT"

    return {
        "operation": "financeMetricSeries",
        "data": {
            "customer_id": customer_id,
            "metric": metric,
            "months": months,
            "points": points,
            "trend_direction": trend,
        },
    }


def _execute_customer_overview(customer_id: str) -> dict:
    """Execute customerOverview query — combines info + finance."""
    info = data_loader.get_customer_by_id(customer_id)
    finance = data_loader.get_finance_profile_latest(customer_id)

    if not info:
        return {"error": f"Customer {customer_id} not found"}

    return {
        "operation": "customerOverview",
        "data": {
            "customer_info": info,
            "finance_latest": finance or {},
        },
    }


# Intent to operation mapping
INTENT_OPERATION_MAP = {
    "customer_overview": "customerOverview",
    "field_lookup": "financeProfileLatest",  # default to finance for field lookups
    "product_holdings_snapshot": "financeProfileLatest",
    "assets_liabilities_snapshot": "financeProfileLatest",
    "income_expenses_snapshot": "financeProfileLatest",
    "aum_trend": "financeMetricSeries",
    "nbo_summary": "financeProfileLatest",
}


@tool
def execute_graphql_query(
    intent: str,
    customer_id: str,
    metric: Optional[str] = None,
    months: int = 3,
    requested_fields: Optional[list[str]] = None,
) -> str:
    """Execute a GraphQL query against the banking data facade.

    Use this tool after validating a query plan to fetch actual customer data.

    Args:
        intent: The query intent (e.g., 'customer_overview', 'field_lookup',
                'product_holdings_snapshot', 'assets_liabilities_snapshot',
                'income_expenses_snapshot', 'aum_trend', 'nbo_summary').
        customer_id: The resolved customer ID (e.g., 'Cus1').
        metric: For aum_trend intent, the metric to query (e.g., 'AUM_EOP',
                'AUM_AVG_LAST_3M', 'CASA_EOP').
        months: For aum_trend intent, number of months of history (1-24).
        requested_fields: Optional list of specific fields to include.
    """
    data_loader.ensure_loaded()

    try:
        if intent == "customer_overview":
            result = _execute_customer_overview(customer_id)
        elif intent in ("field_lookup", "product_holdings_snapshot",
                        "assets_liabilities_snapshot", "income_expenses_snapshot",
                        "nbo_summary"):
            # For field lookups that need customer info too
            if intent == "field_lookup" and requested_fields:
                # Check if requested fields are in customer_info
                info_fields = {"customer_name", "tier", "rm_id", "age", "age_group",
                               "occupation", "gender", "cic_score", "risk_appetite",
                               "lavender_group", "program_code", "economic_segment"}
                if any(f in info_fields for f in requested_fields):
                    result = _execute_customer_info(customer_id)
                else:
                    result = _execute_finance_latest(customer_id)
            else:
                result = _execute_finance_latest(customer_id)

            # Also fetch customer info for context
            info = data_loader.get_customer_by_id(customer_id)
            if info and "data" in result:
                result["customer_info"] = {
                    "customer_id": info.get("customer_id"),
                    "customer_name": info.get("customer_name"),
                    "tier": info.get("tier"),
                }
        elif intent == "aum_trend":
            metric_val = metric or "AUM_EOP"
            result = _execute_finance_series(customer_id, metric_val, months)
        else:
            result = _execute_customer_overview(customer_id)

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error("GraphQL execution error: %s", e, exc_info=True)
        return json.dumps({
            "error": f"Query execution failed: {str(e)}",
        })
