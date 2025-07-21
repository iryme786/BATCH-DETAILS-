import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Admin Telegram username (without @)
ADMIN_USERNAME = "zerofraction"

# UPI ID
UPI_ID = "hasibul-1@ptyes"

# Batch details
BATCH_DETAILS = """
Batch details:
- Recorded lectures (480p/720p)
- Notes
- DPP (with solution)
- Test series (with solution)
"""

async def start(update: Update, context: Application.Context) -> None:
    """Sends a message with inline keyboards for batch selection."""
    keyboard = [
        [
            InlineKeyboardButton("LAKSHAYA HS 2026", callback_data='select_lakshaya'),
            InlineKeyboardButton("PRAYAS WBJEE 2026", callback_data='select_prayas')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please select a batch:', reply_markup=reply_markup)

async def button(update: Update, context: Application.Context) -> None:
    """Handles callback queries from inline keyboard buttons."""
    query = update.callback_query
    await query.answer()

    if query.data == 'select_lakshaya':
        price = "150 Rs"
        batch_name = "LAKSHAYA HS 2026"
    elif query.data == 'select_prayas':
        price = "250 Rs"
        batch_name = "PRAYAS WBJEE 2026"
    elif query.data == 'pay_now':
        await query.edit_message_text(
            f"Please pay to the following UPI ID:\n\n"
            f"💰 UPI ID: `{UPI_ID}`\n\n"
            f"After payment, please send a screenshot to @{ADMIN_USERNAME} here. "
            f"After confirmation, admin will add you soon 🔜"
        )
        return # Exit to prevent further processing if pay_now

    # If a batch was selected, show details and pay button
    if query.data in ['select_lakshaya', 'select_prayas']:
        keyboard = [
            [InlineKeyboardButton("Pay Now", callback_data='pay_now')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"You selected: *{batch_name}*\n\n"
            f"Subscription price: *{price}*\n\n"
            f"{BATCH_DETAILS}\n"
            f"Click 'Pay Now' to proceed with payment.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def echo(update: Update, context: Application.Context) -> None:
    """Echos any message a user sends that isn't a command or callback."""
    # This is optional, but good for debugging or if you want to respond to general messages
    await update.message.reply_text("I'm a bot designed to help you select batches. Please use the /start command to begin.")

def main() -> None:
    """Starts the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    # Add a message handler for all other messages (optional)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    print("Bot is polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
