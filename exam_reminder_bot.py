import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from datetime import datetime
import pytz

     # Set up logging
logging.basicConfig(
         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
         level=logging.INFO
     )
logger = logging.getLogger(__name__)

     # Bot token
TOKEN = "7646830910:AAGJxb0lBKNliW2lX_fr76SaVbA2vuhQJsw"

     # Fixed exam date and chat ID
EXAM_DATE = "2025-09-12"
CHAT_ID = "7377279897"  # For scheduled reminders only

     # Set timezone
TIMEZONE = pytz.timezone("Asia/Kolkata")

def days_until_exam():
         try:
             exam_date = datetime.strptime(EXAM_DATE, "%Y-%m-%d").replace(tzinfo=TIMEZONE)
             today = datetime.now(TIMEZONE)
             delta = exam_date - today
             return max(0, delta.days)
         except ValueError:
             return None

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
         days_left = days_until_exam()
         logger.info("Sending reminder to chat_id: %s", CHAT_ID)
         if days_left is not None:
             if days_left > 0:
                 await context.bot.send_message(
                     chat_id=CHAT_ID,
                     text=f"Reminder: {days_left} days left until your exam on {EXAM_DATE}!"
                 )
             elif days_left == 0:
                 await context.bot.send_message(
                     chat_id=CHAT_ID,
                     text=f"Today is your exam day on {EXAM_DATE}! All the best!"
                 )
             else:
                 await context.bot.send_message(
                     chat_id=CHAT_ID,
                     text=f"Your exam date {EXAM_DATE} has passed!"
                 )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
         logger.info("Received message from chat_id: %s", update.message.chat_id)
         days_left = days_until_exam()
         if days_left is not None:
             chat_id = update.message.chat_id
             if days_left > 0:
                 await context.bot.send_message(
                     chat_id=chat_id,
                     text=f"You sent: {update.message.text}. Remaining days until your exam on {EXAM_DATE}: {days_left}!"
                 )
             elif days_left == 0:
                 await context.bot.send_message(
                     chat_id=chat_id,
                     text=f"You sent: {update.message.text}. Today is your exam day on {EXAM_DATE}! All the best!"
                 )
             else:
                 await context.bot.send_message(
                     chat_id=chat_id,
                     text=f"You sent: {update.message.text}. Your exam date {EXAM_DATE} has passed!"
                 )

async def main():
         app = ApplicationBuilder().token(TOKEN).build()
         
         # Set webhook (replace with your Render URL)
         WEBHOOK_URL = "https://exam-reminder-bot.onrender.com"  # Update with your actual Render URL
         await app.bot.set_webhook(url=WEBHOOK_URL)
         
         app.job_queue.scheduler.configure(timezone=TIMEZONE)
         
         # Schedule daily reminder at 10 AM
         app.job_queue.run_daily(
             callback=send_reminder,
             time=datetime.now(TIMEZONE).time().replace(hour=15, minute=14, second=0),  # 10 AM
             chat_id=CHAT_ID
         )
         
    # Add message handler for any input from any chat
         app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
         
         # Start the application
         logger.info("Starting bot with webhook: %s", WEBHOOK_URL)
         await app.initialize()
         await app.start()
         
         # Keep the bot running
         try:
             while True:
                 await asyncio.sleep(10)  # Keep alive
                 print(".", end="", flush=True)
         except KeyboardInterrupt:
             logger.info("Shutting down bot...")
             await app.stop()
             await app.shutdown()

if __name__ == "__main__":
         loop = asyncio.new_event_loop()
         asyncio.set_event_loop(loop)
         try:
             loop.run_until_complete(main())
         finally:
             loop.close()