---
name: dual-channel-business-agent
version: 1.0.0
author: Synero (Ignacio Bastias)
description: >
  Deploy a WhatsApp/Instagram customer-service AI agent with a separate admin
  interface (Telegram/Discord). The agent learns its personality organically
  from real Instagram/Meta message exports, handles business conversations
  naturally, and can be paused instantly so the owner replies manually.
  Supports 6 business modes: retail, services, freelance, saas, rentals, events.
requires:
  - Hermes Agent >= 0.7.0
  - Node.js >= 20
  - systemd (for production persistence)
  - Linux VPS with public IP or Tailscale
---

# Dual-Channel Business Agent

Complete production-ready **framework** for a business AI agent that serves
customers via **WhatsApp** (or Instagram DM) while the owner manages it via
**Telegram** (or Discord) in a private admin channel.

**Not a generic template.** The agent adapts to your business type through
**business modes** — each mode changes the conversation flow, data schema, and
operational patterns. Whether you sell pastries, cut hair, build websites, rent
cameras, or run yoga retreats, the agent speaks your language and handles your
workflow.

## What This Gives You

| Channel | Audience | Purpose |
|---------|----------|---------|
| **WhatsApp** | Customers | Orders, stock queries, natural conversation |
| **Telegram** | Owner only | Admin commands, stock updates, mode switching, DB queries |

**Key features:**
- **Organic personality** — learns tone from real Instagram/Meta exports, not scripted
- **Manual/Auto switch** — owner can pause the bot anytime from Telegram to reply manually
- **TTS (optional)** — ElevenLabs voice responses for admin channel
- **Stable systemd services** — bridge and gateway run independently, auto-restart on crash
- **No QR re-scanning** — Baileys session persists across reboots

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     Business Gateway (Hermes)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Telegram      │  │  API Server    │  │  WhatsApp      │ │
│  │  (Admin)       │  │  Port 3001     │  │  (Customers)   │ │
│  │  Chat ID filter│  │              │  │              │ │
│  └──────────────┘  └──────────────┘  └─────┬────────────┘ │
│                              │                                   │
│                         ─────´───── HTTP localhost:3002              │
└──────────────────────────────────────────────────────────────────┘
                              │
                    ┌────────────────────────────┐
                    │  WhatsApp Bridge (Baileys)          │
                    │  Standalone Node.js service           │
                    │  Port 3002  ·  systemd auto-restart   │
                    |  Session dir: ~/.hermes-business/...   |
                    └────────────────────────────┘
```

**Why separate the bridge?** The Hermes gateway's built-in subprocess management
has a known bug where the WhatsApp bridge stays `disconnected` under systemd.
Running the bridge as its own systemd service eliminates this and gives you
independent logs and restart policies.

---

## Business Modes

The skill ships with **6 business modes**. Each mode defines:
- **Conversation flow** — how customers interact with the agent
- **Data schema** — what JSON files the agent reads/writes
- **Prompt fragments** — mode-specific instructions for the LLM
- **Payment patterns** — how money changes hands

| Mode | For | Customer Says | Key Data |
|------|-----|---------------|----------|
| **retail** | Product sellers (food, clothing, handmade) | "I want 2 of X and 1 of Y" | Catalog, daily stock, orders, delivery logistics |
| **services** | Appointment businesses (salons, clinics, mechanics) | "Do you have an opening for tomorrow?" | Service catalog, availability calendar, appointments |
| **freelance** | Project-based professionals (designers, devs, photographers) | "How much do you charge for a logo?" | Service catalog, projects, quotes, milestones |
| **saas** | Software subscriptions (apps, platforms, APIs) | "I want to see a demo" | Product tiers, trials, support tickets, onboarding |
| **rentals** | Rental businesses (equipment, cars, properties) | "Do you have availability from the 15th to the 20th?" | Inventory, availability calendar, reservations, deposits |
| **events** | Experience organizers (tours, classes, retreats) | "I want to sign up for Saturday" | Event catalog, bookings, waitlist, capacity |

### How Modes Work

1. **During setup**, the wizard asks which mode matches your business
2. **It copies** the mode's `data-schema.json` to your `data/` directory
3. **It generates** a `system_prompt` by combining:
   - Universal fragments (identity, voice style, iron rules)
   - Mode-specific fragments from `modes/{mode}/prompt-fragments.md`
   - Your Instagram/Meta vocabulary (if exported)
4. **The agent** uses mode-appropriate conversation patterns automatically

### Adding a New Mode

Modes are self-contained in `modes/{mode_name}/`:

```
modes/
  your_mode/
    MODE.md              # Description, flow, examples
    data-schema.json     # JSON schemas for this mode
    prompt-fragments.md  # LLM instructions for this mode
