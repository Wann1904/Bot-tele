from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8881078652:AAEj-804xIW7kZiWA8nQW3yAZBc06O4R9QI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo Wan! Bot berhasil jalan 🚀")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot berjalan...")
app.run_polling()