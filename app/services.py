"""
Module: app.services
Purpose: Implements the core business logic for risk cession calculations.
Author: Developer Agent
Created: 2023-10-27
"""

from config import QUOTA_SHARE_CESSION_RATE, RETENTION_CAP


class CessionCalculationService:
    """
    Service responsible for calculating ceded and retained amounts based on
    Quota Share and Surplus treaties, respecting a retention cap.
    """

    def __init__(self,
                 quota_share_cession_rate: float = QUOTA_SHARE_CESSION_RATE,
                 retention_cap: float = RETENTION_CAP):
        """
        Initializes the CessionCalculationService with configurable parameters.

        Args:
            quota_share_cession_rate (float): The rate for Quota Share cession (e.g., 0.40 for 40%).
            retention_cap (float): The maximum amount the cedent retains per policy.
        """
        if not (0 <= quota_share_cession_rate <= 1):
            raise ValueError("Quota share cession rate must be between 0 and 1.")
        if retention_cap < 0:
            raise ValueError("Retention cap cannot be negative.")

        self.quota_share_cession_rate = quota_share_cession_rate
        self.retention_cap = retention_cap

    def calculate_cession(self, policy_risk_amount: float) -> dict:
        """
        Calculates the ceded and retained portions for a given policy risk amount.

        Args:
            policy_risk_amount (float): The total risk amount of the policy.

        Returns:
            dict: A dictionary containing the calculated cession details:
                  - total_ceded_amount (float)
                  - final_retained_amount (float)
                  - quota_share_ceded_amount (float)
                  - surplus_ceded_amount (float)
        """
        if policy_risk_amount < 0:
            raise ValueError("Policy risk amount cannot be negative.")

        # 1. Calculate Quota Share Cession
        quota_share_ceded_amount = policy_risk_amount * self.quota_share_cession_rate
        retained_amount_after_quota_share = policy_risk_amount - quota_share_ceded_amount

        # 2. Enforce Retention Cap and calculate Surplus Cession
        surplus_ceded_amount = 0.0
        if retained_amount_after_quota_share > self.retention_cap:
            surplus_ceded_amount = retained_amount_after_quota_share - self.retention_cap
            final_retained_amount = self.retention_cap
        else:
            final_retained_amount = retained_amount_after_quota_share

        total_ceded_amount = quota_share_ceded_amount + surplus_ceded_amount

        return {
            "total_ceded_amount": round(total_ceded_amount, 2),
            "final_retained_amount": round(final_retained_amount, 2),
            "quota_share_ceded_amount": round(quota_share_ceded_amount, 2),
            "surplus_ceded_amount": round(surplus_ceded_amount, 2),
        }