```

Follow the pattern of existing modes. The wizard will auto-detect it.

### Mode-Agnostic Features (All Modes)

These work identically across all modes:
- **Instagram/Meta personality clone** — vocabulary extraction is mode-independent
- **Dual channel** — WhatsApp public, Telegram admin
- **Manual/Auto switch** — owner pauses bot from Telegram
- **Admin notifications** — completed transactions alert owner on Telegram
- **Payment data** — `data/datos_pago.json` for transfer details
- **Customer memory** — `data/clientes.json` keyed by phone number

---

---

## Prerequisites

- Linux VPS (Ubuntu/Debian recommended) with Node.js 20+
- Hermes Agent installed (`pip install hermes-agent` or git clone)
- A second `HERMES_HOME` directory for this instance (e.g. `~/.hermes-mybusiness`)
- WhatsApp Business account on the owner's phone
- Telegram Bot token from @BotFather
- (Optional) ElevenLabs API key for TTS voice responses
- (Optional) Meta/Instagram message export for personality training

---

## Quick Start

### 1. Install Hermes Agent

This repo is a **skill/configuration package** for Hermes Agent, not a standalone app.

```bash
pip install hermes-agent
# Or clone from https://github.com/your-username/hermes-agent and install locally
```

### 2. Create Isolated Instance

```bash
export HERMES_HOME="$HOME/.hermes-mybusiness"
mkdir -p "$HERMES_HOME"/{data,logs,platforms/whatsapp/session}
cp -r "$HOME/.hermes/hermes-agent" "$HERMES_HOME/"
```

### 2. Install Bridge Dependencies

```bash
cd "$HERMES_HOME/platforms/whatsapp"
npm init -y
npm install @whiskeysockets/baileys @hapi/boom pino qrcode
```

### 3. Copy Config Template

Use `templates/config.yaml` from this skill. Customize:
- `model.default` and `model.api_key`
- `platforms.telegram` (add your bot token to `.env`)
- `platforms.whatsapp.extra.bridge_port` and `session_path`
- `tts` section (optional)

### 4. Set Environment

Create `~/.hermes-mybusiness/.env`:

```bash
OPENCODE_GO_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here        # optional
TELEGRAM_BOT_TOKEN=your_bot_token
WHATSAPP_HOME_CHANNEL=dummy             # suppresses gateway spam
```

### 5. Configure Personality (Organic, Not Scripted)

**Option A — Instagram/Meta export (recommended):**
1. Owner downloads their Instagram data export from Meta
2. Extract `messages/inbox/` folder
3. Run `scripts/parse-instagram-export.py` (see references/)
4. Parsed conversations go to `chat_logs/instagram/`
5. The `system_prompt` references these files so the LLM learns real vocabulary

**Option B — Manual SOUL.md:**
Use `templates/SOUL.md` as a starting point and fill in real examples.

### 6. Create Systemd Services

**Bridge service** (`~/.config/systemd/user/mybiz-whatsapp-bridge.service`):

```ini
[Unit]
Description=MyBiz WhatsApp Bridge
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.hermes-mybusiness/platforms/whatsapp
ExecStart=/usr/bin/node %h/.hermes/hermes-agent/scripts/whatsapp-bridge/bridge.js \
  --port 3002 --session %h/.hermes-mybusiness/platforms/whatsapp/session --mode bot
Restart=always
RestartSec=5
EnvironmentFile=%h/.hermes-mybusiness/.env
StandardOutput=append:%h/.hermes-mybusiness/logs/whatsapp-bridge.log
StandardError=append:%h/.hermes-mybusiness/logs/whatsapp-bridge.log

[Install]
WantedBy=default.target
```

**Gateway service** (`~/.config/systemd/user/mybiz-gateway.service`):
Use the standard Hermes gateway service pointing to your `HERMES_HOME`.

Enable and start:

```bash
systemctl --user daemon-reload
systemctl --user enable mybiz-whatsapp-bridge mybiz-gateway
systemctl --user start mybiz-whatsapp-bridge mybiz-gateway
```

### 7. Authenticate WhatsApp (One-Time)

```bash
cd ~/.hermes-mybusiness/platforms/whatsapp
node generate-qr-image.mjs
# Scan QR with WhatsApp Business → status changes to connected
```

Session files are stored in `session/` and persist across reboots.

---

## Admin Commands (Telegram)

| Command | Effect |
|---------|--------|
| `modo manual` / `pausar whatsapp` / `yo respondo` | Bot stops answering WhatsApp. Owner sees messages on phone and replies manually. |
| `modo auto` / `activar whatsapp` / `bot responde` | Bot resumes answering WhatsApp automatically. |
| `que modo estoy` | Shows current mode (auto/manual). |
| `stock hoy: product1, product2` | Updates daily stock file. |
| `que stock tengo hoy?` | Reads stock file and reports. |
| *(voice message)* | Bot replies with **audio + text** (if TTS configured). |

The mode switch works via a JSON file (`data/whatsapp-mode.json`) that the bridge
checks on every incoming message. Zero restart needed.

---

## WhatsApp Commerce Personality (Critical)

**Instagram ≠ WhatsApp.** Instagram DMs are friend-chat; WhatsApp is where people
come to **buy**. A prompt optimized for Instagram friend-chat will be too passive
for WhatsApp and will lose sales.

### The "Too Passive" Trap

If your prompt says things like:
- "NO listes productos en el primer hola"
- "NO seas invasiva"
- "Saluda como amigo y espera a que el cliente diga algo más"

You will get this (bad):

```
Cliente: Hola tienes productos??
Bot:     Holii          ← dejó al cliente colgado

