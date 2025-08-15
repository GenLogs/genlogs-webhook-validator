# GenLogs Webhook Validator

A simple FastAPI application to validate and receive GenLogs webhook alerts with HMAC-SHA512 signature verification.

## Setup

### 1. Install Dependencies

```bash
pip install fastapi uvicorn
```

### 2. Configure Your Secret

Edit `app.py` and replace the `WEBHOOK_SECRET` with your own 32-character random string:

```python
WEBHOOK_SECRET = "YOUR_32_CHAR_RANDOM_STRING"
```

### 3. Run the FastAPI Server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

### 4. Expose Your Local Server

Install and use [ngrok](https://ngrok.com) to expose your local server to the internet. Ngrok creates a secure tunnel to your localhost, allowing external services like GenLogs Webhooks to reach your development server running on your local environment.

First, install ngrok from [https://ngrok.com](https://ngrok.com), then run:

```bash
ngrok http 8000
```

Copy the public HTTPS URL, e.g.:
```
https://abc123.ngrok.io/webhooks/genlogs-alerts
```

### 5. Register the Webhook in GenLogs

```bash
curl -L \
  --request POST \
  --url 'https://api.genlogs.io/alerts/webhook' \
  --header 'Access-Token: YOUR_ACCESS_TOKEN' \
  --header 'x-api-key: YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "webhook_url": "https://abc123.ngrok.io/webhooks/genlogs-alerts",
    "secret": "YOUR_32_CHAR_RANDOM_STRING",
    "description": "Local test endpoint"
  }'
```

**Important**: Use the same secret value in both your `app.py` and the webhook registration.

### 6. Trigger a Test Delivery

Use the Test Webhook option in GenLogs UI, or trigger an alert that produces matches.

Check that your FastAPI server logs a 200 OK response and displays the alert data.

### 7. Troubleshooting

- **401/403**: Check Access-Token and x-api-key
- **400**: Ensure the URL is HTTPS and unique
- **Signature mismatch**: Confirm secret matches exactly and is used with HMAC-SHA512

## How It Works

The application:
1. Receives POST requests at `/webhooks/genlogs-alerts`
2. Validates the HMAC-SHA512 signature from the `X-GenLogs-Signature` header
3. Parses and displays the alert data in both console logs and HTTP response
4. Returns a JSON response confirming receipt

## Security Features

- HMAC-SHA512 signature validation
- Timing-safe signature comparison
- Raw body validation to prevent tampering