import os
import re
import logging
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

load_dotenv(Path(__file__).parent.parent / ".env")

INBOX_DIR = Path(__file__).parent.parent / "raw" / "inbox"
TOKEN = os.environ["PENSIEVE_TELEGRAM_TOKEN"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pensieve-telegram")


def slugify(text: str, max_len: int = 50) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].rstrip("-") or "untitled"


def timestamp_prefix() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s\)\"'>]+", text)


def save_file(name: str, content: str) -> Path:
    path = INBOX_DIR / name
    path.write_text(content, encoding="utf-8")
    return path


def build_frontmatter(msg_type: str, extra: dict | None = None) -> str:
    lines = [
        "---",
        "source: telegram",
        f"timestamp: {datetime.now(timezone.utc).isoformat()}",
        f"message_type: {msg_type}",
    ]
    for k, v in (extra or {}).items():
        lines.append(f'{k}: "{v}"')
    lines.append("---")
    return "\n".join(lines)


async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    urls = extract_urls(text)
    msg_type = "url" if urls else "text"
    slug = slugify(urls[0].split("//")[1] if urls else text[:60])
    prefix = timestamp_prefix()

    extra = {}
    if urls:
        extra["original_url"] = urls[0]

    fm = build_frontmatter(msg_type, extra)
    save_file(f"{prefix}-{slug}.md", f"{fm}\n\n{text}\n")

    await update.message.reply_text(f"Saved to inbox. ({msg_type})")
    logger.info("Saved %s: %s", msg_type, slug)


async def handle_photo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await ctx.bot.get_file(photo.file_id)
    prefix = timestamp_prefix()
    caption = update.message.caption or "photo"
    slug = slugify(caption[:60])

    ext = Path(file.file_path).suffix or ".jpg"
    media_name = f"{prefix}-{slug}{ext}"
    await file.download_to_drive(INBOX_DIR / media_name)

    fm = build_frontmatter("photo", {"file": media_name})
    body = caption if caption != "photo" else ""
    save_file(f"{prefix}-{slug}.md", f"{fm}\n\n{body}\n")

    await update.message.reply_text("Saved photo to inbox.")
    logger.info("Saved photo: %s", slug)


async def handle_document(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    file = await ctx.bot.get_file(doc.file_id)
    prefix = timestamp_prefix()
    original_name = doc.file_name or "document"
    slug = slugify(Path(original_name).stem)

    ext = Path(original_name).suffix or ""
    media_name = f"{prefix}-{slug}{ext}"
    await file.download_to_drive(INBOX_DIR / media_name)

    caption = update.message.caption or ""
    fm = build_frontmatter("document", {"file": media_name, "original_filename": original_name})
    save_file(f"{prefix}-{slug}.md", f"{fm}\n\n{caption}\n")

    await update.message.reply_text(f"Saved document to inbox. ({original_name})")
    logger.info("Saved document: %s", original_name)


async def handle_voice(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    file = await ctx.bot.get_file(voice.file_id)
    prefix = timestamp_prefix()
    slug = "voice-memo"

    media_name = f"{prefix}-{slug}.ogg"
    await file.download_to_drive(INBOX_DIR / media_name)

    fm = build_frontmatter("voice", {"file": media_name, "duration_seconds": str(voice.duration)})
    save_file(f"{prefix}-{slug}.md", f"{fm}\n\n")

    await update.message.reply_text("Saved voice memo to inbox.")
    logger.info("Saved voice memo: %ds", voice.duration)


async def handle_forward(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or update.message.caption or ""
    prefix = timestamp_prefix()
    slug = slugify(text[:60]) if text else "forward"

    extra = {}
    if update.message.forward_from:
        extra["forwarded_from"] = update.message.forward_from.username or str(update.message.forward_from.id)
    elif update.message.forward_sender_name:
        extra["forwarded_from"] = update.message.forward_sender_name

    fm = build_frontmatter("forward", extra)
    save_file(f"{prefix}-{slug}.md", f"{fm}\n\n{text}\n")

    await update.message.reply_text("Saved forwarded message to inbox.")
    logger.info("Saved forward: %s", slug)


def main():
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.FORWARDED, handle_forward))
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.FORWARDED, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL & ~filters.FORWARDED, handle_document))
    app.add_handler(MessageHandler(filters.VOICE & ~filters.FORWARDED, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.FORWARDED, handle_text))

    logger.info("Pensieve Telegram bot started. Saving to %s", INBOX_DIR)
    app.run_polling()


if __name__ == "__main__":
    main()
