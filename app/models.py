"""
Module: app.models
Purpose: Defines Pydantic models for request and response data structures.
Author: Developer Agent
Created: 2023-10-27
"""

from pydantic import BaseModel, Field


class PolicyInput(BaseModel):
    """
    Represents the input for a policy cession calculation.
    """
    policy_risk_amount: float = Field(..., gt=0, description="The total risk amount of the policy.")


class CessionOutput(BaseModel):
    """
    Represents the output of a policy cession calculation.
    """
    total_ceded_amount: float = Field(..., description="The total amount ceded to reinsurers.")
    final_retained_amount: float = Field(..., description="The final amount retained by the cedent.")
    quota_share_ceded_amount: float = Field(..., description="The amount ceded under Quota Share treaty.")
    surplus_ceded_amount: float = Field(..., description="The amount ceded under Surplus treaty.")
