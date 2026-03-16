# File: main.py

from fastapi import FastAPI, HTTPException
from models import Policy, CessionResult
from config import QUOTA_SHARE_CESSION_RATE, RETENTION_CAP

app = FastAPI(title="Risk Cession Service",
              description="Service to calculate the risk portion ceded to a reinsurer for new policies.")

@app.post("/calculate-cession", response_model=CessionResult)
async def calculate_cession(policy: Policy):
    """
    Calculates the ceded and retained amounts for a new policy based on Quota Share and Surplus treaties.

    - Applies a default Quota Share cession rate (40%).
    - Enforces a hard Retention Cap ($50,000).
    - Cedes any amount exceeding the Retention Cap as Surplus.
    """
    if policy.risk_amount <= 0:
        raise HTTPException(status_code=400, detail="Risk amount must be positive.")

    # 1. Quota Share Treaty Calculation
    ceded_amount_quota_share = policy.risk_amount * QUOTA_SHARE_CESSION_RATE
    retained_amount_after_quota_share = policy.risk_amount - ceded_amount_quota_share

    ceded_amount_surplus = 0.0
    retention_cap_applied = False

    # 2. Retention Cap Enforcement
    if retained_amount_after_quota_share > RETENTION_CAP:
        retention_cap_applied = True
        # Amount exceeding the cap must be ceded as surplus
        amount_exceeding_cap = retained_amount_after_quota_share - RETENTION_CAP
        ceded_amount_surplus = amount_exceeding_cap
        
        # Adjust retained amount to the cap
        retained_amount = RETENTION_CAP
    else:
        retained_amount = retained_amount_after_quota_share

    total_ceded_amount = ceded_amount_quota_share + ceded_amount_surplus

    return CessionResult(
        policy_id=policy.policy_id,
        original_risk_amount=policy.risk_amount,
        ceded_amount_quota_share=ceded_amount_quota_share,
        ceded_amount_surplus=ceded_amount_surplus,
        total_ceded_amount=total_ceded_amount,
        retained_amount=retained_amount,
        retention_cap_applied=retention_cap_applied,
    )

