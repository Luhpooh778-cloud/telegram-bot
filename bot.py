import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]


# ---------- MENUS ----------

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📞 Call Support", callback_data="call")],
        [InlineKeyboardButton("📝 Submit Request", callback_data="ticket")],
        [InlineKeyboardButton("📊 Service Status", callback_data="status")],
        [InlineKeyboardButton("👨‍💼 Talk to Agent", callback_data="agent")]
    ]
    return InlineKeyboardMarkup(keyboard)


def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]])


# ---------- COMMANDS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 *Welcome to Our Call Center*\n\nPlease select an option below:",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "call":
        await query.edit_message_text(
            "📞 *Call Support*\n\nYou can reach us at:\n\n☎️ 1-800-555-1234\n\nHours: 9AM – 6PM",
            parse_mode="Markdown",
            reply_markup=back_menu()
        )

    elif query.data == "ticket":
        await query.edit_message_text(
            "📝 *Submit Request*\n\nPlease describe your issue and a support agent will contact you.",
            parse_mode="Markdown",
            reply_markup=back_menu()
        )

    elif query.data == "status":
        await query.edit_message_text(
            "📊 *Service Status*\n\n✅ All systems are currently operational.",
            parse_mode="Markdown",
            reply_markup=back_menu()
        )

    elif query.data == "agent":
        await query.edit_message_text(
            "👨‍💼 *Live Agent*\n\nAn agent will respond shortly.\n\nPlease wait...",
            parse_mode="Markdown",
            reply_markup=back_menu()
        )

    elif query.data == "back":
        await query.edit_message_text(
            "📞 *Main Menu*\n\nChoose an option below:",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )


# ---------- MAIN ----------

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Call center bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
