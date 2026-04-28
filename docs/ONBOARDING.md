# Onboarding Flow

The agent interviews you to configure your business. No technical setup required — just answer naturally.

## Phase 0: Choose Your Business Mode

The wizard starts by asking which **mode** matches your business. This determines the entire conversation flow, data structure, and operational patterns.

| Mode | Choose If... | Customer Typically Says |
|------|--------------|------------------------|
| **retail** | You sell physical products | "I want 2 of X and 1 of Y" |
| **services** | You book appointments/slots | "Do you have an opening for tomorrow?" |
| **freelance** | You do custom projects | "How much do you charge for a logo?" |
| **saas** | You sell software subscriptions | "I want to see a demo" |
| **rentals** | You rent items by date | "Do you have availability from the 15th to the 20th?" |
| **events** | You organize experiences | "I want to sign up for Saturday" |

You can always switch modes later by re-running the wizard.

---

## Method 1: Instagram Clone (Fastest, Most Accurate)

If you already have Instagram/WhatsApp conversations with customers:

1. **Agent asks:** *"Do you have Instagram messages with customers I can learn from?"*
2. **You say:** *"Yes"* or give your Meta export ZIP
3. **Agent extracts:** Your real voice, vocabulary, pricing style, and patterns
4. **Agent confirms:** *"Got it. You say 'Holii' and use 'okiiis'. Sound right?"*
5. **Done.** Your clone is ready.

**Note:** The Instagram clone works for **any mode**. The parser extracts vocabulary, tone, emoji usage, and response patterns — all of which transfer across business types.

---

## Method 2: Interview Mode (Build from Scratch)

If you're starting fresh or don't want to use past messages:

### Phase 1: Business Basics

| Agent Question | What It Learns |
|----------------|----------------|
| *"What's your business name?"* | Brand identity |
| *"What should you call yourself?"* | Bot name (can be same as business) |
| *"What currency do you use?"* | Price formatting |

### Phase 2: Your Offerings (Mode-Specific)

**Retail:** *"What products do you sell?"* → Product catalog with prices
**Services:** *"What services do you offer and how long does each take?"* → Service catalog
**Freelance:** *"What services do you offer and what's your starting price?"* → Project catalog
**SaaS:** *"What plans/tiers do you have?"* → Pricing tiers
**Rentals:** *"What items do you rent and what's the daily rate?"* → Inventory catalog
**Events:** *"What events do you have coming up?"* → Event catalog

### Phase 3: Your Voice

| Agent Question | What It Learns |
|----------------|----------------|
| *"How do you usually greet customers?"* | Greeting style |
| *"How do you say yes?"* | Confirmations ("sis", "okis", "bacan") |
| *"How do you quote prices?"* | Price format |
| *"How do you apologize for delays?"* | Service recovery |
| *"Are you casual or formal with clients?"* | Tone calibration |
| *"Do you use emojis?"* | Emoji style |

### Phase 4: Channel Setup

| Agent Question | What It Configures |
|----------------|-------------------|
| *"Which number for WhatsApp Business?"* | WhatsApp bridge target |
| *"Your Telegram user ID for admin?"* | Admin access control |
| *"What time should I do the daily check?"* | Proactive cron schedule |

### Phase 5: Test & Refine

The agent runs a **practice conversation** with you:

```
Agent: "Pretend I'm a customer. Say 'Hola, I'm interested'"
You: "Hola, I'm interested"
Agent: [Responds with your cloned voice]
You: "Too formal" / "Perfect" / "Say 'sis' more"
Agent: [Adjusts and tries again]
```

After 2-3 iterations, the agent locks in your style.

---

## Post-Setup: Daily Operation

Every morning (configurable time), the agent messages you on Telegram:

**Retail:** *"Buen dia! What do you have in stock today?"*
**Services:** *"Buen dia! Any changes to today's schedule?"*
**Freelance:** *"Buen dia! Any project updates I should know?"*
**SaaS:** *"Buen dia! Any support tickets or trial expirations today?"*
**Rentals:** *"Buen dia! Any returns or new reservations today?"*
**Events:** *"Buen dia! Any event updates or capacity changes?"*

You reply with updates. The agent uses them for all customer conversations that day.

---

## Commands (Telegram Admin)

| Command | Action |
|---------|--------|
| `stock` / `inventario` | Show current inventory (retail/rentals) |
| `horarios` / `agenda` | Show today's appointments (services/events) |
| `modo manual` | Pause bot — you handle WhatsApp |
| `modo auto` | Resume bot |
| `ventas hoy` | Query today's transactions (if connected) |
| `fiados` | Show pending customer debts |

---

## Updating Personality

Your voice evolves. To retrain:

```
Telegram: "Update my voice from new messages"
Agent: "Send me the new export or tell me what's changed"
```

The agent merges new patterns without losing what it already learned.

---

## Switching Business Modes

If your business evolves (e.g. you start as freelance but add a product line):

1. Re-run `scripts/setup_wizard.py`
2. Choose your new mode
3. The wizard preserves your voice/personality but updates data schemas and flows
4. Copy the new `data/` files to your agent directory

You can also **combine modes** by merging prompt fragments from multiple modes into a single `system_prompt`.
