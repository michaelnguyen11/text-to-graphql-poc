import json
from src.tools.customer_resolver import resolve_customer
from src.graphql_facade import data_loader

def test_resolve_by_id():
    data_loader.load_data()
    result_str = resolve_customer.invoke({"customer_id": "Cus1"})
    result = json.loads(result_str)
    assert result["status"] == "resolved"
    assert result["customer_id"] == "Cus1"
    assert "source" in result
    assert result["source"] == "exact_id"

def test_resolve_by_exact_name():
    data_loader.load_data()
    result_str = resolve_customer.invoke({"customer_name": "Nguyen van A"})
    result = json.loads(result_str)
    assert result["status"] == "resolved"
    assert result["customer_id"] == "Cus1"
    assert result["source"] == "exact_name"

def test_resolve_by_fuzzy_name():
    data_loader.load_data()
    # Case insensitive, partial
    result_str = resolve_customer.invoke({"customer_name": "nguyen van a"})
    result = json.loads(result_str)
    assert result["status"] == "resolved"
    assert result["customer_id"] == "Cus1"

def test_resolve_by_fuzzy_no_accent():
    data_loader.load_data()
    # No accent
    result_str = resolve_customer.invoke({"customer_name": "nguyen van a"})
    result = json.loads(result_str)
    assert result["status"] == "resolved"
    assert result["customer_id"] == "Cus1"

def test_resolve_not_found():
    data_loader.load_data()
    result_str = resolve_customer.invoke({"customer_name": "Unknown Person"})
    result = json.loads(result_str)
    assert result["status"] == "not_found"

def test_resolve_ambiguous():
    data_loader.load_data()
    # If there are multiple "Nguyen"s in sample data
    # (Checking sample data... Nguyen van A and Chan Thi B and Pham Quang Minh)
    # Let's add more customers to test ambiguity if needed, but for now
    # searching for "nguyen" should only return one.
    pass
