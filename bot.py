import tweepy
import requests
import json
import time
import os

# ==== CONFIG GIỮ NGUYÊN NHƯ YÊU CẦU ====
TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAA5n2gEAAAAA26eHEzWzzxcv%2FPF6qWgLhkX7tIY%3DMcYpMvmrA2wGHiDmZiw4N6dQfmcSCsfXZ5Co5xOwkZUUFw4BeE'

TWITTER_USERNAMES = ['JnP6900erc', 'elonmusk', 'cz_binance', 'VitalikButerin']
USER_IDS_CACHE_FILE = 'user_ids.json'

# === Hàm gửi tin nhắn Telegram ===
def send_telegram(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print(f'⚠️ Telegram Error: {r.text}')
    except Exception as e:
        print(f'⚠️ Lỗi gửi Telegram: {e}')

# === Lấy user_id từ Twitter, có cache ===
def get_user_id(username):
    url = f'https://api.twitter.com/2/users/by/username/{username}'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    while True:
        r = requests.get(url, headers=headers)
        if r.status_code == 429:
            print(f'🚫 Rate limit khi lấy user_id {username}, đợi 60s...')
            time.sleep(60)
            continue
        r.raise_for_status()
        return r.json()['data']['id']

def load_user_ids():
    if os.path.exists(USER_IDS_CACHE_FILE):
        with open(USER_IDS_CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_user_ids(data):
    with open(USER_IDS_CACHE_FILE, 'w') as f:
        json.dump(data, f)

# === Stream Twitter ===
class RetweetStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            if tweet.referenced_tweets:
                for ref in tweet.referenced_tweets:
                    if ref['type'] == 'retweeted':
                        uid = tweet.author_id
                        username = id_to_username.get(uid, f"user_id_{uid}")
                        text = tweet.text
                        url = f"https://x.com/{username}/status/{tweet.id}"
                        msg = f"🔁 Retweet từ @{username}:\n\n{text}\n\n{url}"
                        print(f'[📡] {msg}')
                        send_telegram(msg)
                        break
        except Exception as e:
            print(f'⚠️ Lỗi xử lý tweet: {e}')

    def on_connection_error(self):
        print('⚠️ Mất kết nối tới stream. Disconnect...')
        self.disconnect()

# === Chạy stream (reconnect khi lỗi) ===
def run_stream():
    stream = RetweetStream(BEARER_TOKEN)

    # Xóa hết rule cũ
    try:
        rules = stream.get_rules()
        if rules.data:
            rule_ids = [rule.id for rule in rules.data]
            stream.delete_rules(rule_ids)
    except Exception as e:
        print(f'⚠️ Lỗi khi xóa rule: {e}')

    # Thêm rule theo user_id
    for uid in id_to_username.keys():
        try:
            stream.add_rules(tweepy.StreamRule(f'from:{uid}'))
        except Exception as e:
            print(f'⚠️ Lỗi khi add rule {uid}: {e}')

    print(f'🚀 Bắt đầu stream theo dõi retweet các user: {list(id_to_username.values())}')
    stream.filter(tweet_fields=['referenced_tweets', 'author_id', 'text'])

def main():
    global id_to_username
    user_ids = load_user_ids()
    updated = False

    for username in TWITTER_USERNAMES:
        if username not in user_ids:
            try:
                uid = get_user_id(username)
                user_ids[username] = uid
                print(f'✅ Lấy user_id: {username} → {uid}')
                updated = True
            except Exception as e:
                print(f'❌ Lỗi lấy user_id của {username}: {e}')
    
    if updated:
        save_user_ids(user_ids)

    id_to_username = {v: k for k, v in user_ids.items()}  # map ngược để lấy username từ uid

    # Auto reconnect stream
    while True:
        try:
            run_stream()
        except Exception as e:
            print(f'💥 Lỗi stream: {e}, restart sau 15s...')
            time.sleep(15)

if __name__ == '__main__':
    main()
