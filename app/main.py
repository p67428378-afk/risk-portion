
Module: app.main
Purpose: Main FastAPI application for the Risk Cession Service.
Author: Developer Agent
Created: 2023-10-27


from fastapi import FastAPI, HTTPException, status
from app.models import PolicyInput, CessionOutput
from app.services import CessionCalculationService
from config import QUOTA_SHARE_CESSION_RATE, RETENTION_CAP

app = FastAPI(
    title="Risk Cession Service",
    description="Service to calculate the risk portion ceded to a reinsurer for every new policy issued.",
    version="1.0.0"
)

# Initialize the cession calculation service with configured values
cession_service = CessionCalculationService(
    quota_share_cession_rate=QUOTA_SHARE_CESSION_RATE,
    retention_cap=RETENTION_CAP
)


@app.post(
    "/calculate-cession",
    response_model=CessionOutput,
    summary="Calculate ceded and retained amounts for a policy",
    description="Calculates the ceded portion (Quota Share and Surplus) and the retained amount for a new policy based on its risk amount and configured treaty rules."
)
async def calculate_cession_endpoint(policy_input: PolicyInput) -> CessionOutput:
    """
    Endpoint to calculate the ceded and retained portions for a given policy risk amount.

    Args:
        policy_input (PolicyInput): The input containing the policy's risk amount.

    Returns:
        CessionOutput: The calculated cession details.

    Raises:
        HTTPException: If the policy risk amount is invalid.
    """
    try:
        result = cession_service.calculate_cession(policy_input.policy_risk_amount)
        return CessionOutput(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )


@app.get(
    "/health",
    summary="Health Check",
    description="Checks the health of the Risk Cession Service."
)
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: A status message.
    """
    return {"status": "healthy", "message": "Risk Cession Service is up and running."}
