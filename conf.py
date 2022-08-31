import os

BOT_TOKEN = os.environ.get("TELEGRAM_KEY", "fail")
BOT_CHATID = os.environ.get("CHAT_ID", "quietly")

MONGO_PASSWD = os.environ.get("MONGO_PASSWD")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_DOMAIN = os.environ.get("MONGO_DOMAIN")


AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")

AUTH0_DOMAIN = "dev-vdrz-f6c.eu.auth0.com"
AUTH0_AUDIENCE = "sky.kip.dev"
BUCKET = "colourclusters-api-upload"
