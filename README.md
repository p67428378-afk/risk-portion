# Risk Cession Service

This service calculates the risk portion ceded to a reinsurer for every new policy issued, ensuring financial liability exposure is automatically managed according to predefined treaty rules. It supports Quota Share and Surplus reinsurance treaties, enforcing a configurable retention cap.

## Features

*   Calculates ceded and retained amounts for policies.
*   Supports Quota Share treaties with a configurable cession rate.
*   Enforces a configurable Retention Cap.
*   Automatically cedes amounts exceeding the Retention Cap as Surplus.
*   Provides a REST API for cession calculations.

## Technologies Used

*   Python 3.9+
*   FastAPI
*   Uvicorn
*   Pydantic

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p67428378-afk/risk-portion.git
    cd risk-portion
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The service uses environment variables or `config.py` for configuration.

*   `QUOTA_SHARE_CESSION_RATE`: Default cession rate for Quota Share treaties (e.g., `0.40` for 40%).
*   `RETENTION_CAP`: Hard retention cap per policy (e.g., `50000.00`).

You can modify `config.py` directly or set environment variables.

## Running the Service

To run the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The service will be available at `http://0.0.0.0:8000`.
The API documentation (Swagger UI) will be available at `http://0.0.0.0:8000/docs`.

## API Endpoints

### `POST /calculate-cession`

Calculates the ceded and retained portions for a given policy risk amount.

**Request Body:**

```json
{
  "policy_risk_amount": 100000.00
}
```

**Response Body (Example):**

```json
{
  "total_ceded_amount": 60000.00,
  "final_retained_amount": 40000.00,
  "quota_share_ceded_amount": 40000.00,
  "surplus_ceded_amount": 20000.00
}
```

## Project Structure

```
.
├── README.md
├── requirements.txt
├── config.py
├── .gitignore
├── Dockerfile
└── app/
    ├── __init__.py
    ├── main.py
    ├── models.py
    └── services.py
```
