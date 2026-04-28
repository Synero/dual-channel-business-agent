#!/usr/bin/env python3
"""Proactive script: the bot asks the owner for today's operational status.

Usage: add to crontab to run every morning.
Example (10:00 AM local time):
    0 10 * * * /usr/bin/python3 /path/to/proactive-stock.py

Requires: TELEGRAM_BOT_TOKEN and ADMIN_CHAT_ID in environment or .env file.
"""
import urllib.request
import urllib.parse
import random
import os

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "YOUR_ADMIN_CHAT_ID")

if not TOKEN:
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("TELEGRAM_BOT_TOKEN="):
                    TOKEN = line.strip().split("=", 1)[1]
                    break

if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN not found")
    exit(1)

if CHAT_ID == "YOUR_ADMIN_CHAT_ID":
    print("ERROR: Set ADMIN_CHAT_ID environment variable")
    exit(1)

MESSAGES = [
    "Good morning! What's available today?",
    "Hey! What are we working with today?",
    "Morning check-in — what's on the menu/agenda today?",
]

text = random.choice(MESSAGES)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"})

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode()
        if '"ok":true' in body:
            print(f"Message sent: {text}")
        else:
            print(f"Telegram error: {body}")
except Exception as e:
    print(f"Error: {e}")
