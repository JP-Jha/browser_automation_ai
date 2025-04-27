# Base image
FROM python:3.10-slim
# Set working directory
WORKDIR /app
# Install system dependencies needed for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libnss3 \
    libatk-bridge2.0-0 \
    libxss1 \
    libasound2 \
    libxcomposite1 \
    libxrandr2 \
    libgtk-3-0 \
    libgbm-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Install Playwright browsers
RUN playwright install chromium
# Copy all project files
COPY . .
# Expose FastAPI port
EXPOSE 8000
# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
