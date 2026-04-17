from fastapi import HTTPException
from .config import Config
import datetime

class CostGuard:
    def __init__(self, daily_limit):
        self.daily_limit = daily_limit
        self.usage_count = 0
        self.last_reset = datetime.date.today()

    def check_and_track(self):
        self._reset_if_new_day()
        # Assuming each call costs a fixed 'unit' for simplicity or a real $ amount
        if self.usage_count >= self.daily_limit:
            raise HTTPException(status_code=402, detail="Daily cost limit exceeded. Service paused until tomorrow.")
        
        self.usage_count += 1

    def _reset_if_new_day(self):
        today = datetime.date.today()
        if today > self.last_reset:
            self.usage_count = 0
            self.last_reset = today

# Example limit: 50 requests per day (free tier safe)
cost_guard_instance = CostGuard(50)

async def check_cost_protection():
    cost_guard_instance.check_and_track()
