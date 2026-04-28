#!/usr/bin/env python3
"""Parse Meta Instagram HTML exports to extract business personality.

Extracts vocabulary, greetings, response patterns, and pricing style
from YOUR messages in Instagram DM conversations.
"""
import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter


class MessageParser(HTMLParser):
    """Parse Meta's message_*.html files.
    
    Handles the nested div structure where:
    - Sender name is in <h2 class="... _a6-h ..."> (not span)
    - Text content is in <div class="... _a6-p ..."> with nested inner divs
    - Timestamp is in <div class="... _a6-o ...">
    """
    
    def __init__(self, business_name):
        super().__init__()
        self.business_name = business_name.lower()
        self.in_sender = False
        self.in_message = False
        self.current_sender = ""
        self.current_text = ""
        self.messages = []
        self.div_depth = 0
        self.text_depth = 0  # Track nesting inside text container
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")
        
        # Sender: h2 or div with _a6-h class
        if "_a6-h" in cls and ("_3-95" in cls or "_2pim" in cls):
            self.in_sender = True
            self.current_sender = ""
        
        # Text container: div with _a6-p class
        elif tag == "div" and "_a6-p" in cls and "_3-95" in cls:
            self.in_message = True
            self.text_depth = 0
            self.current_text = ""
        
        # Track nesting inside text container
        elif self.in_message and tag == "div":
            self.text_depth += 1
        
        if tag == "div":
            self.div_depth += 1
        
    def handle_endtag(self, tag):
        if tag == "div":
            self.div_depth -= 1
        
        # Sender end
        if self.in_sender and tag in ("h2", "div"):
            self.in_sender = False
        
        # Text container end: only when the OUTER _a6-p div closes
        elif self.in_message and tag == "div":
            if self.text_depth > 0:
                self.text_depth -= 1
            else:
                self.in_message = False
                if self.current_sender.lower() == self.business_name:
                    text = self.current_text.strip()
                    if text:
                        self.messages.append(text)
                self.current_text = ""
                
    def handle_data(self, data):
        if self.in_sender:
            self.current_sender += data.strip()
        elif self.in_message:
            self.current_text += data


def analyze_personality(messages):
    """Extract personality patterns from messages."""
    
    if not messages:
        print("ERROR: No messages found. Check business name.")
        sys.exit(1)
    
    # Basic stats
    total = len(messages)
    avg_len = sum(len(m) for m in messages) / total
    
    # Greetings
    greetings = []
    greeting_words = ["hola", "holii", "holiii", "holi", "buenas", "buen dia", "buenos dias"]
    for m in messages:
        lower = m.lower()
        for g in greeting_words:
            if lower.startswith(g):
                greetings.append(m[:60])
                break
    
    # Confirmations
    confirmations = []
    confirm_words = ["ok", "sis", "bacan", "super", "listo", "dale"]
    for m in messages:
        lower = m.lower()
        for c in confirm_words:
            if c in lower and len(m) < 30:
                confirmations.append(m.strip())
                break
    
    # Price patterns (numbers with $)
    price_pattern = re.compile(r'\$?[\d.]+(?:\s?mil)?', re.IGNORECASE)
    prices = []
    for m in messages:
        found = price_pattern.findall(m)
        prices.extend(found)
    
    # Emoji usage
    emojis = []
    for m in messages:
        for char in m:
            if ord(char) > 127 and not char.isalpha() and not char.isdigit():
                emojis.append(char)
    emoji_counts = Counter(emojis).most_common(10)
    
    # Vocabulary (words used frequently)
    all_words = []
    for m in messages:
        words = re.findall(r'\b[a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1]{3,}\b', m.lower())
        all_words.extend(words)
    vocab = Counter(all_words).most_common(30)
    
    # Response length distribution
    lengths = [len(m) for m in messages]
    short = sum(1 for l in lengths if l < 30)
    medium = sum(1 for l in lengths if 30 <= l < 100)
    long = sum(1 for l in lengths if l >= 100)
    
    return {
        "stats": {
            "total_messages": total,
            "avg_length": round(avg_len, 1),
            "length_distribution": {"short (<30)": short, "medium (30-100)": medium, "long (100+)": long}
        },
        "greetings": list(set(greetings))[:10],
        "confirmations": list(set(confirmations))[:10],
        "prices": list(set(prices))[:10],
        "emojis": [{"char": c, "count": n} for c, n in emoji_counts],
        "top_vocabulary": [{"word": w, "count": n} for w, n in vocab],
        "sample_messages": messages[:20]
    }


def main():
    parser = argparse.ArgumentParser(description="Parse Instagram DM exports for AI personality")
    parser.add_argument("inbox_dir", help="Path to messages/inbox/ folder")
    parser.add_argument("--business-name", required=True, help="Your name/business name as shown in Instagram")
    parser.add_argument("--output", default="personality_profile.json", help="Output JSON file")
    args = parser.parse_args()
    
    inbox = Path(args.inbox_dir)
    if not inbox.exists():
        print(f"ERROR: Directory not found: {inbox}")
        sys.exit(1)
    
    all_messages = []
    conversation_count = 0
    
    # Find all message_*.html files
    for conv_dir in inbox.iterdir():
        if not conv_dir.is_dir():
            continue
        for html_file in conv_dir.glob("message_*.html"):
            parser = MessageParser(args.business_name)
            try:
                with open(html_file, "r", encoding="utf-8") as f:
                    parser.feed(f.read())
                all_messages.extend(parser.messages)
                if parser.messages:
                    conversation_count += 1
            except Exception as e:
                print(f"Warning: Could not parse {html_file}: {e}")
    
    print(f"Parsed {conversation_count} conversations")
    print(f"Found {len(all_messages)} messages from '{args.business_name}'")
    
    # Analyze
    profile = analyze_personality(all_messages)
    
    # Save
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Personality profile saved to {args.output}")
    print(f"\nQuick stats:")
    print(f"  - Total messages: {profile['stats']['total_messages']}")
    print(f"  - Avg length: {profile['stats']['avg_length']} chars")
    print(f"  - Greetings found: {len(profile['greetings'])}")
    print(f"  - Price mentions: {len(profile['prices'])}")
    print(f"  - Top word: {profile['top_vocabulary'][0]['word'] if profile['top_vocabulary'] else 'N/A'}")
    
    # Also save raw messages for training
    chat_logs_dir = Path("chat_logs")
    chat_logs_dir.mkdir(exist_ok=True)
    with open(chat_logs_dir / "instagram_training.txt", "w", encoding="utf-8") as f:
        for msg in all_messages:
            f.write(msg + "\n---\n")
    print(f"  - Raw messages saved to chat_logs/instagram_training.txt")


if __name__ == "__main__":
    main()
