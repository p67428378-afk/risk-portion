import os

# Default Quota Share cession rate (e.g., 0.40 for 40%)
QUOTA_SHARE_CESSION_RATE: float = float(os.getenv("QUOTA_SHARE_CESSION_RATE", "0.40"))

# Hard Retention Cap per policy
RETENTION_CAP: float = float(os.getenv("RETENTION_CAP", "50000.00"))
