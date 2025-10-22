# ===========================
# 🤖 Gemini + Pollinations Telegram Bot (Railway Fixed Version)
# Author: Irfan x GPT-5
# ===========================

import os
import logging
import requests
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)

# ====== LOGGING ======
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ====== ENV KEYS ======
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not GEMINI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ Missing environment variables (GEMINI_API_KEY or TELEGRAM_BOT_TOKEN)")

# ====== GEMINI ======
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ====== COMMANDS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Welcome to Gemini AI Bot!*\n\n"
        "💬 Send me a message to chat with Gemini.\n"
        "🖼️ Use `/image your prompt` for AI-generated images.\n\n"
        "⚡ Powered by *Gemini* + *Pollinations AI* 🌸",
        parse_mode="Markdown"
    )

# ====== CHAT HANDLER ======
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    chat_id = update.message.chat_id
    await update.message.chat_action(action="typing")

    try:
        response = model.generate_content(msg)
        text = response.text or "⚠️ Gemini returned no text."
    except Exception as e:
        text = f"❌ Error: {e}"

    await context.bot.send_message(chat_id=chat_id, text=text)

# ====== IMAGE HANDLER ======
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("⚡ Use: `/image your prompt`", parse_mode="Markdown")
        return

    await update.message.chat_action(action="upload_photo")

    try:
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
        await update.message.reply_photo(photo=url, caption=f"🖼️ *Prompt:* {prompt}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ====== MAIN ======
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logging.info("✅ Gemini AI Telegram Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
