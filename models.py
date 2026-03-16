# File: models.py

from pydantic import BaseModel, Field

class Policy(BaseModel):
    policy_id: str = Field(..., description="Unique identifier for the policy")
    risk_amount: float = Field(..., gt=0, description="Total risk amount of the policy")

class CessionResult(BaseModel):
    policy_id: str = Field(..., description="Unique identifier for the policy")
    original_risk_amount: float = Field(..., description="Original total risk amount of the policy")
    ceded_amount_quota_share: float = Field(..., description="Amount ceded under Quota Share treaty")
    ceded_amount_surplus: float = Field(..., description="Amount ceded under Surplus treaty")
    total_ceded_amount: float = Field(..., description="Total amount ceded to reinsurer")
    retained_amount: float = Field(..., description="Amount retained by the cedent")
    retention_cap_applied: bool = Field(..., description="Indicates if the retention cap was applied")
