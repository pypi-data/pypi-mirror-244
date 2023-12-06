import requests

def telegram_notification(token: str, message: str, chat_id: str) -> requests.models.Response:
    """
    Sends Telegram Message
    """
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        "text": message,
        "parse_mode": "html",
        "chat_id" : chat_id
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response