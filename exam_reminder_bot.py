import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import json
import os
import pytz

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = "7646830910:AAGJxb0lBKNliW2lX_fr76SaVbA2vuhQJsw"

# File to store exam date
DATA_FILE = "exam_reminder_data.json"

# Set timezone (change to your timezone if needed, e.g., 'US/Pacific', 'Europe/London')
TIMEZONE = pytz.timezone("Asia/Kolkata")

# Helper functions
def save_exam_date(date_str, chat_id):
    data = {"exam_date": date_str, "chat_id": chat_id}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_exam_date():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return None

def days_until_exam(exam_date_str):
    try:
        # Create an offset-naive datetime and localize it to TIMEZONE
        exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").replace(tzinfo=TIMEZONE)
        today = datetime.now(TIMEZONE)
        delta = exam_date - today
        return max(0, delta.days)
    except ValueError:
        return None

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /start command from chat_id: %s", update.message.chat_id)
    await update.message.reply_text(
        "Welcome to @Dailyexamreminder! Use /setexam <YYYY-MM-DD> to set your exam date.\n"
        "Example: /setexam 2025-12-31\n"
        "I'll remind you daily how many days are left!"
    )

async def set_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    logger.info("Received /setexam command from chat_id: %s with args: %s", chat_id, context.args)
    args = context.args
    if not args or len(args) != 1:
        await update.message.reply_text("Please provide the exam date in YYYY-MM-DD format.\nExample: /setexam 2025-12-31")
        return
    date_str = args[0]
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        save_exam_date(date_str, chat_id)
        logger.info("Exam date set to %s for chat_id: %s", date_str, chat_id)
        await update.message.reply_text(f"Exam date set to {date_str}. You'll get daily reminders!")
        
        # Schedule daily reminders (e.g., 3 PM)
        context.job_queue.run_daily(
            callback=send_reminder,
            time=datetime.now(TIMEZONE).time().replace(hour=15, minute=0, second=0),  # 3 PM
            chat_id=chat_id
        )
    except ValueError:
        await update.message.reply_text("Invalid date format. Use YYYY-MM-DD.\nExample: /setexam 2025-12-31")

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    logger.info("Sending reminder to chat_id: %s", chat_id)
    data = load_exam_date()
    if data and data["chat_id"] == chat_id:
        days_left = days_until_exam(data["exam_date"])
        if days_left is not None:
            if days_left > 0:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"Reminder: {days_left} days left until your exam!"
                )
            elif days_left == 0:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Today is your exam day! All the best!"
                )
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Your exam date has passed!"
                )

# Main function
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Explicitly set the timezone for the JobQueue scheduler
    app.job_queue.scheduler.configure(timezone=TIMEZONE)
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setexam", set_exam))
    
    # Check for existing exam date and schedule reminder (e.g., 3 PM)
    data = load_exam_date()
    if data:
        app.job_queue.run_daily(
            callback=send_reminder,
            time=datetime.now(TIMEZONE).time().replace(hour=13, minute=20, second=0),  # 3 PM
            chat_id=data["chat_id"]
        )
    
    # Start polling
    logger.info("Starting bot polling with token: %s", TOKEN[:10] + "..."[:-10])
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Keep the bot running until interrupted
    try:
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour to keep the loop alive
    except KeyboardInterrupt:
        # Graceful shutdown on interrupt
        logger.info("Shutting down bot...")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    # Create a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()