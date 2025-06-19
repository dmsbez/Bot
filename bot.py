import tweepy
import requests
import json
import time
import os

# ==== Cấu hình (tốt nhất mày cho vô biến môi trường Railway) ====
TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAA5n2gEAAAAA26eHEzWzzxcv%2FPF6qWgLhkX7tIY%3DMcYpMvmrA2wGHiDmZiw4N6dQfmcSCsfXZ5Co5xOwkZUUFw4BeE'

TWITTER_USERNAMES = ['JnP6900erc', 'elonmusk', 'cz_binance', 'VitalikButerin']

USER_IDS_CACHE = 'user_ids.json'


# --- Lấy user_id từ Twitter API, có cache file tránh gọi quá nhiều ---
def load_user_ids():
    if os.path.exists(USER_IDS_CACHE):
        with open(USER_IDS_CACHE, 'r') as f:
            return json.load(f)
    return {}

def save_user_ids(user_ids):
    with open(USER_IDS_CACHE, 'w') as f:
        json.dump(user_ids, f)

def get_user_id(username):
    url = f'https://api.twitter.com/2/users/by/username/{username}'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    while True:
        r = requests.get(url, headers=headers)
        if r.status_code == 429:
            print(f'⚠️ Rate limit lấy user_id {username}, đợi 60s...')
            time.sleep(60)
            continue
        r.raise_for_status()
        return r.json()['data']['id']

# --- Gửi tin nhắn Telegram ---
def send_telegram(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        print(f'⚠️ Lỗi Telegram: {r.text}')

# --- StreamingClient xử lý retweet ---
class RetweetStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        # Kiểm tra tweet có phải retweet không
        if tweet.referenced_tweets:
            for ref in tweet.referenced_tweets:
                if ref.type == 'retweeted':
                    author_id = tweet.author_id
                    text = tweet.text
                    url = f"https://x.com/{author_id}/status/{tweet.id}"
                    msg = f"🔁 Retweet từ user_id {author_id}:\n\n{text}\n\n{url}"
                    print(msg)
                    send_telegram(msg)
                    break

    def on_errors(self, errors):
        print(f'⚠️ Stream error: {errors}')

    def on_connection_error(self):
        print('⚠️ Stream connection error, reconnecting...')
        self.disconnect()

def main():
    # Load hoặc lấy mới user_ids
    user_ids = load_user_ids()
    updated = False
    for username in TWITTER_USERNAMES:
        if username not in user_ids:
            try:
                uid = get_user_id(username)
                user_ids[username] = uid
                updated = True
                print(f'✅ Lấy user_id {username}: {uid}')
            except Exception as e:
                print(f'❌ Lỗi lấy user_id {username}: {e}')
    if updated:
        save_user_ids(user_ids)

    # Setup stream
    stream = RetweetStream(BEARER_TOKEN)

    # Xóa hết rule cũ
    rules = stream.get_rules()
    if rules.data:
        rule_ids = [rule.id for rule in rules.data]
        stream.delete_rules(rule_ids)

    # Add rule theo dõi user_ids (stream filter "from:user_id")
    for uid in user_ids.values():
        stream.add_rules(tweepy.StreamRule(f"from:{uid}"))

    print(f'🚀 Bắt đầu stream theo dõi retweet user_ids: {list(user_ids.values())}')
    stream.filter(tweet_fields=["referenced_tweets", "author_id", "text"])

if __name__ == "__main__":
    main()
