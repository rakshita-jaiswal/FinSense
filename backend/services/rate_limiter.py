"""Rate limiter for AI API requests."""
import asyncio
from datetime import datetime, timedelta
from typing import Optional
from collections import deque


class RateLimiter:
    """
    Rate limiter to prevent exceeding API quotas.
    Uses a sliding window approach to track requests.
    """
    
    def __init__(self, max_requests: int = 5, time_window: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in time window
            time_window: Time window in seconds (default: 60 seconds)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()  # Store timestamps of requests
        self.lock = asyncio.Lock()  # Thread-safe operations
    
    async def acquire(self) -> bool:
        """
        Attempt to acquire permission to make a request.
        Blocks until permission is granted.
        
        Returns:
            True when permission is granted
        """
        async with self.lock:
            now = datetime.now()
            
            # Remove requests outside the time window
            cutoff_time = now - timedelta(seconds=self.time_window)
            while self.requests and self.requests[0] < cutoff_time:
                self.requests.popleft()
            
            # If we're at the limit, wait until we can make a request
            if len(self.requests) >= self.max_requests:
                # Calculate how long to wait
                oldest_request = self.requests[0]
                wait_until = oldest_request + timedelta(seconds=self.time_window)
                wait_seconds = (wait_until - now).total_seconds()
                
                if wait_seconds > 0:
                    print(f"[Rate Limiter] Limit reached. Waiting {wait_seconds:.1f}s...")
                    await asyncio.sleep(wait_seconds + 0.1)  # Add small buffer
                    
                    # Clean up again after waiting
                    now = datetime.now()
                    cutoff_time = now - timedelta(seconds=self.time_window)
                    while self.requests and self.requests[0] < cutoff_time:
                        self.requests.popleft()
            
            # Record this request
            self.requests.append(now)
            return True
    
    def get_current_usage(self) -> dict:
        """
        Get current rate limiter statistics.
        
        Returns:
            Dictionary with usage statistics
        """
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=self.time_window)
        
        # Count requests in current window
        active_requests = sum(1 for req_time in self.requests if req_time >= cutoff_time)
        
        return {
            "requests_in_window": active_requests,
            "max_requests": self.max_requests,
            "time_window_seconds": self.time_window,
            "available_requests": max(0, self.max_requests - active_requests)
        }
    
    async def reset(self):
        """Reset the rate limiter (clear all tracked requests)."""
        async with self.lock:
            self.requests.clear()


# Global rate limiter instance for AI requests
# Set to 5 requests per 60 seconds (conservative for 5-6 RPM limit)
ai_rate_limiter = RateLimiter(max_requests=5, time_window=60)