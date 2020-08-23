import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
GROUP_ID = int(os.getenv("GROUP_ID"))
