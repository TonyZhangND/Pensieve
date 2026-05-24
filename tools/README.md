# Pensieve Tools

## Telegram Bot

A local Telegram bot that captures URLs, notes, images, and files from your phone and saves them to `raw/inbox/` for later processing by Claude Code.

### Setup

1. **Create a bot** — message [@BotFather](https://t.me/BotFather) on Telegram, send `/newbot`, and follow the prompts. Copy the bot token.

2. **Configure the token** — create a `.env` file in the project root:
   ```
   PENSIEVE_TELEGRAM_TOKEN=your-bot-token-here
   ```

3. **Install dependencies**:
   ```bash
   pip install -r tools/requirements.txt
   ```

4. **Run the bot**:
   ```bash
   python tools/telegram-bot.py
   ```

### Usage

Send anything to your bot on Telegram:
- **URLs** — shared links are saved with the URL extracted
- **Text** — notes, thoughts, quotes
- **Photos** — images are downloaded with captions
- **Documents** — PDFs, files are downloaded
- **Voice memos** — audio is saved for later processing
- **Forwarded messages** — original author is preserved

The bot saves everything to `raw/inbox/`. To process the inbox, open Claude Code and run:

```
/process-inbox
```

### Running as a Background Service (macOS)

To keep the bot running automatically, create a launchd plist at `~/Library/LaunchAgents/com.pensieve.telegram-bot.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.pensieve.telegram-bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/pensieve/tools/telegram-bot.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/pensieve</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/pensieve-telegram.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/pensieve-telegram.err</string>
</dict>
</plist>
```

Then load it:
```bash
launchctl load ~/Library/LaunchAgents/com.pensieve.telegram-bot.plist
```