Cliente: Que productos tiene?
Bot:     Holii! Dime    ← repitió saludo como si no viera la pregunta
```

### The Fix

Your WhatsApp rules should say:

1. **Si el cliente dice "Hola + pregunta", saludá BREVE y respondé.** No lo ignores.
2. **Si ya saludó antes y ahora pregunta por productos, NO repitas el saludo.** Respondé directo.
3. **Si dice "hola" solo, sin nada más, abrí la conversación:** "Holii, dime!" o "Holii, qué buscabas?"
4. **Sé amable y cálida.** La gente compra productos, no atención al cliente de banco.

Include explicit **GOOD/BAD examples** in the system prompt for the WhatsApp scenario.

---

### The "Technical Leak" Trap (CRITICAL)

The most embarrassing failure is when the bot **tells the customer about its own implementation** — file paths, JSON, database operations, or tool names.

**Real example of what went wrong:**
The prompt contained: *"lee ~/.hermes-business/data/stock_hoy.json. El campo 'activos' dice que sabores hay HOY."*

The LLM, not understanding the boundary between "my instructions" and "what I say to the customer", responded to a customer with:
- *"read_file: /home/user/.hermes-business/data/stock_hoy.json"*
- *"Guarda el pedido en ~/.hermes-business/data/pedidos.json"*

This instantly destroys the illusion. The customer sees code, paths, and raw JSON.

### The Fix: Separate Technical from Customer-Facing

**NEVER put in system_prompt:**
- File paths (`~/.hermes/...`, `/tmp/...`, etc.)
- JSON field names (`"activos"`, `"estado"`, `"id"`)
- Tool names or operations (`guarda en`, `lee el archivo`, `consulta la tabla`)
- Database table names or SQL
- Process descriptions (`auto-incremental`, `número de teléfono` as a technical key)

**What goes in system_prompt instead:**
- Behavior and personality only
- Prices, products, tone rules
- Examples of natural speech
- What NOT to say (banned phrases)

**Where technical details live:**
Create a separate file like `TECHNICAL.md` or `OPERATOR.md` in the skill directory. This file is for the human operator only. The LLM still uses tools (file, terminal, etc.) via its tool-calling capability — it does NOT need to know file paths in its prompt.

If the LLM absolutely needs file awareness, wrap it in scripts with friendly names:
- `get_stock.py` instead of "read ~/.hermes-business/data/stock_hoy.json"
- `save_order.py` instead of "write to pedidos.json"

**Also ban these verbs in the prompt** because they imply technical action visible to the customer:
- *"consulto"*, *"reviso"*, *"mire"*, *"veo"*, *"busco"*, *"chequeo"*, *"confirmo"* (in the sense of checking something)
- *"estoy revisando"*, *"dame un seg"*, *"cargando"*

The customer should believe you already know everything from memory.

**Iron Rule for the prompt:**
```
REGLA ABSOLUTA:
NUNCA menciones que usas archivos, rutas, JSON, base de datos, sistema, o tecnología.
El cliente no sabe que existe nada técnico. Actúa como si todo lo supieras de memoria.
NUNCA digas "consulto", "reviso", "mire", "veo", "busco", "chequeo".
```

---

### The "Breaking Character" Trap (CRITICAL)

Even worse than being passive is when the bot **admits there is a human behind it**.
This happens when the system prompt itself leaks the owner's identity.

**Real example of what went wrong:**
The prompt said: *"Eres el bot de un emprendimiento de productos handmade."*

This caused the model to naturally say things like:
- *"Dejame confirmar con el dueno y te aviso"*
- *"Habla con el al +56*********"*
- *"El esta ocupado ahora"*

This destroys the illusion completely. Customers know they're talking to a bot,
and worse, they get a blocked phone number.

### The Fix: Iron Rules (Reglas de Hierro)

Your system prompt must declare the bot IS the business, not an assistant OF the business:

```
Eres el negocio. Vendes productos. No eres "asistente de" nadie.
No hay jefe, no hay equipo, no hay persona real detras de ti.
Eres el negocio.
```

And you need **explicit negative constraints** in the prompt:

```
=== REGLAS DE HIERRO ===
1. NUNCA digas que eres una IA, un bot, una asistente, o un programa.
2. NUNCA menciones a [OWNER NAME] ni ningún nombre de persona real.
3. NUNCA digas "déjame confirmar con...", "te paso con...",
   "habla con...", o cualquier frase que sugiera que hay alguien más.
