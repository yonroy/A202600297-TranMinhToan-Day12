# 🌤️ SkyCast: Professional Weather App

A stunning, production-ready weather application built with **React (Vite)** and **FastAPI**. It features a premium glassmorphic UI, API authentication, rate limiting, and cost protection guardrails.

## 🚀 Quick Start (Local)

1. **Clone and Setup Environment:**
   ```bash
   cp .env.example .env
   # Add your OpenWeather API Key to .env
   ```

2. **Run with Docker:**
   ```bash
   docker-compose up --build
   ```
   Access the app at [http://localhost:8000](http://localhost:8000).

---

## ☁️ Deployment to Railway (Step-by-Step)

### 1. Prepare your Repository
Ensure all files are committed to your GitHub repository.

### 2. Setup Railway Project
1. Go to [Railway.app](https://railway.app/) and log in.
2. Click **"+ New Project"**.
3. Select **"Deploy from GitHub repo"**.
4. Choose your `weather-app` repository.

### 3. Configure Environment Variables
In the Railway dashboard for your service, go to the **Variables** tab and add:
- `OPENWEATHER_API_KEY`: Your real key from OpenWeather.
- `API_AUTH_KEY`: A secret string (e.g., `my-production-secret`).
- `PORT`: `8000` (Railway will usually provide this automatically, but good to have).

### 4. Deploy
- Railway will detect the `Dockerfile` and start the multi-stage build automatically.
- Once finished, you'll receive a public URL (e.g., `weather-app-production.up.railway.app`).

---

## 🛠️ Tech Stack & Features

- **Frontend:** React (Vite), Vanilla CSS (Glassmorphism), Google Fonts (Montserrat & Inter).
- **Backend:** FastAPI (Python), httpx for async API calls.
- **Security:**
    - **API Gateway Guard:** Custom authentication header check.
    - **Rate Limiter:** Prevents spamming and ensures infrastructure stability.
    - **Cost Guard:** Tracks usage count to prevent exceeding free-tier limits.
- **Deployment:** Docker Multi-stage build (optimized image size).
