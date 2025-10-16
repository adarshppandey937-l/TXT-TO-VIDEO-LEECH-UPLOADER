

from os import environ

API_ID = int(environ.get("API_ID", "23916386"))
API_HASH = environ.get("API_HASH", "613666377f6a46bba98777abf5ce402e")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

# Force Subscribe Configuration
FORCE_SUB_CHANNEL = environ.get("FORCE_SUB_CHANNEL", "neerajdrm)  # Channel username without @, 
FORCE_SUB_CHANNEL_LINK = environ.get("FORCE_SUB_CHANNEL_LINK", "https://t.me/neerajdrm")  # Channel link

# Admin Configuration
ADMINS = list(map(int, environ.get("ADMINS", "1483382098").split()))

# Optional: Bot Owner ID
OWNER_ID = int(environ.get("OWNER_ID", "1483382098"))

# Database URL (if you want to add database support later)
DATABASE_URL = environ.get("DATABASE_URL", "")





