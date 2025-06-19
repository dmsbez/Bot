import tweepy
import requests
import time

# ==== Cấu hình cố định ====
TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAA5n2gEAAAAA26eHEzWzzxcv%2FPF6qWgLhkX7tIY%3DMcYpMvmrA2wGHiDmZiw4N6dQfmcSCsfXZ5Co5xOwkZUUFw4BeE'

# ==== Username → ID thủ công (khỏi cần gọi API) ====
USER_MAP = {
    "JnP6900erc": "1644057593241622529",
    "elonmusk": "44196397",
    "cz_binance": "1150512580",
    "VitalikButerin": "295218901"
}

# ==== Gửi tin nhắn Telegram ====
def send_telegram(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print(f'⚠️ Telegram Error: {r.text}')
    except Exception as e:
        print(f'⚠️ Lỗi gửi Telegram: {e}')

# ==== Stream class ====
class RetweetStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            if tweet.referenced_tweets:
                for ref in tweet.referenced_tweets:
                    if ref['type'] == 'retweeted':
                        uid = tweet.author_id
                        username = id_to_username.get(uid, f"user_{uid}")
                        text = tweet.text
                        url = f"https://x.com/{username}/status/{tweet.id}"
                        msg = f"🔁 Retweet từ @{username}:\n\n{text}\n\n{url}"
                        print(f"[📡] {msg}")
                        send_telegram(msg)
                        break
        except Exception as e:
            print(f'⚠️ Lỗi xử lý tweet: {e}')

    def on_connection_error(self):
        print('⚠️ Mất kết nối tới stream. Disconnect...')
        self.disconnect()

# ==== Chạy stream chính ====
def run_stream():
    stream = RetweetStream(BEARER_TOKEN)

    # Xoá rule cũ (nếu có)
    try:
        rules = stream.get_rules()
        if rules.data:
            stream.delete_rules([r.id for r in rules.data])
    except:
        pass

    # Thêm rule mới
    for uid in USER_MAP.values():
        try:
            stream.add_rules(tweepy.StreamRule(f"from:{uid}"))
        except Exception as e:
            print(f'⚠️ Lỗi thêm rule {uid}: {e}')

    print(f"🚀 Bắt đầu stream theo dõi: {', '.join(USER_MAP.keys())}")
    stream.filter(tweet_fields=["referenced_tweets", "author_id", "text"])

# ==== Main chạy vĩnh viễn ====
def main():
    global id_to_username
    id_to_username = {v: k for k, v in USER_MAP.items()}
    
    while True:
        try:
            run_stream()
        except Exception as e:
            print(f'💥 Lỗi stream: {e} → Restart sau 15s')
            time.sleep(15)

if __name__ == '__main__':
    main()
