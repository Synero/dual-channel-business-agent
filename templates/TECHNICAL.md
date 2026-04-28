# Technical Operator Guide (NOT FOR LLM PROMPT)
# This file contains file paths and technical details for the human operator.
# NEVER include this content in the system_prompt.

## Data Files

| File | Purpose | Who Writes |
|------|---------|------------|
| `data/stock_hoy.json` | Daily active stock list | Admin (Telegram) |
| `data/clientes.json` | Customer memory by phone number | Bot (auto) |
| `data/pedidos.json` | Scheduled and completed orders | Bot (auto) |
| `data/datos_pago.json` | Banking details for transfers | Admin (manual) |
| `data/products.json` | Product catalog with prices | Script or Admin |

## WhatsApp Toolset (Limited)

WhatsApp platform should ONLY have:
- `file` — read/write local JSON data files
- `messaging` — send notifications to Telegram admin

NO terminal, NO browser, NO web search on WhatsApp.

## Telegram Admin (Full Access)

Telegram platform has full toolset:
- `file` — manage data files
- `terminal` — run scripts, git, systemctl
- `browser` — web access if needed
- `tts` — voice responses
- `messaging` — confirm notifications
- etc.

## Scripts

- `scripts/sync_products.py` — sync product catalog from companion app
- `scripts/proactive_stock.py` — morning stock check cron
