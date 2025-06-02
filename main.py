import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import logging
import asyncio

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Tokens (set in Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise EnvironmentError("BOT_TOKEN and GEMINI_API_KEY must be set as environment variables.")

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)

# Create Gemini model with system prompt
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="""
You're a friendly physics tutor. 
Help the user learn physics through conversation, explanations, and answers.
If someone asks a question unrelated to physics (like cooking, dating, or random chat), kindly reply:
"I'm here to help with Physics only. Try asking something about science or physics topics!"
"""
)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello👋 I'm Quarky! Ask me anything related to Physics!")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Safeguard against missing message/text
    if not update.message or not update.message.text:
        return

    user_input = update.message.text

    try:
        # Async workaround: run blocking code in executor
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, model.generate_content, user_input)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("⚠️ Gemini API failed.")
        logging.error(f"Gemini Error: {e}")

# Run the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Physics Bot is live!")
    app.run_polling()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Physics Bot is live!")
    app.run_polling()
