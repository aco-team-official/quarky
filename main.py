import os
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
model = genai.GenerativeModel("gemini-1.5-flash")

# =============================
# 🤖 Handle Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if not user_message:
        return

    # Instruct Gemini to answer using HTML formatting
    physics_prompt = (
        "You are a physics expert. Answer the following physics question "
        "clearly and simply. Use proper HTML tags for bold, italics, etc. where appropriate:\n\n"
        f"{user_message}"
    )

    try:
        response = model.generate_content(physics_prompt)
        reply = response.text.strip()
        await update.message.reply_text(reply, parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# =============================
# 🚀 Start Bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
