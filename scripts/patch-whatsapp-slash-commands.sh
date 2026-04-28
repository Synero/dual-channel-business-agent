#!/usr/bin/env bash
# ============================================================================
# Patch: Block Hermes slash commands from WhatsApp customers
# ============================================================================
# WhatsApp users typing "/new" or "/reset" would trigger Hermes session
# management commands. This patch strips the leading "/" from ALL WhatsApp
# messages before they reach the agent, so "/new" becomes "new" (harmless text).
#
# Run this after installing/upgrading Hermes Agent:
#   bash scripts/patch-whatsapp-slash-commands.sh
# ============================================================================

set -euo pipefail

HERMES_AGENT_DIR="${HERMES_AGENT_DIR:-$HOME/.hermes/hermes-agent}"
TARGET="$HERMES_AGENT_DIR/gateway/platforms/whatsapp.py"

if [[ ! -f "$TARGET" ]]; then
    echo "ERROR: $TARGET not found. Set HERMES_AGENT_DIR to your Hermes install."
    exit 1
fi

# Check if already patched
if grep -q "Strip leading slash so WhatsApp users can't trigger Hermes commands" "$TARGET"; then
    echo "Already patched."
    exit 0
fi

# Apply patch inline — adds a 3-line block right after "body = data.get('body', '')"
python3 << 'PYEOF'
import sys

target = sys.argv[1]
with open(target, 'r') as f:
    content = f.read()

old_block = '''            # For text-readable documents, inject file content directly into
            # the message text so the agent can read it inline.
            # Cap at 100KB to match Telegram/Discord/Slack behaviour.
            body = data.get("body", "")
            if data.get("isGroup"):'''

new_block = '''            # For text-readable documents, inject file content directly into
            # the message text so the agent can read it inline.
            # Cap at 100KB to match Telegram/Discord/Slack behaviour.
            body = data.get("body", "")
            # Strip leading slash so WhatsApp users can't trigger Hermes commands
            if body.startswith("/"):
                body = body[1:]
            if data.get("isGroup"):'''

if old_block not in content:
    print("ERROR: Could not find the target code block to patch.")
    print("Hermes Agent version may have changed. Manual patch required.")
    sys.exit(1)

content = content.replace(old_block, new_block)

with open(target, 'w') as f:
    f.write(content)

print("PATCHED: $TARGET")
print("WhatsApp slash commands are now blocked.")
PYEOF
"$TARGET"

echo "Done. Restart your gateway for changes to take effect:"
echo "  systemctl --user restart <your-gateway-service>"
