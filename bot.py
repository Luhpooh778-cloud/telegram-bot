import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ["8250106450:AAFkzjLhAxihUlKxPhMueaTCOY3xv9njNdM]


# ----- MENU -----

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("📖 Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ Info", callback_data="info"),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)



# ----- COMMAND HANDLERS -----

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Choose an option below 👇",
        reply_markup=main_menu()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        await query.edit_message_text("📖 *Help Menu*\n\nUse the buttons to navigate.", parse_mode="Markdown")

    elif query.data == "info":
        await query.edit_message_text("ℹ️ *Bot Info*\n\nThis is a demo Telegram bot.", parse_mode="Markdown")

    elif query.data == "settings":
        await query.edit_message_text("⚙️ *Settings*\n\nSettings coming soon!", parse_mode="Markdown")


# ----- MAIN -----

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
