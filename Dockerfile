FROM python:3.10-slim

WORKDIR /app

# Cài certificate + curl để xác minh HTTPS
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy code
COPY . .

# Cài thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
