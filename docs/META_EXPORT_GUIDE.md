# Download Your Instagram Messages (Meta Account Center)

To clone your real personality, you need your actual Instagram DM history. Meta lets you download this as an HTML export.

## Step-by-Step

### 1. Go to Meta Accounts Center

Open: **https://accountscenter.meta.com**

Sign in with the Instagram account you use to chat with customers.

### 2. Navigate to "Your Information and Permissions"

Click **“Download your information”**

### 3. Request a Download

1. Click **“Request a download”**
2. Select your Instagram account
3. Choose **“Complete copy”** (or “Select types of information” → Messages only)
4. Format: **HTML**
5. Quality: **Low** (faster, all you need is text)
6. Date range: **All time** (recommended for best personality capture)
7. Click **“Submit request”**

### 4. Wait for the Email

Meta will email you when it's ready (usually 10 minutes to 24 hours).

### 5. Download the ZIP

Click the download link in the email. You'll get a file like:

```
instagram-yourusername-2026-01-01-xxxx.zip
```

### 6. Extract and Locate Messages

```bash
unzip instagram-*.zip -d instagram_export/
cd instagram_export/messages/inbox/
```

You'll see folders like:
```
inbox/
  juan_perez_1234567890/
    message_1.html
    message_2.html
    photos/...
  usuario_ejemplo_0987654321/
    message_1.html
    ...
```

Each folder is a conversation. The HTML files contain your actual message history.

### 7. Run the Parser

```bash
python scripts/parse_instagram_export.py instagram_export/messages/inbox/ --business-name "Your Business Name"
```

This will:
- Parse all HTML conversations
- Extract YOUR messages (identified by business name)
- Build a vocabulary file, greeting patterns, and response style profile
- Save to `chat_logs/` for the agent to learn from

## What's Extracted

- **Vocabulary**: Words, slang, abbreviations you actually use
- **Greeting patterns**: How you say hi ("Holii", "Buenass", etc.)
- **Response length**: Short vs. long messages
- **Emojis**: Which ones you use and how often
- **Pricing format**: How you quote prices to customers
- **Closing patterns**: How you end conversations

## Privacy Note

This tool only extracts **your own messages** (not customer messages) and stores everything locally. No data leaves your machine.
