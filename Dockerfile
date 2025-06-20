FROM python:3.12-slim

WORKDIR /app

# Cài gói CA certs để tránh lỗi SSL
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
