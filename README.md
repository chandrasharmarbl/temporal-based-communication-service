# Temporal + FastAPI based communication service


# Install dependencies
pip install -r requirements.txt
```

### Start the Services

**Terminal 1 - Start the Temporal Worker:**
```bash
python worker.py
```

**Terminal 2 - Start the FastAPI Server:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Test the Service (Might not work as initially it was built to test)

**Terminal 3 - Run the test client:**
```bash
python test_client.py
```

Or use **curl** directly:

```bash
# Send email + SMS notification
curl -X POST "http://localhost:8000/send-notification" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "phone_number": "+1-555-0123",
    "subject": "Important Update",
    "message": "You have a new notification!"
  }'

# Or you can use the async one
curl -X POST "http://localhost:8000/send-notification-async" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "phone_number": "+1-555-0123",
    "subject": "Important Update",
    "message": "You have a new notification!"
  }'

# Check workflow status
curl "http://localhost:8000/workflow/{workflow_id}"
```

### Combined Notifications
- `POST /send-notification` - Send email + SMS (blocking/sync)
  - Body: `{ "email": "...", "phone_number": "...", "subject": "...", "message": "..." }`
  - Returns: Both email and SMS results

- `POST /send-notification-async` - Send email + SMS (non-blocking/async)
  - Body: `{ "email": "...", "phone_number": "...", "subject": "...", "message": "..." }`
  - Returns: Workflow ID immediately

## Note: can be extended through custom activities.
