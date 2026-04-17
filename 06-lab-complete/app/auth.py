from fastapi import Header, HTTPException, status
from .config import settings

async def verify_api_key(x_api_key: str = Header(None)):
    """
    Dependency to verify the API Key from headers.
    Returns the user_id (mocked as 'default_user' for now).
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Please provide X-API-Key header."
        )
    
    if x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key."
        )
    
    # Trong thực tế, bạn có thể map API Key với một User ID từ DB
    return "user_123"
