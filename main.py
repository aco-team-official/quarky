import os
import re
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# =============================
# 🔐 Your Tokens
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# =============================
# ⚡️ Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# =============================
# 🧼 Markdown Fixer
def clean_markdown(text):
    return re.sub(r'([_*[\]()~`>#+=|{}.!-])', r'\\\1', text)

# =============================
# 🤖 Handle Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # 🚫 Filter out non-text
    if not user_message:
        return

    # 📚 Force Physics context
    physics_prompt = f"You are a physics expert. Answer the following physics question clearly and simply:\n\n{user_message}"

    try:
        response = model.generate_content(physics_prompt)
        reply = response.text.strip()

        # ✅ Clean for Telegram
        safe_reply = clean_markdown(reply)
        await update.message.reply_text(safe_reply, parse_mode="MarkdownV2")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# =============================
# 🚀 Start Bot
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Physics Bot is live!")
    app.run_polling()
