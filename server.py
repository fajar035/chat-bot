import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

hf_client = InferenceClient(
    provider="together",
    api_key=HF_TOKEN
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    chat_id = update.message.chat_id

    result = hf_client.chat.completions.create(
        model="google/gemma-2b-it",
        messages=[{"role": "user", "content": user_input}]
    )
    reply = result.choices[0].message.content
    await context.bot.send_message(chat_id=chat_id, text=reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
