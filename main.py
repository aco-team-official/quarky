import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Tokens (set in Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)

# Create Gemini model with system prompt
model = genai.GenerativeModel(
    "gemini-pro",
    system_instruction="""
You are a helpful Physics tutor.
Only answer questions that are clearly about Physics (including classical mechanics, quantum physics, thermodynamics, optics, etc).
If the question is not related to Physics, respond with:
'Sorry, I only answer Physics-related questions. Try asking something about Physics.'
"""
)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello👋 I'm a Quarky! Ask me anything related to Physics!")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        response = model.generate_content(user_input)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("⚠️ Gemini API failed.")
        print(f"Gemini Error: {e}")

# Run the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Physics Bot is live!")
    app.run_polling()
