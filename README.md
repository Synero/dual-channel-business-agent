# Dual Channel Business Agent

> Clone your real personality from Instagram DMs or create a new one from scratch and deploy an autonomous AI sales agent for your business.

**[Leer en Espanol](README_ES.md)**

**Built for real businesses** — An assistant that actually sounds like you, not a corporate chatbot.

Generic chatbots kill your personal brand. This agent learns your real voice, powered from actual Instagram/WhatsApp messages. It can handle customers 24/7 while you focus on what matters most.

---

## The Problem

Business owners live on socials (Instagram, WhatsApp, Facebook). But when you are out selling, working, or just busy, you can not reply to everyone. And generic AI assistants sound like call centers — customers notice immediately and bounce.

## The Solution

A dual-channel agent architecture that:

1. **Clones your real personality** from Instagram DM exports (not scripted)
2. **Handles customers on WhatsApp** with your actual voice, slang, and rhythm
3. **Gives you an admin dashboard on Telegram** to update data, check sales, and toggle the bot on/off
4. **Adapts to your business type** through 6 built-in modes: retail, services, freelance, SaaS, rentals, events
5. **Proactively checks operations** so the agent never promises what you can not deliver

---

## Architecture

```
+-----------------+     +------------------+     +-----------------+
|   WhatsApp      |     |   Hermes Agent   |     |    Telegram     |
|  (Customers)    |<----|   Gateway        |---->|  (Owner/Admin)  |
+-----------------+     +------------------+     +-----------------+
         |                        |                        |
         ▼                        ▼                        ▼
   Baileys Bridge          Personality Engine        Admin Control
   (WhatsApp Web)          +-------------+          +-------------+
                           |  Instagram  |          |  Mode Data  |
                           |  DM Parser  |          |   Files     |
                           +-------------+          +-------------+
```

**Channels:**
- **WhatsApp** — Customer-facing. Warm, natural, voice-cloned from real conversations.
- **Telegram** — Owner-only. Data updates, sales queries, bot on/off switch.

**Core Components:**
- `parse_instagram_export.py` — Extracts vocabulary, rhythm, and patterns from Meta's HTML export
- `proactive_stock.py` — Daily cron that asks the owner for today's operational status
- Hermes Agent gateway — Multi-platform orchestration with persistent memory

---

## Requirements

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) (multi-platform AI gateway) — **This is required. This repo is a skill/configuration for Hermes Agent, not a standalone app.**
- Node.js + Baileys (WhatsApp Web bridge)
- Python 3.9+
- Supabase (optional, for sales tracking)

---

## Business Modes

The agent adapts to your business type through **6 built-in modes**. Each mode changes the conversation flow, data schema, and operational patterns:

| Mode | For | Customer Says | Key Data |
|------|-----|---------------|----------|
| **retail** | Product sellers (food, clothing, handmade) | "I want 2 of X and 1 of Y" | Catalog, daily stock, orders, delivery logistics |
| **services** | Appointment businesses (salons, clinics) | "Do you have an opening for tomorrow?" | Service catalog, availability calendar, appointments |
| **freelance** | Project professionals (designers, devs) | "How much do you charge for a logo?" | Service catalog, projects, quotes, milestones |
| **saas** | Software subscriptions | "I want to see a demo" | Product tiers, trials, support tickets |
| **rentals** | Equipment/property rentals | "Do you have availability from the 15th to the 20th?" | Inventory, availability, reservations, deposits |
| **events** | Experience organizers | "I want to sign up for Saturday" | Event catalog, bookings, waitlist, capacity |

Each mode includes:
- **MODE.md** — Description, examples, conversation flow, payment patterns
- **data-schema.json** — Structured data files the agent reads/writes
- **prompt-fragments.md** — Mode-specific instructions for the LLM

---

## Quick Start

> **The fastest way:** Tell your Hermes Agent to set this up for you. Since you already have an AI agent running, let it handle the clone, config, and deployment.

### Manual Setup (if you prefer)

**1. Install Hermes Agent**

```bash
pip install hermes-agent
# or follow: https://github.com/NousResearch/hermes-agent#installation
```

**2. Clone this skill into your Hermes directory**

```bash
cd ~/.hermes/skills/
git clone https://github.com/Synero/dual-channel-business-agent.git
cd dual-channel-business-agent
```

**3. Run the setup wizard**

```bash
python scripts/setup_wizard.py
```

The wizard interviews you to configure your business. It adapts questions based on your chosen mode (retail, services, freelance, SaaS, rentals, or events). It generates:
- `generated_config/SOUL.md` — Your agent's personality
- `generated_config/data/` — Mode-specific data files (catalog, calendar, projects, etc.)
- `generated_config/config.yaml` — Hermes Agent config snippet

**4. Point Hermes Agent to this config**

Copy the generated files to your Hermes Agent directory, or merge the config into your existing `~/.hermes/config.yaml`.

**5. Start the gateway**

```bash
hermes gateway run
```

Your agent connects to WhatsApp (via Baileys bridge on port 3002) and Telegram.

---

### Option A: Clone from Instagram (Recommended)

If you already have Instagram/WhatsApp conversations with customers:

1. **Download your Instagram data** → See [Meta Export Guide](docs/META_EXPORT_GUIDE.md)
2. **Run the parser:** `python scripts/parse_instagram_export.py /path/to/messages/ --business-name "Your Name"`
3. **The wizard picks this up automatically** when it detects `personality_profile.json`

> Or just tell your Hermes Agent: *"Download my Instagram data, parse it, and set up the business agent for me."*

### Option B: Create New Personality

Run the wizard and answer the questions. The agent interviews you to build your business persona from scratch.

---

## Documentation

- [Meta Account Center Export Guide](docs/META_EXPORT_GUIDE.md) — How to download your Instagram DMs
- [Onboarding Flow](docs/ONBOARDING.md) — How the agent interviews you to configure the business
- [Telegram Admin Guide](docs/TELEGRAM_ADMIN.md) — Commands for the owner

---

## License

MIT — Built with love for businesses everywhere.
