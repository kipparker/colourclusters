import requests
import os


def telegram_bot_sendtext(bot_message):
    bot_token = os.environ.get("TELEGRAM_KEY", "fail")
    bot_chatID = os.environ.get("CHAT_ID", "quietly")
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&parse_mode=Markdown&text="
        + bot_message
    )
    response = requests.get(send_text)
    return response.json()
