from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import httpx
import os
from .config import Config
from .auth import verify_auth
from .rate_limiter import check_rate_limit
from .cost_guard import check_cost_protection

app = FastAPI(title="Stunning Weather API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Frontend Static Files
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api/health")
async def root():
    return {"message": "Stunning Weather API is running", "version": "1.0.0"}

@app.get("/api/weather", dependencies=[Depends(verify_auth), Depends(check_rate_limit), Depends(check_cost_protection)])
async def get_weather(city: str = Query(..., min_length=1)):
    if not Config.OPENWEATHER_API_KEY:
        # Fallback for testing if no key is provided
        return {
            "city": city,
            "temp": 22.5,
            "description": "sunny (demo mode)",
            "humidity": 45,
            "wind_speed": 5.2,
            "icon": "01d"
        }

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Config.OPENWEATHER_API_KEY}&units=metric"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="City not found or API error")
            
            data = response.json()
            return {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "icon": data["weather"][0]["icon"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT)