4. NUNCA des un número de teléfono alternativo o digas "escríbele a...".
5. NUNCA traduzcas del inglés. NO uses español neutro forzado.
```

Also add these phrases to the **banned phrases list**:
- *"Dame un momento para confirmar"*
- *"Te paso con..."*
- *"Habla con..."*
- *"Escríbele a..."*

**Privacy note:** Even if the model partially redacts a phone number (***),
it still reveals that a human exists. The only safe rule is: **never mention anyone else exists.**

---

### The "Forced Emoji" Trap

Overusing emojis or using generic ones (🔥, 👍) in every message makes the bot feel like a marketing template.

**The Fix: Contextual, Reactive Emojis**

Emojis should react to the topic, not decorate:
- 🍪 / 📦 / 🎨 when talking about your specific products/orders/projects
- 😊 when someone thanks you or is kind
- ✨ when highlighting something special (promo, new item)
- 💕 when someone shows affection or enthusiasm
- 🙌 when celebrating or closing a deal well
- Often 0 emojis, sometimes 1, rarely 2. Never more than 2.

Ban the aggressive/generic 🔥. It reads as hype-beast energy, not natural.

**Example transition:**
```
Before (forced): "Total $7.000 🔥 Te lo dejo en el centro?"
After (contextual): "Total $7.000. ¿Para cuándo lo quieres?"  (zero emojis, direct)
Or: "Total $7.000 🍪 ¿Te lo llevo al centro?"  (relevant emoji)
```

---

### The "Generic Delivery Offer" Trap

A generic offer like "Te las dejo en el centro?" assumes the customer's location and skips the actual order confirmation flow.

**The Fix: Ask When, Where, and Remember**

For every order, collect:
1. What (products + quantities + total)
2. When (date + time)
3. Where (delivery point or address)

And **remember the customer** across conversations:

```
(Cliente con historial)
Cliente: "Hola!"
Bot: "Holii! 🍪 ¿Quieres lo mismo que la última vez?
       2 de X y 1 de Y.
       ¿Te lo dejo en tu ubicación habitual como siempre?"

(Cliente nuevo)
Cliente: "Quiero 3 productos"
Bot: "Okiiis! ¿Cuáles te tincan? Y ¿dónde te los dejo? ¿A qué hora te conviene?"
```

**Client memory fields** (stored in `data/clientes.json`, keyed by phone number):
- `nombre` — if they share it
- `ultima_compra` — what, when, how much
- `ubicacion` — preferred delivery spot
- `horario_preferido` — usual order time
- `preferencias` — most-ordered items or preferences
- `notas` — allergies, preferences

The bot reads this at conversation start and uses it naturally — never mentioning "I looked you up" or "I have your data."

---

### Payment & Banking Data

When a customer asks how to pay or requests transfer details:

**What to say:**
```
"Puedes pagar ahora por transferencia, o al momento de la entrega
 en efectivo o transferencia, como te acomode 😊"
```

**If they choose transfer now:**
- Read `data/datos_pago.json` (do NOT hardcode in prompt for security)
- Share exactly: titular, bank, account type, account number, email
- Never invent or approximate banking details
- Never make the customer wait — the data is fixed, share immediately

**Template `datos_pago.json`:**
```json
{
  "titular": "YOUR_FULL_NAME",
  "rut": "YOUR_RUT",
  "banco": "YOUR_BANK",
  "tipo_cuenta": "YOUR_ACCOUNT_TYPE",
  "numero_cuenta": "YOUR_ACCOUNT_NUMBER",
  "correo": "YOUR_EMAIL",
  "opciones_pago": [
    "Transferencia ahora",
    "Transferencia al momento de la entrega",
    "Efectivo al momento de la entrega"
  ]
}
```

**Security:** Only the admin (via Telegram) can modify this file. The bot reads it but never reveals it was "read from a file."

---

### Admin Synchronization (Telegram)

**Every completed or scheduled order must notify the admin on Telegram immediately.**
But the customer must NEVER know this happened.

**WRONG way to write this in the prompt** (causes the bot to say "avisé a admin" to the customer):
```
PEDIDOS:
- Entrega inmediata: confirma pedido, calcula total, pregunta cuándo y dónde.
  Después avisa a Admin por Telegram.
- CUALQUIER compra concretada debe avisar inmediatamente a Admin por Telegram.
```

**RIGHT way** (internal action, invisible to customer):
```
PEDIDOS:
- Entrega inmediata: confirma pedido, calcula total, pregunta cuándo y dónde entregar.
- Para otra fecha: confirma, registra el pedido, confirma con el cliente.
- DESPUÉS de concretar CUALQUIER compra, tu respuesta al cliente DEBE ser solo
  la confirmación del pedido. NUNCA digas que vas a avisar a alguien más.

