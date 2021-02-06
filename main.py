from telegram.ext.handler import Handler
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from instaloader import Instaloader, Profile, Post
import re
import telegram
import os
import logging

L = Instaloader()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


welcome_msg = '''<b>Welcome To the Bot</b>
<i>Send instagram username to get DP</i>
Bot is for Education Purpose only. Don't Misuse'''

help_keyboard = [[InlineKeyboardButton("Join Channel", url="https://t.me/helpingbots"),
                  InlineKeyboardButton("Support Channel", url="https://t.me/helpingbots")]]
help_reply_markup = InlineKeyboardMarkup(help_keyboard)


def start(update, context):
    context.bot.send_chat_action(
        chat_id=update.message.chat_id, action="typing")
    user = update.message.from_user
    channel_member = context.bot.get_chat_member(
        os.environ.get("CHANNEL_ID"), user_id=update.message.chat_id)
    status = channel_member["status"]
    if(status == 'left'):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"Hi {user.first_name}, to use me you have to be a member of the updates channel in order to stay updated with the latest developments.\nPlease click below button to join and /start the bot again.", reply_markup=help_reply_markup)
        return
    else:
        update.message.reply_html(welcome_msg)


def contact(update, context):
    keyboard = [[InlineKeyboardButton(
        "Contact", url="https://github.com/varundeva/instagram-tools-telegram-bot/")], ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Nothing Much. Code Availble on Github', reply_markup=reply_markup)


def about(update, context):
    pass


def help(update, context):
    pass


def dp(update, context):
    user = update.message.from_user
    channel_member = context.bot.get_chat_member(
        os.environ.get("CHANNEL_ID"), user_id=update.message.chat_id)
    status = channel_member["status"]
    if(status == 'left'):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"Hi {user.first_name}, to use me you have to be a member of the updates channel in order to stay updated with the latest developments.\nPlease click below button to join and /start the bot again.", reply_markup=help_reply_markup)
        return
    else:
        # Get username/string from the message
        query = update.message.text
        originalQuery = query
        # To Check given username starts from '/'
        if query[0] == "/":
            update.message.reply_text(
                "Username Should Not Start from '/'\nEnter a Valid Instagram User Name")
            return
        # To check given username starts from '@' if it's true then remove the @ from beginning
        if query[0] == '@':
            query = query[1:]
        # To check given username in url format. if its true extract username from url
        if "instagram.com" in query:
            splittedUrl = re.split(r'[/?]', query)
            query = splittedUrl[3]
        msg = update.message.reply_text("Downloading...")
        chat_id = update.message.chat_id
        try:
            user = Profile.from_username(L.context, query)
            caption_msg = f'''*Name*: {user.full_name}'''
            context.bot.send_photo(
                chat_id=chat_id, photo=user.profile_pic_url,
                caption=caption_msg, parse_mode='MARKDOWN')
            context.bot.delete_message(chat_id, msg.message_id)
            thnk_msg = '''Thank you for using bot \nShare bot with your friends and have fun'''
            context.bot.send_message(chat_id, thnk_msg, 'HTML')

        except Exception:
            msg.edit_text(
                f'''Something Went Wrong..\nMaybe Username {originalQuery}  not Available..''')


def acc_type(val):
    if(val):
        return "Private"
    else:
        return "Public"


def info(update, context):
    query = update.message.text[6:]
    context.bot.send_chat_action(
        chat_id=update.message.chat_id, action="typing")
    try:
        user = Profile.from_username(L.context, query)
        infoMsg = f'''
<b>Account Information</b>
Name - {user.full_name}
UserName - {user.username}
Bio  - {user.biography}
Bio Url - {user.external_url}
Followers - {user.followers}
Following - {user.followees}
Posts - {user.mediacount}
IGTV Videos - {user.igtvcount}
Account Type - {acc_type(user.is_private)}
    '''
        update.message.reply_photo(
            photo=user.profile_pic_url, caption=infoMsg, parse_mode='HTML')
    except:
        update.message.reply_text(
            f'''Something Went Wrong..\nMaybe Username {query}  not Available..''')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(
        token=os.environ.get("BOT_TOKEN"), use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))
    dispatcher = updater.dispatcher
    logger.info("Setting Up MessageHandler")
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("contact", contact))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("about", about))
    dispatcher.add_handler(MessageHandler(Filters.text, dp))
    dispatcher.add_handler(CommandHandler("info", info))

    # log all errors
    dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=PORT,
                          url_path=os.environ.get("BOT_TOKEN"))
    updater.bot.set_webhook(
        os.environ.get("HOST_NAME") + os.environ.get("BOT_TOKEN"))
    logging.info("Starting Long Polling!")
    updater.idle()


if __name__ == "__main__":
    main()
