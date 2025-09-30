# Additional Security Enhancements

## Rate Limiting (Optional)
Add this to your app.py to limit usage:

```python
import time
from functools import wraps

# Simple rate limiting decorator
def rate_limit(calls_per_minute=10):
    def decorator(func):
        calls = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [call for call in calls if now - call < 60]
            if len(calls) >= calls_per_minute:
                return "❌ Rate limit exceeded. Please wait before trying again."
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Apply to your processor
@rate_limit(calls_per_minute=5)
def process_cover_letter(self, ...):
    # existing code
```

## Usage Monitoring
Add logging to track usage:

```python
import logging
from datetime import datetime

def log_usage(user_ip, action):
    logging.info(f"{datetime.now()}: {user_ip} - {action}")

# In your processor
def process_cover_letter(self, ...):
    log_usage("user_ip", "cover_letter_generated")
    # existing code
```

## Environment Variable Validation
Your current setup is already secure, but you could add:

```python
# In config.py
def validate_api_key():
    if not OPENAI_API_KEY or len(OPENAI_API_KEY) < 20:
        raise ValueError("Invalid API key format")
    return True

validate_api_key()
```
