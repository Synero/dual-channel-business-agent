#!/usr/bin/env python3
"""Interactive setup wizard for Dual Channel Business Agent.

The agent interviews you to configure your business personality,
products/services, channels, and operational rules — adapted to your
business mode (retail, services, freelance, saas, rentals, events).
"""
import json
import os
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent

MODES = {
    "retail": {
        "name": "Retail — Product Sales",
        "description": "You sell physical products: food, clothing, handmade goods, etc.",
        "examples": "Food vendors, bakeries, clothing stores, flower shops, bookstores",
        "customer_says": "Quiero 2 de X y 1 de Y",
        "item_label": "products",
        "item_name": "product",
        "has_stock": True,
        "has_delivery": True,
        "has_appointments": False,
    },
    "services": {
        "name": "Services — Appointments",
        "description": "You book time slots: haircuts, massages, medical, classes.",
        "examples": "Salons, barbershops, clinics, mechanics, tutors, gyms",
        "customer_says": "Tienen hora para mañana?",
        "item_label": "services",
        "item_name": "service",
        "has_stock": False,
        "has_delivery": False,
        "has_appointments": True,
    },
    "freelance": {
        "name": "Freelance — Projects",
        "description": "You work on custom projects: design, development, photography.",
        "examples": "Designers, developers, photographers, writers, architects",
        "customer_says": "Cuánto me cobras por un logo?",
        "item_label": "services",
        "item_name": "service",
        "has_stock": False,
        "has_delivery": False,
        "has_appointments": False,
    },
    "saas": {
        "name": "SaaS — Software Subscriptions",
        "description": "You sell software access: apps, platforms, APIs, tools.",
        "examples": "CRM tools, project management apps, hosting, courses",
        "customer_says": "Quiero ver la posibilidad de una demo",
        "item_label": "plans",
        "item_name": "plan",
        "has_stock": False,
        "has_delivery": False,
        "has_appointments": True,
    },
    "rentals": {
        "name": "Rentals — Equipment & Properties",
        "description": "You rent items for a period: cameras, cars, homes, gear.",
        "examples": "Camera rentals, car rentals, vacation homes, party supplies",
        "customer_says": "Tienen disponible del 15 al 20?",
        "item_label": "items",
        "item_name": "item",
        "has_stock": True,
        "has_delivery": False,
        "has_appointments": False,
    },
    "events": {
        "name": "Events — Experiences",
        "description": "You organize experiences: tours, classes, retreats, workshops.",
        "examples": "Food tours, yoga retreats, cooking classes, concerts",
        "customer_says": "Quiero inscribirme al sábado",
        "item_label": "events",
        "item_name": "event",
        "has_stock": True,
        "has_delivery": False,
        "has_appointments": True,
    },
}


def ask(question, default=None, required=True):
    """Ask a question and return the answer."""
    prompt = f"\n💬 {question}"
    if default:
        prompt += f" [{default}]"
    prompt += "\n> "
    while True:
        answer = input(prompt).strip()
        if answer:
            return answer
        if default is not None:
            return default
        if not required:
            return ""
        print("  (Required)")


def ask_bool(question, default=True):
    """Ask yes/no."""
    suffix = " [Y/n]" if default else " [y/N]"
    answer = input(f"\n💬 {question}{suffix}\n> ").strip().lower()
    if not answer:
        return default
    return answer in ["y", "yes", "s", "si", "sí"]


def ask_list(question):
    """Ask for a comma-separated list."""
    answer = ask(question)
    return [item.strip() for item in answer.split(",") if item.strip()]


def phase_mode():
    """Phase 0: Choose business mode."""
    print("\n" + "=" * 60)
    print("PHASE 0: CHOOSE YOUR BUSINESS MODE")
    print("=" * 60)
    print("\nWhich mode matches your business?\n")

    for i, (key, info) in enumerate(MODES.items(), 1):
        print(f"  {i}. {info['name']}")
        print(f"     {info['description']}")
        print(f"     Eg: {info['examples']}")
        print()

    while True:
        choice = ask("Enter number (1-6) or mode name")
        # Map number to mode key
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(MODES):
                mode_key = list(MODES.keys())[idx]
                break
        # Map name to mode key
        mode_key = choice.lower().strip()
        if mode_key in MODES:
            break
        print("  Invalid choice. Try again.")

    mode_info = MODES[mode_key]
    print(f"\n  ✅ Selected: {mode_info['name']}")
    print(f"     Your customers typically say: \"{mode_info['customer_says']}\"")
    return mode_key, mode_info


