import time
import redis
from fastapi import HTTPException, status
from .config import settings

# Kết nối Redis
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def check_rate_limit(user_id: str):
    """
    Sliding window rate limiter using Redis.
    """
    now = time.time()
    key = f"rate_limit:{user_id}"
    window = 60 # 1 minute
    
    # Dùng pipeline để tối ưu performance
    pipe = redis_client.pipeline()
    # Loại bỏ các request đã quá 1 phút
    pipe.zremrangebyscore(key, 0, now - window)
    # Đếm số request hiện tại
    pipe.zcard(key)
    # Thêm request mới
    pipe.zadd(key, {str(now): now})
    # Set expire để tự dọn dẹp data cũ
    pipe.expire(key, window + 10)
    
    results = pipe.execute()
    request_count = results[1]

    if request_count >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_PER_MINUTE} req/min."
        )
