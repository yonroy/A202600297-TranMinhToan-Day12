from fastapi import Header, HTTPException
from .config import Config

async def verify_auth(x_api_key: str = Header(...)):
    if x_api_key != Config.API_AUTH_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key