NOTIFICACIONES INTERNAS (INVIOLABLE):
- NUNCA le digas al cliente que vas a avisar a alguien, notificar, informar a admin,
  o hacer cualquier acción aparte de confirmarle su pedido.
- El cliente NO SABE que existe un admin, Telegram, ni ningún sistema.
  Tú eres la única persona que atiende.
- Ejemplo de lo que SÍ dices al cliente: "Listo, quedó agendado para mañana a las 15:00. 🍪"
- Ejemplo de lo que NUNCA dices: "Avisé a admin", "Le aviso a mi jefa",
  "Ya notifiqué", "Déjame avisarle a alguien".
- INFRACCIÓN GRAVE: Si dices al cliente que avisaste a alguien, rompes la ilusión
  de que tú eres la dueña del negocio.
```

**Why this matters:** The LLM cannot distinguish between "instructions for me" and "what I say to the user." If you tell it to "notify admin", it may say that out loud. Frame internal actions as silent background tasks.

**Tool configuration:** Keep the `messaging` tool available on WhatsApp so the bot CAN send Telegram notifications, but set `display.platforms.whatsapp.tool_progress: off` so the customer never sees a "Using messaging..." spinner.

---

## Daily Stock & Product Management

The bot needs to know what products exist, what flavors are in stock, and current
prices. There are two patterns depending on whether you have a companion app.

### Pattern A: Companion App (Supabase Table) — Recommended

If you have a companion web/mobile app (like `mybusiness-app`), store products in a
**Supabase `products` table** so both the app and the bot read from the same source.

**Why:** If the app hardcodes products in `useState` (like `const [productos] = useState([...])`),
the bot and app will drift. Customers will see different prices on WhatsApp vs the app.

**SQL to create the table:**

```sql
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio INT NOT NULL,
    activo BOOLEAN DEFAULT true,
    es_promo BOOLEAN DEFAULT false,
    descripcion TEXT,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read active" ON products FOR SELECT USING (activo = true);
CREATE POLICY "Allow service role all" ON products FOR ALL USING (true) WITH CHECK (true);
```

**Bot config:** In `system_prompt`, tell the bot to query Supabase for products
instead of reading a local file:

```
Lee SIEMPRE la tabla `products` de Supabase antes de responder sobre productos.
Solo muestra productos con activo=true.
```

**Admin price changes via Telegram:**

```
Precio simples a 3000    → UPDATE products SET precio=3000 WHERE categoria='simple'
Desactivar Producto X  → UPDATE products SET activo=false WHERE nombre='Producto X'
```

### Pattern B: Standalone Bot (stock.json)

If there is no companion app, a local JSON file is simpler:

Store at `~/.hermes-mybusiness/data/stock.json`:

```json
{
  "fecha": "2026-04-27",
  "actualizado_por": "Owner",
  "productos": {
    "producto_a": {
      "descripcion": "Producto A, descripcion corta",
      "precio": 2500,
      "variantes_disponibles": [
        {"variante": "Opcion 1", "stock": 2},
        {"variante": "Opcion 2", "stock": 3}
      ]
    },
    "producto_b": {
      "descripcion": "Producto B, descripcion corta",
      "precio": 3000,
      "promo": "2x $5.000",
      "variantes_disponibles": [
        {"variante": "Opcion 3", "stock": 3}
      ]
    },
    "producto_c": { "precio": 5000, "stock": 3 },
    "producto_d": { "precio": 6000, "stock": 3 }
  },
  "sin_stock": ["Producto E", "Producto F"]
}
```

**Taxonomy note:** Organize products by type/category, then list variants/options inside each type.

### Proactive Morning Check (Cron)

Create `scripts/proactive_stock.py` that sends a Telegram message to the owner
every morning asking for the day's stock:

```python
#!/usr/bin/env python3
import urllib.request, urllib.parse, random, os

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = "YOUR_TELEGRAM_ID"  # Get from @userinfobot

msg = random.choice([
    "Buen dia! Que tienes hoy?",
    "Holaa, que saliste a vender hoy?",
])

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": msg}).encode()
urllib.request.urlopen(urllib.request.Request(url, data=data, method="POST"))
```

Add to crontab:

```bash
# 10:00 AM local time (adjust UTC offset as needed)
0 14 * * * /usr/bin/python3 /home/user/.hermes-mybusiness/scripts/proactive_stock.py
```

The owner replies in Telegram with the stock list, and the bot updates the DB or JSON.
Now when a WhatsApp customer asks "qué tienen?", the bot reads real data.

---

## Privacy Guardrails (Critical)

This agent learns from **real personal messages**. Never commit private data to public repos:

- **NO real names** in examples/templates (use "Owner", "Business Name")
- **NO phone numbers, chat IDs, or API keys** in committed files
- **NO customer conversation exports** in version control (add to `.gitignore`)
- **NO specific product catalogs** with real prices in public examples
- **NO Instagram usernames** in documentation examples

Always use placeholders: `YOUR_TELEGRAM_ID`, `YOUR_BUSINESS_NAME`, `+56XXXXXXXXX`.

### Publishing a Public Repo (Grants, Contests, Open Source)

If you publish this configuration as a public showcase repo (e.g. for a grant or contest), enforce anonymity at the Git level:

```bash
# Enforce anonymous author identity in this repo only
git config user.name "Synero"
git config user.email "synero@yourdomain.cl"

