#!/usr/bin/env python3
"""
Parse Meta/Instagram HTML message export into plain-text conversation files.

Usage:
    python parse_instagram_export.py <inbox_dir> <output_dir> [--business-name 'Your Name']

Output:
    One .txt file per conversation, ready for LLM training context.
"""

import sys
import os
import re
from pathlib import Path
from html.parser import HTMLParser


class MessageParser(HTMLParser):
    """Parse Instagram/Meta HTML message exports.

    Handles the nested div structure where:
    - Sender name is in <h2 class="... _a6-h ...">
    - Text content is in <div class="... _a6-p ..."> with nested inner divs
    - Timestamp is in <div class="... _a6-o ...">
    """

    def __init__(self):
        super().__init__()
        self.messages = []
        self.current_tag = None
        self.in_sender = False
        self.in_text = False
        self.in_time = False
        self.text_depth = 0  # Track nesting depth inside text container
        self.current_sender = None
        self.current_text = None
        self.current_time = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.current_tag = tag
        cls = attrs_dict.get("class", "")

        # Sender: can be h2 or div with _a6-h class
        if "_a6-h" in cls and ("_3-95" in cls or "_2pim" in cls):
            self.in_sender = True
            self.current_sender = None

        # Text container: div with _a6-p class
        elif tag == "div" and "_a6-p" in cls and "_3-95" in cls:
            self.in_text = True
            self.text_depth = 0
            self.current_text = None

        # Track nesting depth inside text container
        elif self.in_text and tag == "div":
            self.text_depth += 1

        # Timestamp: div with _a6-o class
        elif tag == "div" and "_a6-o" in cls and "_3-94" in cls:
            self.in_time = True
            self.current_time = None

    def handle_endtag(self, tag):
        # Sender end
        if self.in_sender and tag in ("h2", "div"):
            self.in_sender = False

        # Text container end: only when the OUTER _a6-p div closes
        elif self.in_text and tag == "div":
            if self.text_depth > 0:
                # Inner div closing — don't exit text mode
                self.text_depth -= 1
            else:
                # The outer _a6-p div is closing — commit the message
                self.in_text = False
                if self.current_sender and self.current_text:
                    text = self.current_text.strip()
                    if text:
                        self.messages.append((
                            self.current_time or "unknown",
                            self.current_sender.strip(),
                            text
                        ))
                self.current_text = None

        # Time end
        elif self.in_time and tag == "div":
            self.in_time = False

    def handle_data(self, data):
        if self.in_sender:
            if self.current_sender is None:
                self.current_sender = data
            else:
                self.current_sender += data
        elif self.in_text:
            if self.current_text is None:
                self.current_text = data
            else:
                self.current_text += data
        elif self.in_time:
            if self.current_time is None:
                self.current_time = data
            else:
                self.current_time += data


def parse_html_file(filepath):
    """Parse a single HTML message file and return list of (time, sender, text) tuples."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    parser = MessageParser()
    parser.feed(content)
    return parser.messages


def process_inbox(inbox_dir, output_dir, business_name_filter=None):
    """Process all conversation directories in the inbox."""
    inbox = Path(inbox_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    total_conversations = 0
    total_messages = 0
    business_messages = 0

    for conv_dir in sorted(inbox.iterdir()):
        if not conv_dir.is_dir():
            continue

        all_messages = []
        for html_file in sorted(conv_dir.glob("message_*.html")):
            msgs = parse_html_file(html_file)
            all_messages.extend(msgs)

        if not all_messages:
            continue

        total_conversations += 1
        total_messages += len(all_messages)

        # Count messages from business account if filter provided
        biz_count = 0
        if business_name_filter:
            filter_lower = business_name_filter.lower()
            biz_count = sum(1 for m in all_messages if filter_lower in m[1].lower())
            business_messages += biz_count

        # Write output
        safe_name = re.sub(r'[^\w\-]', '_', conv_dir.name)
        out_file = out / f"{safe_name}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"# Conversation: {conv_dir.name}\n")
            f.write(f"# Total messages: {len(all_messages)}\n")
            if business_name_filter:
                f.write(f"# Messages from '{business_name_filter}': {biz_count}\n")
            f.write("-" * 50 + "\n\n")
            for time_str, sender, text in all_messages:
                f.write(f"[{time_str}] {sender}: {text}\n\n")

    print(f"Conversations processed: {total_conversations}")
    print(f"Total messages: {total_messages}")
    if business_name_filter:
        print(f"Business account messages: {business_messages}")
    print(f"Files saved to: {out}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python parse_instagram_export.py <inbox_dir> <output_dir> [--business-name 'Your Name']")
        sys.exit(1)

    business_filter = None
    if "--business-name" in sys.argv:
        idx = sys.argv.index("--business-name")
        if idx + 1 < len(sys.argv):
            business_filter = sys.argv[idx + 1]
    elif len(sys.argv) > 3:
        business_filter = sys.argv[3]

    process_inbox(sys.argv[1], sys.argv[2], business_filter)
