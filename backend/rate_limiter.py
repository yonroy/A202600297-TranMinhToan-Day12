import time
from collections import deque
from fastapi import HTTPException
from .config import Config

class RateLimiter:
    def __init__(self, limit, period):
        self.limit = limit
        self.period = period
        self.requests = deque()

    def is_allowed(self):
        now = time.time()
        while self.requests and self.requests[0] < now - self.period:
            self.requests.popleft()
        
        if len(self.requests) < self.limit:
            self.requests.append(now)
            return True
        return False

# Global instance
limiter = RateLimiter(Config.RATE_LIMIT_CALLS, Config.RATE_LIMIT_PERIOD)

async def check_rate_limit():
    if not limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