# Commit with explicit author (belt-and-suspenders)
git commit --author="Synero <synero@yourdomain.cl>" -m "..."
```

**Token hygiene for non-interactive push** (if `gh` CLI is unavailable):
```bash
# 1. Temporarily embed token in remote URL
git remote set-url origin https://TOKEN@github.com/USER/REPO.git
git push origin main
# 2. IMMEDIATELY strip it from .git/config
git remote set-url origin https://github.com/USER/REPO.git
```

**Pre-push PII scrub checklist:**
- [ ] Search repo for real names: `grep -ri "your_real_name" . --include="*.md" --include="*.py" --include="*.yaml"`
- [ ] Search for phone numbers: `grep -rE "\+56[0-9]{9}" .`
- [ ] Search for chat IDs: `grep -rE "[0-9]{10}" .`
- [ ] Verify `chat_logs/instagram/` is in `.gitignore`
- [ ] Verify `.env` is in `.gitignore`
- [ ] Run `git log --format="%an <%ae>"` — confirm no real identity leaked in history

---

## Bilingual Documentation Pattern

For Latin American businesses, provide docs in both English and Spanish:

```
README.md           # English (for grants, contests, international visibility)
README_ES.md        # Spanish (for the actual business owner)
docs/
  META_EXPORT_GUIDE.md
  META_EXPORT_GUIDE_ES.md
  ONBOARDING.md
  ONBOARDING_ES.md
