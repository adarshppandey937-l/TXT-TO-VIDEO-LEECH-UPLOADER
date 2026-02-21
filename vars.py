

from os import environ

API_ID = int(environ.get("API_ID", "22865155"))
API_HASH = environ.get("API_HASH", "e430e3f61712616b926be959f1612c46")
BOT_TOKEN = environ.get("BOT_TOKEN", "8203333831:AAE1c3ip57X_xKzoiJRQ5N8WVGaGKstl-aM")

# Force Subscribe Configuration
FORCE_SUB_CHANNEL = environ.get("FORCE_SUB_CHANNEL", "safalta_batc6766")  # Channel username without @, 
FORCE_SUB_CHANNEL_LINK = environ.get("FORCE_SUB_CHANNEL_LINK", "https://t.me/safalta_batc6766")  # Channel link

# Admin Configuration
ADMINS = list(map(int, environ.get("ADMINS", "8453406690").split()))

# Optional: Bot Owner ID
OWNER_ID = int(environ.get("OWNER_ID", "8453406690"))

# Database URL (if you want to add database support later)
DATABASE_URL = environ.get("DATABASE_URL", "mongodb+srv://adarshppandey937:uIoPcln9vXQBF0vP@cluster0.o9mn6hb.mongodb.net/?")