def phase_business_basics(mode_info):
    print("\n" + "=" * 60)
    print("PHASE 1: BUSINESS BASICS")
    print("=" * 60)

    return {
        "business_name": ask("What's your business name?"),
        "owner_name": ask("What's YOUR name? (how customers know you)"),
        "bot_name": ask("What should the bot call itself? (e.g. same as business name)",
                        default=ask.__defaults__[0] if False else None) or ask("What's your business name?"),
        "currency": ask("What currency symbol?", default="$"),
        "mode": mode_info,
    }


def phase_items(mode_info):
    print("\n" + "=" * 60)
    print(f"PHASE 2: YOUR {mode_info['item_label'].upper()}")
    print("=" * 60)

    items = ask_list(f"What {mode_info['item_label']} do you offer? (comma-separated)")

    pricing = {}
    print(f"\nEnter price for each {mode_info['item_name']} (or '0' if variable/ask):")
    for item in items:
        price = ask(f"  {item}", default="0")
        pricing[item] = price

    return {"items": items, "pricing": pricing}


def phase_voice():
    print("\n" + "=" * 60)
    print("PHASE 3: YOUR VOICE & STYLE")
    print("=" * 60)

    print("\nHow do you greet customers? Examples: 'Holii', 'Buenass', 'Hola!'")
    greetings = ask_list("Your greetings (comma-separated)")

    print("\nHow do you confirm things? Examples: 'Okis', 'Sis', 'Bacan', 'Listo'")
    confirmations = ask_list("Your confirmations (comma-separated)")

    print("\nHow do you say thank you? Examples: 'Graciasss', 'Uwu', 'Gracias!'")
    thanks = ask_list("Your thank-you phrases (comma-separated)")

    print("\nHow do you apologize for delays? Examples: 'Sorry recien vi', 'Perdon!'")
    apologies = ask_list("Your delay apologies (comma-separated)")

    tone = ask("Tone: casual (amigo) or formal (usted)?", default="casual")
    uses_emojis = ask_bool("Do you use emojis?")

    return {
        "greetings": greetings,
        "confirmations": confirmations,
        "thanks": thanks,
        "apologies": apologies,
        "tone": tone,
        "uses_emojis": uses_emojis,
    }


def phase_channels():
    print("\n" + "=" * 60)
    print("PHASE 4: CHANNEL SETUP")
    print("=" * 60)

    print("\nWhatsApp Business number (with country code, e.g. +569****5678):")
    whatsapp = ask("WhatsApp number")

    print("\nYour Telegram user ID for admin access (ask @userinfobot):")
    telegram_id = ask("Telegram ID")

    print("\nWhat time should the agent do its daily check? (24h format)")
    check_time = ask("Daily check time", default="10:00")

    return {
        "whatsapp_number": whatsapp,
        "telegram_admin_id": telegram_id,
        "daily_check_time": check_time,
    }


def phase_instagram_clone():
    print("\n" + "=" * 60)
    print("PHASE 5: INSTAGRAM CLONE (Optional but Recommended)")
    print("=" * 60)

    has_export = ask_bool("Do you have an Instagram/Meta message export?")

    if not has_export:
        print("\n  ⚠️  Skipping Instagram clone.")
        print("  You can run the parser later:")
        print("  python scripts/parse_instagram_export.py <inbox_dir> --business-name '<you>'")
        return {"has_export": False}

    print("\n  ℹ️  See references/META_EXPORT_GUIDE.md if you need help downloading.")

    export_path = ask("Path to your messages/inbox/ folder")
    business_name = ask("Your exact name as shown in Instagram chats")

    print("\n  🔄 Running parser...")
    import subprocess
    result = subprocess.run([
        sys.executable, str(SKILL_DIR / "scripts/parse_instagram_export.py"),
        export_path,
        "--business-name", business_name,
        "--output", "personality_profile.json"
    ], capture_output=True, text=True)

    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return {"has_export": False}

    return {"has_export": True, "profile": "personality_profile.json"}


