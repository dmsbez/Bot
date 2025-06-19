import requests
import time

# === Config ===
TELEGRAM_TOKEN = '7970022703:AAEFU0v_402lujK3-FHkP6xW0NXKeteco3U'
TELEGRAM_CHAT_ID = '-1001875640464'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAA5n2gEAAAAAsht7hjWAW7ZBJ1zhxyFxdhfEahs%3DQVC3UohzEWyuwoq3cdEvFsBu6Zr52NbmvLISpOkdBawPDZKXru'

TWITTER_USERS = {
    'JnP6900erc': '1644057593241622529',
    'elonmusk': '44196397',
}

last_tweet_ids = {}

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print(f'⚠️ Telegram lỗi: {r.text}')
    except Exception as e:
        print(f'⚠️ Lỗi gửi Telegram: {e}')

def get_latest_tweet(user_id):
    url = f'https://api.twitter.com/2/users/{user_id}/tweets?max_results=5&tweet.fields=created_at'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        tweets = r.json().get('data', [])
        return tweets[0] if tweets else None
    except Exception as e:
        print(f'⚠️ Lỗi khi lấy tweet user {user_id}: {e}')
        return None

def main():
    usernames = list(TWITTER_USERS.keys())
    index = 0

    print(f"👀 Theo dõi {len(usernames)} người: {', '.join(usernames)}")

    while True:
        username = usernames[index]
        user_id = TWITTER_USERS[username]

        tweet = get_latest_tweet(user_id)
        if tweet:
            tweet_id = tweet['id']
            if last_tweet_ids.get(username) != tweet_id:
                url = f"https://x.com/{username}/status/{tweet_id}"
                msg = f"🧵 Tweet mới từ @{username}:\n\n{tweet['text']}\n\n{url}"
                send_telegram_message(msg)
                last_tweet_ids[username] = tweet_id
                print(f"[+] Gửi tweet của @{username}")

        index = (index + 1) % len(usernames)
        time.sleep(30)  # mỗi user cách nhau 20s → đủ giãn

if __name__ == '__main__':
    main()
