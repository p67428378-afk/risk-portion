import pytest
from app.services import CessionCalculationService
from app.main import app
from fastapi.testclient import TestClient

# Initialize TestClient for FastAPI app
client = TestClient(app)

# Test cases for CessionCalculationService
@pytest.fixture
def default_cession_service():
    """Fixture for CessionCalculationService with default values."""
    return CessionCalculationService(quota_share_cession_rate=0.40, retention_cap=50000.00)

def test_quota_share_only(default_cession_service):
    """
    Test case: Policy risk amount results in only Quota Share cession,
    and retained amount is below retention cap.
    """
    policy_risk_amount = 80000.00
    expected_quota_share_ceded = 32000.00  # 40% of 80000
    expected_retained_after_qs = 48000.00  # 80000 - 32000
    expected_surplus_ceded = 0.00
    expected_total_ceded = 32000.00
    expected_final_retained = 48000.00

    result = default_cession_service.calculate_cession(policy_risk_amount)

    assert result["quota_share_ceded_amount"] == expected_quota_share_ceded
    assert result["surplus_ceded_amount"] == expected_surplus_ceded
    assert result["total_ceded_amount"] == expected_total_ceded
    assert result["final_retained_amount"] == expected_final_retained

def test_quota_share_and_surplus(default_cession_service):
    """
    Test case: Policy risk amount results in Quota Share cession,
    and retained amount exceeds retention cap, leading to Surplus cession.
    """
    policy_risk_amount = 150000.00
    expected_quota_share_ceded = 60000.00  # 40% of 150000
    expected_retained_after_qs = 90000.00  # 150000 - 60000
    expected_surplus_ceded = 40000.00  # 90000 - 50000 (cap)
    expected_total_ceded = 100000.00  # 60000 + 40000
    expected_final_retained = 50000.00  # Retention cap

    result = default_cession_service.calculate_cession(policy_risk_amount)

    assert result["quota_share_ceded_amount"] == expected_quota_share_ceded
    assert result["surplus_ceded_amount"] == expected_surplus_ceded
    assert result["total_ceded_amount"] == expected_total_ceded
    assert result["final_retained_amount"] == expected_final_retained

def test_policy_risk_amount_equals_retention_cap(default_cession_service):
    """
    Test case: Policy risk amount is such that retained amount after quota share
    exactly equals the retention cap.
    """
    # If policy_risk_amount * (1 - 0.40) = 50000 => policy_risk_amount * 0.60 = 50000
    # policy_risk_amount = 50000 / 0.60 = 83333.333...
    policy_risk_amount = 83333.33
    expected_quota_share_ceded = round(policy_risk_amount * 0.40, 2) # 33333.33
    expected_retained_after_qs = round(policy_risk_amount - expected_quota_share_ceded, 2) # 50000.00
    expected_surplus_ceded = 0.00
    expected_total_ceded = expected_quota_share_ceded
    expected_final_retained = 50000.00

    result = default_cession_service.calculate_cession(policy_risk_amount)

    assert result["quota_share_ceded_amount"] == expected_quota_share_ceded
    assert result["surplus_ceded_amount"] == expected_surplus_ceded
    assert result["total_ceded_amount"] == expected_total_ceded
    assert result["final_retained_amount"] == expected_final_retained

def test_zero_policy_risk_amount(default_cession_service):
    """
    Test case: Policy risk amount is zero.
    """
    policy_risk_amount = 0.00
    expected_quota_share_ceded = 0.00
    expected_surplus_ceded = 0.00
    expected_total_ceded = 0.00
    expected_final_retained = 0.00

    result = default_cession_service.calculate_cession(policy_risk_amount)

    assert result["quota_share_ceded_amount"] == expected_quota_share_ceded
    assert result["surplus_ceded_amount"] == expected_surplus_ceded
    assert result["total_ceded_amount"] == expected_total_ceded
    assert result["final_retained_amount"] == expected_final_retained

def test_negative_policy_risk_amount(default_cession_service):
    """
    Test case: Policy risk amount is negative (should raise ValueError).
    """
    policy_risk_amount = -1000.00
    with pytest.raises(ValueError, match="Policy risk amount cannot be negative."):
        default_cession_service.calculate_cession(policy_risk_amount)

def test_invalid_quota_share_rate():
    """
    Test case: Invalid quota share rate during service initialization.
    """
    with pytest.raises(ValueError, match="Quota share cession rate must be between 0 and 1."):
        CessionCalculationService(quota_share_cession_rate=1.5, retention_cap=50000.00)
    with pytest.raises(ValueError, match="Quota share cession rate must be between 0 and 1."):
        CessionCalculationService(quota_share_cession_rate=-0.1, retention_cap=50000.00)

def test_negative_retention_cap():
    """
    Test case: Negative retention cap during service initialization.
    """
    with pytest.raises(ValueError, match="Retention cap cannot be negative."):
        CessionCalculationService(quota_share_cession_rate=0.4, retention_cap=-100.00)

# Test cases for FastAPI endpoint
def test_calculate_cession_endpoint_success():
    """
    Test the FastAPI endpoint for a successful calculation.
    """
    response = client.post(
        "/calculate-cession",
        json={"policy_risk_amount": 100000.00}
    )
    assert response.status_code == 200
    assert response.json() == {
        "total_ceded_amount": 50000.00,
        "final_retained_amount": 50000.00,
        "quota_share_ceded_amount": 40000.00,
        "surplus_ceded_amount": 10000.00
    }

def test_calculate_cession_endpoint_with_surplus():
    """
    Test the FastAPI endpoint for a calculation involving surplus cession.
    """
    response = client.post(
        "/calculate-cession",
        json={"policy_risk_amount": 150000.00}
    )
    assert response.status_code == 200
    assert response.json() == {
        "total_ceded_amount": 100000.00,
        "final_retained_amount": 50000.00,
        "quota_share_ceded_amount": 60000.00,
        "surplus_ceded_amount": 40000.00
    }

def test_calculate_cession_endpoint_invalid_input():
    """
    Test the FastAPI endpoint with invalid input (negative policy risk amount).
    """
    response = client.post(
        "/calculate-cession",
        json={"policy_risk_amount": -500.00}
    )
    assert response.status_code == 422
    # Pydantic's default error message for gt=0 validation
    assert "Input should be greater than 0" in response.json()["detail"][0]["msg"]

def test_calculate_cession_endpoint_missing_input():
    """
    Test the FastAPI endpoint with missing input.
    """
    response = client.post(
        "/calculate-cession",
        json={}
    )
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation error

def test_health_check_endpoint():
    """
    Test the health check endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "Risk Cession Service is up and running."}
