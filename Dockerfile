# Stage 1: Builder
FROM python:3.9-slim AS builder

WORKDIR /build

# Copy requirements
COPY requirements.txt .

# Install all dependencies to a specific directory
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make Python find our installed packages
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches using Uvicorn
# The FastAPI app object is named 'app' in app.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]