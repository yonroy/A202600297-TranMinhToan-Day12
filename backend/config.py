import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    API_AUTH_KEY = os.getenv("API_AUTH_KEY", "super-secret-key")
    RATE_LIMIT_CALLS = int(os.getenv("RATE_LIMIT_CALLS", "10"))
    RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))  # seconds
    MAX_DAILY_COST = float(os.getenv("MAX_DAILY_COST", "1.00"))  # USD equivalent or just a count
    PORT = int(os.getenv("PORT", "8000"))
