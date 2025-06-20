FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Cài thư viện hệ thống fix lỗi SSL
RUN apt-get update && apt-get install -y ca-certificates

# Cài thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
