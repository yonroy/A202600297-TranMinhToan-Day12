from datetime import datetime
import redis
from fastapi import HTTPException, status
from .config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def check_cost_budget(user_id: str):
    """
    Monthly cost guard using Redis.
    """
    month_key = datetime.now().strftime("%Y-%m")
    key = f"cost:{user_id}:{month_key}"
    
    current_spent = float(redis_client.get(key) or 0)
    
    if current_spent >= settings.MONTHLY_BUDGET_USD:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Monthly budget of ${settings.MONTHLY_BUDGET_USD} exceeded."
        )

def record_usage(user_id: str, cost: float):
    """Ghi nhận chi phí sau mỗi request thành công."""
    month_key = datetime.now().strftime("%Y-%m")
    key = f"cost:{user_id}:{month_key}"
    redis_client.incrbyfloat(key, cost)
    redis_client.expire(key, 32 * 24 * 3600) # 32 days
