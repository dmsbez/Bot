import requests
import time

# ==== Cấu hình ====
TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAA5n2gEAAAAA26eHEzWzzxcv%2FPF6qWgLhkX7tIY%3DMcYpMvmrA2wGHiDmZiw4N6dQfmcSCsfXZ5Co5xOwkZUUFw4BeE'

# ==== Danh sách Twitter usernames ====
TWITTER_USERNAMES = ['JnP6900erc', 'elonmusk', 'cz_binance', 'VitalikButerin']
CHECK_INTERVAL = 60  # giây

# ==== Lưu trạng thái tweet cuối cùng của mỗi user ====
last_tweet_ids = {}

def get_user_id(username):
    url = f'https://api.twitter.com/2/users/by/username/{username}'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()['data']['id']

def get_latest_tweet(user_id):
    url = f'https://api.twitter.com/2/users/{user_id}/tweets?max_results=5&tweet.fields=created_at'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    tweets = r.json().get('data', [])
    return tweets[0] if tweets else None

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        print(f'⚠️ Telegram error: {r.text}')

def main():
    print(f"👁️ Theo dõi các Twitter users: {', '.join(TWITTER_USERNAMES)}")

    # Map username -> user_id
    user_ids = {}
    for username in TWITTER_USERNAMES:
        try:
            user_id = get_user_id(username)
            user_ids[username] = user_id
        except Exception as e:
            print(f'❌ Lỗi lấy user ID của {username}: {e}')

    while True:
        for username, user_id in user_ids.items():
            try:
                tweet = get_latest_tweet(user_id)
                if tweet:
                    tweet_id = tweet['id']
                    if last_tweet_ids.get(username) != tweet_id:
                        msg = f"🧵 Tweet mới từ @{username}:\n\n{tweet['text']}\n\nhttps://x.com/{username}/status/{tweet_id}"
                        send_telegram_message(msg)
                        last_tweet_ids[username] = tweet_id
            except Exception as e:
                print(f'⚠️ Lỗi khi check @{username}: {e}')
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
