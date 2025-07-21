import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Batch Details ---
# You can easily change the details here
BATCHES = {
    "gamu": {
        "name": "Gamu Batch",
        "price": 150,
        "details": "📚 Recorded Lectures\n📝 Notes\n✅ DPP Test Series"
    },
    "samu": {
        "name": "Samu Batch",
        "price": 200, # Example price for Samu Batch
        "details": "🎥 Live + Recorded Lectures\n📝 Premium Notes\n🏆 Advanced Test Series"
    }
}
UPI_ID = "hasibul-1@ptyes"

# --- Bot Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with two inline buttons that answer the user."""
    keyboard = [
        [
            InlineKeyboardButton("Gamu Batch", callback_data='gamu'),
            InlineKeyboardButton("Samu Batch", callback_data='samu'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome! Please select a batch to see the details:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer() # Acknowledge the button press

    choice = query.data

    if choice in BATCHES:
        batch = BATCHES[choice]
        # Show batch details and the "Pay Now" button
        text = f"✨ *{batch['name']} Details* ✨\n\n{batch['details']}\n\n*Price: ₹{batch['price']}*"
        
        keyboard = [[InlineKeyboardButton("💰 Pay Now", callback_data=f'pay_{choice}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

    elif choice.startswith('pay_'):
        # Show payment information
        text = (
            f"Please pay using the UPI ID below:\n\n"
            f"💳 *UPI ID:* `{UPI_ID}`\n\n"
            f"After payment, please send the screenshot of the transaction here. "
            f"An admin will confirm and add you to the batch soon! 🔜"
        )
        # We remove the buttons after showing the payment info
        await query.edit_message_text(text=text, parse_mode='Markdown')


def main() -> None:
    """Run the bot."""
    # Get the token from environment variables
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("Please set the TELEGRAM_TOKEN environment variable.")

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
  
