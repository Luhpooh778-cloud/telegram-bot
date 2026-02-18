import os
import uuid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]

# PUT YOUR TELEGRAM NUMERIC ID HERE
ADMIN_ID = 8329734663

tickets = {}  # ticket_id : user_id


# ---------- MENUS ----------

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Submit Support Ticket", callback_data="ticket")],
        [InlineKeyboardButton("👨‍💼 Talk to Agent", callback_data="agent")],
        [InlineKeyboardButton("📊 Service Status", callback_data="status")]
    ])


def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]])


# ---------- START ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 *Welcome to Customer Support*\n\nChoose an option below:",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )


# ---------- BUTTON HANDLER ----------

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ticket":
        await query.edit_message_text(
            "📝 *Submit Your Request*\n\nSend your issue in one message.",
            parse_mode="Markdown"
        )
        context.user_data["ticket_mode"] = True

    elif query.data == "agent":
        await query.edit_message_text(
            "👨‍💼 *Live Agent*\n\nSend your message below. An agent will reply.",
            parse_mode="Markdown"
        )
        context.user_data["agent_mode"] = True

    elif query.data == "status":
        await query.edit_message_text(
            "📊 *System Status*\n\n✅ All systems operational.",
            parse_mode="Markdown",
            reply_markup=back_menu()
        )

    elif query.data == "back":
        await query.edit_message_text(
            "📞 *Main Menu*\n\nChoose an option:",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )


# ---------- MESSAGE HANDLER ----------

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # Ticket System
    if context.user_data.get("ticket_mode"):
        ticket_id = str(uuid.uuid4())[:8]
        tickets[ticket_id] = user_id

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🎫 *NEW SUPPORT TICKET*\n\nTicket ID: `{ticket_id}`\nUser ID: `{user_id}`\n\nMessage:\n{text}",
            parse_mode="Markdown"
        )

        await update.message.reply_text(
            f"✅ Ticket Created!\n\n🎫 Ticket ID: `{ticket_id}`\nAn agent will contact you shortly.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

        context.user_data["ticket_mode"] = False

    # Live Agent Chat
    elif context.user_data.get("agent_mode"):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"💬 *LIVE CHAT*\nUser ID: `{user_id}`\n\n{text}",
            parse_mode="Markdown"
        )

    # Admin Reply Routing
    elif user_id == ADMIN_ID and context.args:
        ticket_id = context.args[0]
        reply_text = " ".join(context.args[1:])

        if ticket_id in tickets:
            await context.bot.send_message(
                chat_id=tickets[ticket_id],
                text=f"👨‍💼 *Support Reply*\n\n{reply_text}",
                parse_mode="Markdown"
            )
            await update.message.reply_text("✅ Reply sent.")
        else:
            await update.message.reply_text("❌ Invalid ticket ID.")


# ---------- ADMIN COMMAND ----------

async def reply_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await message_handler(update, context)


# ---------- MAIN ----------

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply_ticket))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Professional call center bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
