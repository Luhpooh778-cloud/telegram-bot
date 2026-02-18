import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from twilio.rest import Client

# --- Environment variables ---
BOT_TOKEN = os.environ["BOT_TOKEN"]
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]

# --- Twilio client ---
twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

# --- Bot menus ---
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📞 Call a Number", callback_data="call_number")]
    ])

def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]])

# --- /start command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to the Call Agent Bot!\n\nUse the menu below to initiate a call.",
        reply_markup=main_menu()
    )

# --- Button handler ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "call_number":
        await query.edit_message_text(
            "📞 Send me the phone number you want me to call (format: +1234567890)",
        )
        context.user_data["awaiting_number"] = True

    elif query.data == "back":
        await query.edit_message_text(
            "🤖 Main Menu",
            reply_markup=main_menu()
        )

# --- Message handler ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Check if user just pressed "Call a Number"
    if context.user_data.get("awaiting_number"):
        phone_number = user_message.strip()
        try:
            call = twilio_client.calls.create(
                twiml=f'<Response><Say voice="alice">Hello! This is your automated call from the bot.</Say></Response>',
                to=phone_number,
                from_=TWILIO_NUMBER
            )
            await update.message.reply_text(
                f"✅ Call initiated to {phone_number}!\nCall SID: {call.sid}",
                reply_markup=main_menu()
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to make call: {e}", reply_markup=main_menu())
        finally:
            context.user_data["awaiting_number"] = False
    else:
        await update.message.reply_text("Please use the menu to initiate a call.", reply_markup=main_menu())

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"\+?\d+"), message_handler))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(MessageHandler(filters.ALL, message_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Call Agent Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
