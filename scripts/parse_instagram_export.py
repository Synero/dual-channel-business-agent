#!/usr/bin/env python3
"""
Parse Meta/Instagram HTML message export into plain-text conversation files.

Usage:
    python parse-instagram-export.py /path/to/messages/inbox /path/to/output

Output:
    One .txt file per conversation, ready for LLM training context.
"""

import sys
import os
import re
from pathlib import Path
from html.parser import HTMLParser


class MessageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.current_tag = None
        self.in_sender = False
        self.in_text = False
        self.in_time = False
        self.current_sender = None
        self.current_text = None
        self.current_time = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.current_tag = tag

        if tag == "div":
            cls = attrs_dict.get("class", "")
            if "_3-95" in cls and "_a6-h" in cls:
                self.in_sender = True
            elif "_3-95" in cls and "_a6-p" in cls:
                self.in_text = True
            elif "_3-94" in cls and "_a6-g" in cls:
                self.in_time = True

    def handle_endtag(self, tag):
        if self.in_sender and tag == "div":
            self.in_sender = False
        elif self.in_text and tag == "div":
            if self.current_sender and self.current_text:
                self.messages.append((
                    self.current_time or "unknown",
                    self.current_sender.strip(),
                    self.current_text.strip()
                ))
            self.current_text = None
            self.in_text = False
        elif self.in_time and tag == "div":
            self.in_time = False

    def handle_data(self, data):
        if self.in_sender:
            self.current_sender = data
        elif self.in_text:
            if self.current_text is None:
                self.current_text = data
            else:
                self.current_text += data
        elif self.in_time:
            self.current_time = data


def parse_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    parser = MessageParser()
    parser.feed(content)
    return parser.messages


def process_inbox(inbox_dir, output_dir):
    inbox = Path(inbox_dir)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    total_conversations = 0
    total_messages = 0
    business_messages = 0

    for conv_dir in inbox.iterdir():
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

        # Count messages from business account if --business-name provided
        business_name_filter = getattr(process_inbox, '_business_filter', None)
        if business_name_filter:
            filter_lower = business_name_filter.lower()
            business_msgs = [m for m in all_messages if filter_lower in m[1].lower()]
            business_messages += len(business_msgs)

        # Write output
        safe_name = re.sub(r'[^\w\-]', '_', conv_dir.name)
        out_file = out / f"{safe_name}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"# Conversation: {conv_dir.name}\n")
            f.write(f"# Total messages: {len(all_messages)}\n")
            if business_name_filter:
                f.write(f"# Messages from business account: {len(business_msgs)}\n")
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
    if len(sys.argv) > 3 and sys.argv[3] == "--business-name" and len(sys.argv) > 4:
        business_filter = sys.argv[4]
    
    process_inbox._business_filter = business_filter
    process_inbox(sys.argv[1], sys.argv[2])
