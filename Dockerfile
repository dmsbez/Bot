FROM python:3.10-slim

WORKDIR /app

# Fix lỗi SSL bằng cách cài ca-certificates và cập nhật
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Cập nhật pip và cài gói cần thiết
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
