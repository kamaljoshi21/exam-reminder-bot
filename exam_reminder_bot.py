import asyncio
import logging
import os
from telegram.ext import ApplicationBuilder, ContextTypes
from datetime import datetime, timedelta
import pytz
import random

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
CHAT_ID = "7377279897"  # Your confirmed chat ID

# Set timezone
TIMEZONE = pytz.timezone("Asia/Kolkata")

# Emojis list for variety
EMOJIS = ["🎉", "📅", "⏰", "📚", "🚀", "🌟", "💡", "🏁", "🎓", "🔔", "💪", "✨", "🌈", "🌟", "🎯", "⌛", "📝", "🌞", "🌙", "❤️"]

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
        emoji1, emoji2 = random.sample(EMOJIS, 2)
        style = random.randint(1, 50)
        message = ""
        if style == 1:
            message = f"{emoji1} Hey Kamal! 🎉 Only {days_left} days until your exam on {EXAM_DATE}! Keep shining! {emoji2}"
        elif style == 2:
            message = f"{emoji1} 🚀 Blast off! {days_left} days to your exam {EXAM_DATE}! Study hard! {emoji2}"
        elif style == 3:
            message = f"{emoji1} 📅 Countdown: {days_left} days left for {EXAM_DATE}! You’ve got this! {emoji2}"
        elif style == 4:
            message = f"{emoji1} ⏰ Time’s ticking! {days_left} days to go for {EXAM_DATE}! Focus up! {emoji2}"
        elif style == 5:
            message = f"{emoji1} 📚 Knowledge time! {days_left} days until {EXAM_DATE}! Let’s go! {emoji2}"
        elif style == 6:
            message = f"{emoji1} 🌟 Star student! {days_left} days to your exam {EXAM_DATE}! Shine bright! {emoji2}"
        elif style == 7:
            message = f"{emoji1} 💡 Idea alert! {days_left} days left for {EXAM_DATE}! Keep learning! {emoji2}"
        elif style == 8:
            message = f"{emoji1} 🏁 Race is on! {days_left} days to {EXAM_DATE}! Run to success! {emoji2}"
        elif style == 9:
            message = f"{emoji1} 🎓 Grad vibes! {days_left} days until your exam {EXAM_DATE}! Prepare well! {emoji2}"
        elif style == 10:
            message = f"{emoji1} 🔔 Ding ding! {days_left} days to go for {EXAM_DATE}! Stay alert! {emoji2}"
        elif style == 11:
            message = f"{emoji1} 💪 Power up! {days_left} days left for {EXAM_DATE}! You’re strong! {emoji2}"
        elif style == 12:
            message = f"{emoji1} ✨ Magic moment! {days_left} days to your exam {EXAM_DATE}! Keep the magic! {emoji2}"
        elif style == 13:
            message = f"{emoji1} 🌈 Rainbow goals! {days_left} days until {EXAM_DATE}! Chase them! {emoji2}"
        elif style == 14:
            message = f"{emoji1} 🌟 Twinkle twinkle! {days_left} days to go for {EXAM_DATE}! Shine on! {emoji2}"
        elif style == 15:
            message = f"{emoji1} 🎯 Target locked! {days_left} days left for {EXAM_DATE}! Hit it! {emoji2}"
        elif style == 16:
            message = f"{emoji1} ⌛ Sand runs low! {days_left} days to your exam {EXAM_DATE}! Hurry up! {emoji2}"
        elif style == 17:
            message = f"{emoji1} 📝 Notes time! {days_left} days until {EXAM_DATE}! Write your success! {emoji2}"
        elif style == 18:
            message = f"{emoji1} 🌞 Sunny day! {days_left} days to go for {EXAM_DATE}! Brighten your study! {emoji2}"
        elif style == 19:
            message = f"{emoji1} 🌙 Night owl! {days_left} days left for {EXAM_DATE}! Burn the midnight oil! {emoji2}"
        elif style == 20:
            message = f"{emoji1} ❤️ Love your goals! {days_left} days to {EXAM_DATE}! Passion drives you! {emoji2}"
        elif style == 21:
            message = f"{emoji1} 🎉 Party prep! {days_left} days until your exam {EXAM_DATE}! Study first! {emoji2}"
        elif style == 22:
            message = f"{emoji1} 🚀 Rocket launch! {days_left} days to go for {EXAM_DATE}! Blast off! {emoji2}"
        elif style == 23:
            message = f"{emoji1} 📅 Calendar check! {days_left} days left for {EXAM_DATE}! Mark it! {emoji2}"
        elif style == 24:
            message = f"{emoji1} ⏰ Wake-up call! {days_left} days to your exam {EXAM_DATE}! Rise! {emoji2}"
        elif style == 25:
            message = f"{emoji1} 📚 Library vibes! {days_left} days until {EXAM_DATE}! Dive in! {emoji2}"
        elif style == 26:
            message = f"{emoji1} 🌟 Star power! {days_left} days to go for {EXAM_DATE}! Glow up! {emoji2}"
        elif style == 27:
            message = f"{emoji1} 💡 Bright idea! {days_left} days left for {EXAM_DATE}! Think big! {emoji2}"
        elif style == 28:
            message = f"{emoji1} 🏁 Finish line! {days_left} days to {EXAM_DATE}! Sprint now! {emoji2}"
        elif style == 29:
            message = f"{emoji1} 🎓 Cap ready! {days_left} days until your exam {EXAM_DATE}! Prepare! {emoji2}"
        elif style == 30:
            message = f"{emoji1} 🔔 Bell rings! {days_left} days to go for {EXAM_DATE}! Listen up! {emoji2}"
        elif style == 31:
            message = f"{emoji1} 💪 Muscle up! {days_left} days left for {EXAM_DATE}! Strengthen your mind! {emoji2}"
        elif style == 32:
            message = f"{emoji1} ✨ Sparkle time! {days_left} days to your exam {EXAM_DATE}! Shine! {emoji2}"
        elif style == 33:
            message = f"{emoji1} 🌈 Colorful days! {days_left} days until {EXAM_DATE}! Paint your success! {emoji2}"
        elif style == 34:
            message = f"{emoji1} 🌟 Stellar effort! {days_left} days to go for {EXAM_DATE}! Keep it up! {emoji2}"
        elif style == 35:
            message = f"{emoji1} 🎯 Bullseye! {days_left} days left for {EXAM_DATE}! Aim high! {emoji2}"
        elif style == 36:
            message = f"{emoji1} ⌛ Clock’s ticking! {days_left} days to your exam {EXAM_DATE}! Hurry! {emoji2}"
        elif style == 37:
            message = f"{emoji1} 📝 Scribble success! {days_left} days until {EXAM_DATE}! Write it! {emoji2}"
        elif style == 38:
            message = f"{emoji1} 🌞 Sun shines! {days_left} days to go for {EXAM_DATE}! Bright study! {emoji2}"
        elif style == 39:
            message = f"{emoji1} 🌙 Moonlight study! {days_left} days left for {EXAM_DATE}! Night power! {emoji2}"
        elif style == 40:
            message = f"{emoji1} ❤️ Heart of gold! {days_left} days to {EXAM_DATE}! Love your work! {emoji2}"
        elif style == 41:
            message = f"{emoji1} 🎉 Celebration soon! {days_left} days until your exam {EXAM_DATE}! Earn it! {emoji2}"
        elif style == 42:
            message = f"{emoji1} 🚀 Space journey! {days_left} days to go for {EXAM_DATE}! Explore knowledge! {emoji2}"
        elif style == 43:
            message = f"{emoji1} 📅 Date marked! {days_left} days left for {EXAM_DATE}! Ready? {emoji2}"
        elif style == 44:
            message = f"{emoji1} ⏰ Wake-up call! {days_left} days to your exam {EXAM_DATE}! Rise! {emoji2}"
        elif style == 45:
            message = f"{emoji1} 📚 Library vibes! {days_left} days until {EXAM_DATE}! Dive deep! {emoji2}"
        elif style == 46:
            message = f"{emoji1} 🌟 Starry night! {days_left} days to go for {EXAM_DATE}! Twinkle! {emoji2}"
        elif style == 47:
            message = f"{emoji1} 💡 Light the way! {days_left} days left for {EXAM_DATE}! Illuminate! {emoji2}"
        elif style == 48:
            message = f"{emoji1} 🏁 Victory ahead! {days_left} days to {EXAM_DATE}! Charge up! {emoji2}"
        elif style == 49:
            message = f"{emoji1} 🎓 Degree dreams! {days_left} days until your exam {EXAM_DATE}! Chase it! {emoji2}"
        elif style == 50:
            message = f"{emoji1} 🔔 Final bell! {days_left} days to go for {EXAM_DATE}! Ring it in! {emoji2}"

        await context.bot.send_message(chat_id=CHAT_ID, text=message)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Set webhook (confirmed Render URL)
    WEBHOOK_URL = "https://exam-reminder-bot.onrender.com"
    await app.bot.set_webhook(url=WEBHOOK_URL)
    
    app.job_queue.scheduler.configure(timezone=TIMEZONE)
    
    # Schedule daily reminder at 10 AM
    app.job_queue.run_daily(
        callback=send_reminder,
        time=datetime.now(TIMEZONE).time().replace(hour=8, minute=0, second=0),  # 10 AM IST
        chat_id=CHAT_ID
    )
    
    # Start the application
    logger.info("Starting bot with webhook: %s", WEBHOOK_URL)
    port = int(os.getenv("PORT", 10000))  # Render default port
    logger.info("Listening on port: %d", port)
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