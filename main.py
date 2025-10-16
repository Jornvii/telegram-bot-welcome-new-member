import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes
from telegram.constants import ParseMode
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Configuration from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
YOUTUBE_LINK = os.getenv("YOUTUBE_LINK")
TWITTER_LINK = os.getenv("TWITTER_LINK")
INSTAGRAM_LINK = os.getenv("INSTAGRAM_LINK")
WEBSITE_LINK = os.getenv("WEBSITE_LINK")

# Welcome message template - Customize as needed
WELCOME_MESSAGE = """
🎉 **សូមស្វាគមន៍មកកាន់ក្រុមបង {name}!** 🎉


📌 **Please take a moment to:**
• Read our group rules
• Introduce yourself  
• Be respectful to all members

💬 Feel free to ask questions and engage with the community!

👇Connect with us:
"""


async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome new members when they join the group"""
    result = update.chat_member
    
    # Check if this is a new member joining
    if result.new_chat_member.status == "member" and result.old_chat_member.status in ["left", "kicked"]:
        user = result.new_chat_member.user
        
        # Get user's display name
        user_name = user.first_name if user.first_name else "friend"
        if user.last_name:
            user_name += f" {user.last_name}"
        
        # Format welcome message with user's name
        welcome_text = WELCOME_MESSAGE.format(name=user_name)
        
        # Create inline keyboard with social media buttons
        keyboard = []
        
        # Add social media links (only if they exist in .env)
        if YOUTUBE_LINK:
            keyboard.append([InlineKeyboardButton("📺 YouTube", url=YOUTUBE_LINK)])
        if TWITTER_LINK:
            keyboard.append([InlineKeyboardButton("📘 Facebook", url=TWITTER_LINK)])
        if INSTAGRAM_LINK:
            keyboard.append([InlineKeyboardButton("📷 Instagram", url=INSTAGRAM_LINK)])
        if WEBSITE_LINK and WEBSITE_LINK != "https://yourwebsite.com":
            keyboard.append([InlineKeyboardButton("🌐 Website", url=WEBSITE_LINK)])
        
        # Add contact admin button
        if ADMIN_USERNAME:
            keyboard.append([InlineKeyboardButton("👤 Contact Admin | ទាក់ទងអ្នកគ្រប់គ្រង", url=f"https://t.me/{ADMIN_USERNAME}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send welcome message
        try:
            await context.bot.send_message(
                chat_id=result.chat.id,
                text=welcome_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            logger.info(f"✅ Welcomed new member: {user_name} (ID: {user.id}) in chat {result.chat.id}")
        except Exception as e:
            logger.error(f"❌ Error sending welcome message: {e}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    start_text = """
👋 សួស្តី! ខ្ញុំជាបូតស្វាគមន៍!
👋 Hello! I'm a welcome bot! New members will automatically receive welcome messages

Bot: {bot_username}
Admin: @{admin}
    """.format(
        bot_username=BOT_USERNAME if BOT_USERNAME else "N/A",
        admin=ADMIN_USERNAME if ADMIN_USERNAME else "N/A"
    )
    await update.message.reply_text(start_text, parse_mode=ParseMode.MARKDOWN)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
ℹ️ **Welcome Bot Help | ជំនួយបូតស្វាគមន៍**

**Commands | ពាក្យបញ្ជា:**
/start - ចាប់ផ្តើម bot
/help - បង្ហាញជំនួយ 
/test - សាក

**Note:** i just here to welcome our new members.

📬 Contact Admin: @{admin}
    """.format(admin=ADMIN_USERNAME if ADMIN_USERNAME else "N/A")
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test welcome message"""
    if update.message.chat.type in ["group", "supergroup"]:
        user = update.message.from_user
        user_name = user.first_name if user.first_name else "friend"
        if user.last_name:
            user_name += f" {user.last_name}"
        
        welcome_text = WELCOME_MESSAGE.format(name=user_name)
        
        keyboard = []
        if YOUTUBE_LINK:
            keyboard.append([InlineKeyboardButton("📺 YouTube", url=YOUTUBE_LINK)])
        if TWITTER_LINK:
            keyboard.append([InlineKeyboardButton("📘 Facebook", url=TWITTER_LINK)])
        if INSTAGRAM_LINK:
            keyboard.append([InlineKeyboardButton("📷 Instagram", url=INSTAGRAM_LINK)])
        if WEBSITE_LINK and WEBSITE_LINK != "https://yourwebsite.com":
            keyboard.append([InlineKeyboardButton("🌐 Website", url=WEBSITE_LINK)])
        if ADMIN_USERNAME:
            keyboard.append([InlineKeyboardButton("👤 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("⚠️ This command only works in groups!")

# print check bot status when bot starts ........................................................................

# async def post_init(application: Application) -> None:
#     """Post initialization - runs after bot starts"""
#     logger.info("=" * 50)
#     logger.info("🤖 Welcome Bot Started Successfully!")
#     logger.info(f"📱 Bot Username: {BOT_USERNAME if BOT_USERNAME else 'Not set'}")
#     logger.info(f"👤 Admin: @{ADMIN_USERNAME if ADMIN_USERNAME else 'Not set'}")
#     logger.info(f"💬 Group Chat ID: {GROUP_CHAT_ID if GROUP_CHAT_ID else 'Not set'}")
#     logger.info("=" * 50)


def main():
    """Start the bot"""
    # Check if BOT_TOKEN is set
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not found in .env file!")
        return
    
    try:
        # Create application with post_init
        app = (
            Application.builder()
            .token(BOT_TOKEN)
            # .post_init(post_init)
            .build()
        )
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("test", test_command))
        
        # Add chat member handler for welcoming new members
        app.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))
        
        # Start the bot with polling
        logger.info("🚀 Starting bot polling...")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        raise


if __name__ == "__main__":
    main()