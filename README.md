# FastAPI Mutual Fund API

Simple mutual fund API built with fastapi, postgres and redis.

## Prerequisites

- Docker Engine (27.3.1+)
- Docker Compose (2.29.7+)
- Python 3.12+

## Quick Start

1. Clone the repository
   ```bash
   git clone https://github.com/snifhex/mutual-fund.git
   cd mutual-fund
   ```

2. Run locally via Docker
   ```bash
   docker compose -f docker-compose.local.yaml up --build
   ```

3. Access the Swagger UI:
   - Swagger UI: http://localhost:80/docs

## Run locally via docker 

  ```bash
  docker compose -f docker-compose.local.yaml up -d
  ```

## Quick Test

### Authentication
```bash
# Register a new user
curl -X POST "http://localhost:80/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Login to get access token
curl -X POST "http://localhost:80/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

### Mutual Funds
```bash
# Get all mutual fund families
curl -X GET "http://localhost:80/api/v1/funds/families/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get schemes for a fund family
curl -X GET "http://localhost:80/api/v1/funds/FUND_FAMILY_ID/schemes/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get specific scheme details
curl -X GET "http://localhost:80/api/v1/funds/schemes/SCHEME_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Portfolio Management
```bash
# Buy a mutual fund
curl -X POST "http://localhost:80/api/v1/portfolio/add-mutual-fund" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "scheme_id": "SCHEME_ID",
    "amount": 5000
  }'

# Get portfolio details
curl -X GET "http://localhost:80/api/v1/portfolio/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure

```bash
app/
├── api/               # API versioning and route aggregation
├── auth/              # Authentication and authorization
├── core/              # Core configurations, database setup
├── data/              # Mutual fund data in case api is not available
├── funds/             # Mutual funds related endpoints
├── lib/               # Shared utilities and components
├── portfolio/         # Portfolio management endpoints
└── main.py            # Application entry point
```

## Development

1. Install Dependencies
    ```
    uv sync
    ```
2. Run Linting
    ```
    ./scripts/lint.sh
    ```
3. Format code
    ```
    ./scripts/lint.sh
    ```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| DATABASE_URL | Database connection URL | postgresql://postgres:password@localhost:5432/mutual_funds | Yes |
| JWT_SECRET_KEY | Secret key for JWT tokens | JWT_SECRET_KEY | Yes |
| JWT_ALGORITHM | Algorithm for JWT tokens | HS256 | Yes |
| JWT_ACCESS_TOKEN_EXPIRY | Token expiry in seconds | 86400 | Yes |
| REDIS_HOST | Redis server address | localhost | Yes |
| REDIS_PORT | Redis server port | 6379 | Yes |
| REDIS_DB | Redis database number | 0 | Yes |
| RAPIDAPI_KEY | RapidAPI key for MF data | your-api-key | Yes |
| MF_RAPIDAPI_HOST | RapidAPI host for MF data | host | Yes |
| MF_RAPIDAPI_BASE_URL | RapidAPI base URL | base-url | Yes | 