```

Cross-link between versions so visitors can switch.

---

### Tone & Honesty in Public Descriptions

**Don't** write startup-pitch language like "losing sales every time she went out" or "every missed message is lost revenue." That sounds like VC demo day.

**Do** write honestly: "We wanted an assistant that actually sounds like her, not a corporate chatbot." Focus on the quality of interaction, not dramatized business impact.

This is especially important for grant/contest applications — reviewers see through exaggerated claims instantly.

### Grant/Contest Evidence Checklist

When submitting to accelerators, grants, or contests, prepare:

1. **GitHub repo link** — public, anonymized, with clear README (see Privacy Guardrails above)
2. **Live logs** — curated `gateway.log` or `whatsapp-bridge.log` showing real customer interactions with response times
3. **System status screenshot** — `systemctl --user status mybusiness-gateway` showing uptime and active state
4. **Architecture diagram** — simple ASCII or SVG showing dual-channel flow
5. **Before/after comparison** (if available) — e.g. "Previously responded in 30 min; now responds in <7 sec"

**Never** submit private customer data, real phone numbers, or unredacted conversation exports as evidence.

---

### WhatsApp (Public)
- `platform_toolsets.whatsapp: []` — no tools, no DB access
- `display.platforms.whatsapp.tool_progress: off` — customers never see tool-call spinners
- No code execution, no file access
- Filter in bridge.js strips tool-call hallucinations and robot phrases
- All messages processed; no allowlist needed for customer-facing bot
- **Slash commands blocked** — customers typing `/new`, `/reset`, etc. cannot trigger Hermes session commands (see `scripts/patch-whatsapp-slash-commands.sh`)

### Telegram (Private Admin)
- Only one chat ID should have admin access
- Full toolset enabled (file, terminal, web, tts, etc.)
- The `system_prompt` should explicitly restrict sensitive commands to the owner
- Consider setting `TELEGRAM_ALLOWED_USERS` env var for hard filtering

---

## Customization Checklist

- [ ] **Business name** — replace in `system_prompt` and `SOUL.md`
- [ ] **Products & prices** — list in `system_prompt`
- [ ] **Owner name** — used in admin-mode instructions
- [ ] **Telegram chat ID** — hardcoded in prompt for admin recognition
- [ ] **Vocabulary** — replace with real examples from `chat_logs/instagram/`
- [ ] **Banned phrases** — add any industry-specific robot language
- [ ] **Model choice** — `minimax-m2.7` via opencode-go is cheap; upgrade to larger model if quality issues persist
- [ ] **TTS voice** — pick from ElevenLabs Voice Library if default "Sarah" doesn't fit
- [ ] **Port numbers** — ensure no conflicts with other Hermes instances
- [ ] **Banking details** — fill `data/datos_pago.json` with real transfer info
- [ ] **Payment options** — customize transfer/cash options for your business
- [ ] **Tool progress hidden** — `display.platforms.whatsapp.tool_progress: off` and `display.platforms.telegram.tool_progress: off` in `config.yaml`
- [ ] **Slash commands blocked** — run `scripts/patch-whatsapp-slash-commands.sh` after installing Hermes Agent
- [ ] **Customer memory** — enable `file` tool on WhatsApp for `data/clientes.json`

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| **Bot not responding to WhatsApp at all** (not even "hola") | Bridge in `manual_mode` — `data/whatsapp-mode.json` contains `{"mode": "manual"}` | Check bridge log for `{"event":"ignored","reason":"manual_mode"}`. Change to `{"mode": "auto"}`. No restart needed. |
| Bridge `disconnected` under gateway systemd | Gateway subprocess bug | Use separate `whatsapp-bridge.service` |
| "No home channel is set for Whatsapp" | Missing `WHATSAPP_HOME_CHANNEL` env var | Add `WHATSAPP_HOME_CHANNEL=dummy` to `.env` |
| Model replies with code/XML tags | minimax tool-call hallucination | Bridge `formatOutgoingMessage` filter strips these; also add explicit ban in prompt |
| "En que puedo ayudarte?" robot Spanish | LLM defaulting to generic assistant tone | Add negative examples in prompt + bridge tone guard |
| **Bot replies "Holii" and ignores the customer's question** | Prompt too passive / over-trained on Instagram friend-chat | Rewrite WhatsApp rules: saludá breve Y respondé la pregunta. Don't leave customers hanging. |
| QR expired during scan | Normal — QR lasts ~30s | Re-run QR generator; only needed once per session wipe |
| Session lost after reboot | `session/` directory missing or corrupted | Ensure `session_path` in config points to persistent dir |
| TTS not generating | `elevenlabs` package missing or API key wrong | `pip install elevenlabs` in Hermes venv; verify key |
| **Bot tells customers file paths, JSON, or "read_file"** | Technical details (file paths, JSON fields, tool names) inside `system_prompt` | Move all technical instructions to a separate `TECHNICAL.md` operator file. Keep `system_prompt` 100% behavior/personality. Use wrapper scripts if the LLM needs file awareness. |
| **Customer typed `/new` and bot reset the session** | WhatsApp messages starting with `/` are interpreted as Hermes slash commands | Run `scripts/patch-whatsapp-slash-commands.sh` to strip leading `/` from all WhatsApp messages before they reach the agent. |
| **Bot tells customers "déjame confirmar con María" or gives a phone number** | System prompt leaks owner identity (e.g. "asistente de María...") | Rewrite prompt: "Eres [Name]. Vendes [product]. No eres asistente de nadie." Add Iron Rules banning "confirmar con", "te paso con", "habla con". |
| **Bot says "Dame un seg" or makes customer wait for fixed data** | Prompt includes insecurity phrases like "déjame confirmar" or missing payment data rules | Ban "dame un seg", "reviso", "confirmo" in prompt. Add payment section with immediate data sharing rule. Store banking details in `data/datos_pago.json`, not in prompt. |
| **Bot quotes wrong prices** | stock.json / prompt prices out of sync with companion app | Move products to Supabase `products` table. Both bot and app read from same DB. Admin updates prices via Telegram → DB → instant sync. |

---

## Architecture Decisions

These are non-obvious design choices that emerged from real deployment experience.

### 1. Framework, Not Instance

**Problem:** The first version was hardcoded for a specific food business. Flavor lists, product taxonomies, delivery logistics — none of this transfers to a hair salon or a SaaS.

**Solution:** Business modes. Each mode is a self-contained package (MODE.md, data-schema.json, prompt-fragments.md) that the setup wizard copies based on user selection. The skill is a **framework** that generates instances.

**Implication:** You can add a new mode by creating one directory with three files. No code changes needed.

### 2. Instagram Clone Is Mode-Agnostic

**Problem:** The user feared the Instagram parser was tied to one business type.

**Reality:** The parser extracts vocabulary ("holii", "okis", "bacán"), emoji patterns, response length, and greeting style — all of which transfer across business types. A SaaS founder's WhatsApp style is just as clonable as a baker's.

**Implementation:** The parser runs BEFORE mode selection in the wizard. The extracted personality profile is merged into the system prompt regardless of mode.

### 3. Technical Details Must Leave the Prompt

**Problem:** The LLM repeated file paths (`~/.hermes-business/data/stock_hoy.json`) and tool names (`read_file`) to customers because they were in the system prompt.

**Lesson:** The LLM cannot distinguish between "instructions for me" and "what I say to the user." If you tell it "read ~/.hermes/data/stock.json", it may literally say that to the customer.

**Solution:** Zero file paths, JSON field names, or tool references in `system_prompt`. All technical operations live in `TECHNICAL.md` (human operator guide) and wrapper scripts (`get_stock.py`, `save_order.py`). The LLM uses tools via its tool-calling capability without needing to know filenames.

### 4. WhatsApp ≠ Instagram DM

**Problem:** Training on Instagram DMs made the bot too passive. It greeted warmly and waited for the customer to lead. On WhatsApp, customers want to buy NOW.

**Real failure:**
```
Customer: "Hola tienes productos??"
Bot:      "Holii"          ← left customer hanging
```

**Solution:** The prompt must explicitly override Instagram passivity for WhatsApp:
- "Si el cliente dice 'Hola + pregunta', saludá BREVE y respondé."
- "NO repitas el saludo si ya saludó antes."
- "Sé directa. La gente compra, no conversa."

### 5. Modes Need Different Payment Patterns

**Retail:** Transfer now OR on delivery. Immediate.
**Services:** Pay on arrival. No deposit needed for most.
**Freelance:** 50% upfront, 50% on delivery. Milestones for big projects.
**SaaS:** Trial → subscription. No "payment" conversation, it's self-service.
**Rentals:** Deposit + rental fee upfront. Refundable deposit psychology matters.
**Events:** Full payment to secure spot. Capacity is perishable.

Each mode's `prompt-fragments.md` encodes these patterns so the bot doesn't offer "transfer on delivery" for a SaaS trial.

### 6. Generic Customer Memory

**Problem:** `clientes.json` with fields like "sabores_favoritos" is useless for a mechanic.

**Solution:** A generic schema with a `preferencias` object:
```json
{
  "telefono": "...",
  "nombre": "...",
  "historial": [...],
  "preferencias": {
    "productos_frecuentes": [...],
    "horario_preferido": "...",
    "ubicacion_habitual": "...",
    "profesional_preferido": "...",
    "notas_adicionales": "..."
  }
}
```
Each mode documents which preference fields it uses. Retail uses `productos_frecuentes`; services uses `profesional_preferido`; events uses `notas_adicionales` for dietary restrictions.

---

## Files in This Skill

| File | Purpose |
|------|---------|
| `templates/config.yaml` | Starter config with dual-platform + TTS section |
| `templates/SOUL.md` | Personality template referencing chat logs |
| `templates/prompt.txt` | Base prompt with real vocabulary examples |
| `templates/datos_pago.json` | Banking details template (admin-only) |
| `templates/clientes.json` | Customer memory schema template |
| `templates/TECHNICAL.md` | Operator-only file with file paths and technical instructions |
| `modes/retail/` | Product-selling businesses (food, clothing, handmade) |
| `modes/services/` | Appointment businesses (salons, clinics, mechanics) |
| `modes/freelance/` | Project professionals (designers, devs, photographers) |
| `modes/saas/` | Software subscriptions (apps, platforms, APIs) |
| `modes/rentals/` | Rental businesses (equipment, cars, properties) |
| `modes/events/` | Experience organizers (tours, classes, retreats) |
| `scripts/parse-instagram-export.py` | Parse Meta HTML export into conversation text files |
| `scripts/parse-instagram-personality.py` | Analyze Meta export and generate `personality_profile.json` |
| `scripts/setup_wizard.py` | **Interactive onboarding** — interviews you and generates mode-specific config |
| `scripts/generate-qr.mjs` | Standalone QR generator for Baileys auth |
| `scripts/proactive_stock.py` | Cron script for daily proactive check via Telegram |
| `scripts/patch-whatsapp-slash-commands.sh` | **Security patch** — blocks customers from triggering Hermes `/` commands via WhatsApp |
| `references/meta-export-guide.md` | How to export Instagram data from Meta Account Center |
| `references/telegram-admin-guide.md` | Admin commands reference for the owner |
| `references/ONBOARDING.md` | How the setup wizard interviews the user |
| `.gitignore` | Prevents accidental commit of private exports and env files |
| `LICENSE` | MIT license |

## Onboarding Approaches

### A. Instagram Clone (Fastest, Most Accurate)
1. Download export from https://accountscenter.meta.com
2. Run `parse-instagram-personality.py` to extract real vocabulary and tone
3. Wizard auto-configures SOUL.md from the profile

### B. Interview Mode (No Export Needed)
1. Run `setup_wizard.py`
2. Answer questions about your business, products, pricing, and voice
3. Wizard generates SOUL.md, stock.json, and config.yaml automatically
4. Test conversation with the agent and refine iteratively

---

## Production Notes

- **Never expose the API server port** publicly without `API_SERVER_KEY`
- **Monitor logs:** `journalctl --user -u mybiz-whatsapp-bridge -f`
- **Backup `session/`** before any major change — losing it means re-scanning QR
- **Credit budgets:** ElevenLabs free tier = ~10k chars/month. TTS auto-trigger only on admin voice messages to preserve credits.
- **Model fallback:** Configure `fallback_providers` in `config.yaml` so the agent stays online if the primary provider fails.

---

## Credits

Built by Synero. Based on real deployment experience with businesses.