def generate_config(mode_key, mode_info, config_data):
    """Generate Hermes Agent config files."""

    output_dir = Path("generated_config")
    output_dir.mkdir(exist_ok=True)
    data_dir = output_dir / "data"
    data_dir.mkdir(exist_ok=True)

    # Save full config
    with open(output_dir / "business_config.json", "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)

    # Copy mode-specific data schema as template
    schema_src = SKILL_DIR / "modes" / mode_key / "data-schema.json"
    if schema_src.exists():
        # Create empty data files based on schema
        with open(schema_src, "r", encoding="utf-8") as f:
            schema = json.load(f)
        for key, info in schema.items():
            filename = info.get("file", f"data/{key}.json").replace("data/", "")
            filepath = data_dir / filename
            # Extract empty array/object structure
            empty_data = extract_empty_schema(info.get("schema", {}))
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(empty_data, f, indent=2, ensure_ascii=False)

    # Generate SOUL.md
    voice = config_data["voice"]
    items = config_data["items"]["items"]
    pricing = config_data["items"]["pricing"]

    soul = f"""# SOUL — {config_data['business']['business_name']}

## Identity
You are {config_data['business']['bot_name']}, running {config_data['business']['business_name']}.

## Mode
{mode_info['name']}

## Vocabulary
- Greetings: {', '.join(voice['greetings'][:5])}
- Confirmations: {', '.join(voice['confirmations'][:5])}
- Thanks: {', '.join(voice['thanks'][:3])}
- Apologies: {', '.join(voice['apologies'][:3])}
- Tone: {voice['tone']}
- Emojis: {'Yes' if voice['uses_emojis'] else 'No'}

## {mode_info['item_label'].title()}
"""
    for item in items:
        price = pricing.get(item, "?")
        soul += f"- {item}: {config_data['business']['currency']}{price}\n"

    with open(output_dir / "SOUL.md", "w", encoding="utf-8") as f:
        f.write(soul)

    # Generate datos_pago.json template
    datos_pago = {
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
    with open(data_dir / "datos_pago.json", "w", encoding="utf-8") as f:
        json.dump(datos_pago, f, indent=2, ensure_ascii=False)

    # Copy mode prompt fragments
    fragments_src = SKILL_DIR / "modes" / mode_key / "prompt-fragments.md"
    if fragments_src.exists():
        shutil.copy(fragments_src, output_dir / "prompt-fragments.md")

    return output_dir


def extract_empty_schema(schema):
    """Extract empty structure from schema for template files."""
    result = {}
    for key, value in schema.items():
        if key.endswith("s") and isinstance(value, list):
            # It's likely an array of objects
            result[key] = []
        elif isinstance(value, dict):
            result[key] = extract_empty_schema(value)
        elif key == "fecha":
            result[key] = "YYYY-MM-DD"
        elif key == "actualizado_por":
            result[key] = ""
        elif key == "notas":
            result[key] = ""
        elif key == "dias_cerrados":
            result[key] = []
        else:
            result[key] = ""
    return result


def main():
    print("""
╔════════════════════════════════════════════════╗
║  Dual Channel Business Agent - Setup Wizard              ║
║  Clone your personality. Deploy your AI.                 ║
╚════════════════════════════════════════════════╝
    """)

    # Run phases
    mode_key, mode_info = phase_mode()
    business = phase_business_basics(mode_info)
    items = phase_items(mode_info)
    voice = phase_voice()
    channels = phase_channels()
    instagram = phase_instagram_clone()

    config = {
        "business": business,
        "items": items,
        "voice": voice,
        "channels": channels,
        "instagram_clone": instagram,
    }

    # Generate files
    print("\n" + "=" * 60)
    print("GENERATING CONFIG FILES...")
    print("=" * 60)

    output_dir = generate_config(mode_key, mode_info, config)

    print(f"\n✅ Setup complete for **{mode_info['name']}**!")
    print(f"\nFiles generated in ./{output_dir}/")
    print("  - business_config.json  (full configuration)")
    print("  - SOUL.md               (personality document)")
    print("  - data/                 (mode-specific data files)")
    print("  - prompt-fragments.md   (mode-specific LLM instructions)")

    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print(f"""
1. Copy generated_config/SOUL.md to your Hermes Agent directory
2. Copy templates/config.yaml and customize with your API keys
3. Use prompt-fragments.md to build your system_prompt
4. Fill data/datos_pago.json with your real banking details
5. Set up the WhatsApp bridge (see README)
6. Test: Send yourself a WhatsApp message!

Need help? Read references/ONBOARDING.md
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled. Run again when ready.")
        sys.exit(0)
