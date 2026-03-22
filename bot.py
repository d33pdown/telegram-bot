import os
import random
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

FANVUE_LINK = "https://www.fanvue.com/linavossbaby"

FLIRTY_LINES = [
    "You’re kinda interesting… I like that 💋",
    "Careful… I might get attached 😏",
    "I don’t show everything here… just saying 🔥",
    "You’re making me curious…",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey 💋 I’ve been waiting for you...\n\n"
         "Chat with me here 😏\n"
         "But I don’t show everything here...\n"
         "Only my private page 🔥"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    lowered = user_text.lower()

    try:
        if lowered in ["hi", "hello", "hey"]:
            await update.message.reply_text("Hey you 💋 How’s your night going?")
            return

        if any(word in lowered for word in ["private", "exclusive", "content"]):
            await update.message.reply_text(
                f"I keep the private drop here 🔥\n{FANVUE_LINK}"
            )
            return

        # OpenAI cevabı
        response = client.responses.create(
            model="gpt-5.4",
            input=user_text
        )

        reply_text = response.output_text.strip()

        if not reply_text:
            reply_text = "Tell me what you're looking for 💋"

        # Flirty line ekle
        reply_text += "\n\n" + random.choice(FLIRTY_LINES)

        # Ara sıra link yönlendirmesi
        if random.random() < 0.3:
            reply_text += f"\n\nI posted something you might like 👀\n{FANVUE_LINK}"

        await update.message.reply_text(reply_text)

    except Exception:
        await update.message.reply_text(
            "Hey… something went wrong. Try again in a minute 💋"
        )

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN eksik")
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY eksik")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()