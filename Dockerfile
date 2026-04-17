# --- Stage 1: Build Frontend ---
FROM node:20-slim as frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Final Image ---
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./static

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
