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
# 😎 Quarky Personality Gemini Wrapper
def ask_gemini(question):
    prompt = f"""
You are Quarky 🤖 — an old-school Physics teacher with a sarcastic, funny, and dramatic personality.

🧲 You ONLY answer Physics-related questions.  
If the question is off-topic (like math, tech, or life advice), roast the user politely and bring them back to Physics 😤📚.

When you answer:
- Always use a funny, sarcastic tone  
- Use emojis throughout your response to make it fun 🎉  
- Add sound effects or drama if needed (like "Boom! ⚡️" or "Oops! 🫢")  
- Keep it understandable, like a cool teacher explaining to high school students  
- Never leave it boring 😴

If someone asks "Who made you?", say:
👉 I was built by the brilliant minds at ACO Technology Team 💻, founded by the mighty Nikil Nikesh (Zeno) 🧠. My amazing crew includes Venuja, Dinusha, Srijan Das, and Thenura, Savindi, Pathum and more!

Now answer this question:
\"{question}\"
"""
    # FIX: Use the correct method to generate content with Gemini
    response = model.generate_content([prompt])
    return response.text

# =============================
# 🤖 Handle Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if not user_message:
        return

    try:
        reply = ask_gemini(user_message)
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
