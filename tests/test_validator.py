import json
from src.tools.validator import validate_plan

def test_validate_plan_valid():
    plan = {
        "intent": "customer_overview",
        "customer_selector": {"mode": "customer_id", "value": "Cus1"},
        "resolved_customer_id": "Cus1",
        "requested_blocks": ["demographics", "assets"]
    }
    result_str = validate_plan.invoke({"plan_json": json.dumps(plan)})
    result = json.loads(result_str)
    assert result["status"] == "approved"

def test_validate_plan_invalid_intent():
    plan = {
        "intent": "invalid_intent",
        "customer_selector": {"mode": "customer_id", "value": "Cus1"}
    }
    result_str = validate_plan.invoke({"plan_json": json.dumps(plan)})
    result = json.loads(result_str)
    assert result["status"] == "unsupported"

def test_validate_plan_invalid_block():
    plan = {
        "intent": "customer_overview",
        "requested_blocks": ["invalid_block"],
        "resolved_customer_id": "Cus1"
    }
    result_str = validate_plan.invoke({"plan_json": json.dumps(plan)})
    result = json.loads(result_str)
    assert result["status"] == "denied"

def test_validate_plan_clarify():
    plan = {
        "intent": "customer_overview",
        "resolved_customer_id": "Cus1",
        "clarification_needed": True,
        "clarification_question": "Which customer do you mean?"
    }
    result_str = validate_plan.invoke({"plan_json": json.dumps(plan)})
    result = json.loads(result_str)
    assert result["status"] == "clarify"
    assert "Which customer" in result["reason"]
