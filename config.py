import os

# Railway Variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "1175970327"))
PDF_LINK = os.getenv("PDF_LINK", "https://bigcheeses.org/30phrases.pdf")
BOOKING_LINK = os.getenv("BOOKING_LINK", "https://bigcheeses.org/#start")
SHEET_WEBHOOK_URL = os.getenv("SHEET_WEBHOOK_URL", "")

# TEST_MODE=1: scheduled funnel messages are sent after 2/4/6/7 minutes for QA.
# TEST_MODE=0: production daily schedule: 24/48/72/96 hours.
TEST_MODE = os.getenv("TEST_MODE", "0")
