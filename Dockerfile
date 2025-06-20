FROM python:3.10-slim

WORKDIR /app

# Cài certs và fix SSL verification
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        openssl && \
    update-ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
