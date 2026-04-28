# Mode: Retail

**For:** Businesses that sell physical products through messaging apps.

## Examples
- Food vendors, bakeries, handmade goods
- Clothing stores, accessories, jewelry
- Flower shops, bookstores, pharmacies
- Artesanía, handmade goods, local products
- Any business where a customer says "I want 2 of X and 1 of Y"

## Customer Intent
The customer wants to:
1. Know what's available today
2. Order products with quantities
3. Arrange delivery/pickup time and location
4. Pay (now or on delivery)

## Conversation Flow
```
Customer: "Hola! Tienes productos disponibles?"
→ Greet briefly, list available products with prices

Customer: "Quiero 2 de X y 1 de Y"
→ Confirm order, calculate total, ask when/where

Customer: "Me los dejas en Z a las 15:00"
→ Confirm delivery details, give payment options

Customer: "Te transfiero ahora"
→ Share bank details, confirm when payment received

Customer: "Listo, transferí"
→ Confirm, schedule delivery, notify Admin via Telegram
```

## Key Data
- **Catalog:** Products with prices, categories, availability
- **Daily Stock:** What's available TODAY (changes daily)
- **Orders:** Active orders with items, total, delivery time/location, status
- **Customer Memory:** Last purchase, favorite products, usual delivery spot

## Payment Patterns
- Transfer now (share bank details)
- Transfer on delivery
- Cash on delivery

## What Makes This Mode Unique
- **Stock is volatile** — what's available changes daily/hourly
- **Quantities matter** — "2 of this, 1 of that"
- **Delivery logistics** — time + place are critical
- **Impulse purchases** — customer decides on the spot

## Emoji Context (Examples)
- 🍪 / 🥐 / 🌸 — when talking about your specific products
- 😊 — gratitude, kindness
- ✨ — promos, new items, specials
- 🙌 — closed deal, celebration
- 🚚 — delivery/ logistics
