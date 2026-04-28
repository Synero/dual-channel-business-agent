# Telegram Admin Guide

Your private control panel. Only your Telegram user ID can access these commands.

## Daily Commands

| Command | What It Does |
|---------|-------------|
| `stock` | Shows current inventory from stock.json |
| `sales today` | Queries your database for today's sales (if connected) |
| `pending` | Shows pending customer debts or open orders |
| `what do I have today?` | Same as stock, but conversational |

## Bot Control

| Command | Effect |
|---------|--------|
| `manual mode` | Bot stops. You handle WhatsApp yourself. |
| `auto mode` | Bot resumes answering customers. |
| `status` | Shows current mode (manual/auto) |

## Updating Stock

Just tell the bot naturally:

> "Today I have: product A 5, product B 3, product C 2"

The bot updates stock.json automatically.

Or send a structured list:

```
Stock today:
- Product A: 5
- Product B: 3
- Product C: 2
- Product D: 0
```

## Voice Messages

Send voice messages on Telegram. The bot will:
1. Transcribe your audio
2. Respond by text
3. Also send a voice reply (TTS) if configured

This is great when you're hands-full working.

## Personality Updates

If your style changes or you want to correct the bot:

> "Don't say 'okis' so often"
> "Always mention prices when someone asks"
> "When they say hello, ask how you can help"

The bot logs these corrections and adjusts.

## Getting Help

> "How does this work?" — Bot explains its own capabilities
> "What can you do?" — Lists available commands
