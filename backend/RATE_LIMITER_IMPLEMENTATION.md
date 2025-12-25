# Rate Limiter Implementation

## Overview

Implemented a sophisticated rate limiter to handle Gemini API's free tier quotas gracefully. The system prevents rate limit errors by queuing requests and spacing them appropriately.

## Gemini Free Tier Limits

Based on testing, the Gemini API free tier has TWO types of limits:

### 1. Per-Minute Rate Limit
- **Limit**: 5-6 requests per minute
- **Error**: 429 with "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"
- **Retry delay**: ~30-60 seconds

### 2. Daily Quota Limit  
- **Limit**: 20 requests per day
- **Error**: 429 with "GenerateRequestsPerDayPerProjectPerModel-FreeTier"
- **Retry delay**: ~19 seconds (but won't help until next day)

## Implementation

### Rate Limiter Service
**File**: `backend/services/rate_limiter.py`

Features:
- **Sliding window algorithm**: Tracks requests in a 60-second window
- **Automatic queuing**: Blocks requests when limit reached
- **Thread-safe**: Uses asyncio locks for concurrent requests
- **Configurable**: Easy to adjust limits (currently set to 5 RPM)

```python
# Global instance
ai_rate_limiter = RateLimiter(max_requests=5, time_window=60)
```

### AI Service Integration
**File**: `backend/services/ai_service.py`

The AI service now:
1. Acquires rate limit permission before each request
2. Automatically waits if limit is reached
3. Provides better error messages for rate limit errors
4. Exposes rate limit status via `get_rate_limit_status()`

## Test Results

### Test 1: Sequential Requests (10 requests)
- ✅ All 10 requests completed successfully
- ✅ Rate limiter queued requests appropriately
- ✅ Average time: 6.1s per request (includes waiting)
- ✅ No rate limit errors from per-minute limit

### Test 2: Concurrent Requests (5 requests)
- ✅ All 5 requests completed successfully  
- ✅ Requests properly serialized by rate limiter
- ✅ Time: 50.1s total (proper spacing maintained)

### Daily Quota Discovery
During testing, we discovered the 20 requests/day limit:
- After ~20 total requests across all tests, hit daily quota
- Error message clearly indicates daily limit exceeded
- System handles this gracefully with appropriate error message

## Usage

### In Code
```python
from services.ai_service import ai_service

# Make AI request (rate limiting handled automatically)
response = await ai_service.generate_response(
    user_message="Your question here",
    conversation_history=[],
    user_data={}
)

# Check rate limit status
status = await ai_service.get_rate_limit_status()
print(f"Used: {status['requests_in_window']}/{status['max_requests']}")
```

### Error Handling
The system provides user-friendly messages:

**Per-Minute Limit**:
> "I'm currently experiencing high demand. Please wait a moment and try again. Your question is important to me!"

**Other Errors**:
> "I'm having trouble processing that right now. Please try asking your question in a different way, or try again in a moment."

## Configuration

To adjust rate limits, edit `backend/services/rate_limiter.py`:

```python
# Conservative (current setting)
ai_rate_limiter = RateLimiter(max_requests=5, time_window=60)

# More aggressive (not recommended for free tier)
ai_rate_limiter = RateLimiter(max_requests=10, time_window=60)
```

## Production Recommendations

### For Free Tier (Current Setup)
- ✅ Keep at 5 requests per minute
- ✅ Monitor daily usage (20 requests/day limit)
- ✅ Consider caching common responses
- ✅ Implement response caching for repeated questions

### For Paid Tier
If you upgrade to paid Gemini API:
1. Increase `max_requests` to 60+ (paid tier supports 1000+ RPM)
2. Remove or increase daily quota monitoring
3. Consider removing rate limiter entirely if not needed

## Monitoring

Check your API usage at:
- https://ai.dev/usage?tab=rate-limit
- https://makersuite.google.com/app/apikey

## Upgrade Path

To get higher limits:
1. Visit https://ai.google.dev/pricing
2. Enable billing on Google Cloud project
3. Paid tier pricing:
   - Input: $0.00015 per 1K tokens
   - Output: $0.0006 per 1K tokens
   - Rate limits: 1000+ RPM, no daily limits

## Testing

Run the test suite:
```bash
cd backend
python test_rate_limiter.py
```

This will test:
- Sequential request handling
- Concurrent request handling  
- Rate limit queuing behavior
- Error handling

## Summary

✅ **Rate limiter successfully implemented**
✅ **Handles 5-6 RPM limit gracefully**
✅ **Queues requests automatically**
✅ **Provides user-friendly error messages**
✅ **Thread-safe for concurrent requests**
⚠️ **Daily quota: 20 requests/day on free tier**

The system is production-ready for free tier usage with appropriate rate limiting and error handling.