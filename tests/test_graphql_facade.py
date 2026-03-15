import pytest
from src.graphql_facade.schema import schema
from src.graphql_facade import data_loader

@pytest.fixture(autouse=True)
def setup_data():
    data_loader.load_data()

def test_query_resolve_customer():
    query = """
    query {
      resolveCustomer(customerId: "Cus1") {
        status
        candidates {
          customerId
          customerName
        }
      }
    }
    """
    result = schema.execute_sync(query)
    assert result.errors is None
    data = result.data["resolveCustomer"]
    assert data["status"] == "RESOLVED"
    assert data["candidates"][0]["customerId"] == "Cus1"

def test_query_customer_info():
    query = """
    query {
      customerInfo(customerId: "Cus1") {
        customerId
        customerName
        age
        tier
      }
    }
    """
    result = schema.execute_sync(query)
    assert result.errors is None
    data = result.data["customerInfo"]
    assert data["customerId"] == "Cus1"
    assert data["customerName"] == "Nguyen van A"
    assert data["age"] > 0

def test_query_finance_latest():
    query = """
    query {
      financeProfileLatest(customerId: "Cus1") {
        customerId
        aumEopAmount
        casaEopAmount
      }
    }
    """
    result = schema.execute_sync(query)
    assert result.errors is None
    data = result.data["financeProfileLatest"]
    assert data["customerId"] == "Cus1"
    assert data["aumEopAmount"] > 0

def test_query_customer_overview():
    query = """
    query {
      customerOverview(customerId: "Cus1") {
        customer {
          customerName
        }
        customerInfo {
          tier
        }
        financeLatest {
          aumEopAmount
        }
      }
    }
    """
    result = schema.execute_sync(query)
    assert result.errors is None
    data = result.data["customerOverview"]
    assert data["customer"]["customerName"] == "Nguyen van A"
    assert data["customerInfo"]["tier"] == "Gold"

def test_query_finance_series():
    query = """
    query {
      financeMetricSeries(customerId: "Cus1", metric: "AUM_EOP", months: 3) {
        customerId
        metric
        points {
          month
          value
        }
        trendDirection
      }
    }
    """
    result = schema.execute_sync(query)
    assert result.errors is None
    data = result.data["financeMetricSeries"]
    assert data["customerId"] == "Cus1"
    assert len(data["points"]) > 0
    assert data["trendDirection"] in ["UP", "DOWN", "FLAT", "UNKNOWN"]
