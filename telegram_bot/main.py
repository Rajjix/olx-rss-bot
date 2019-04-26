import time

from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

from olx_parser.parser import OlxRssParser
from db.user_db import UserDB


db = UserDB()
db.setup()

Feed = OlxRssParser()

SUB = '🔔 Subsscribe'
UNSUB = '🚫 Unsubscribe'

s_keyboard = [[SUB],[UNSUB]]


class RssBot:

    def start(bot, update, user_data):
        num_key = ReplyKeyboardMarkup(s_keyboard, resize_keyboard=True)
        try:
            db.create_member(update.effective_chat.id)
            bot.send_message(
                chat_id=update.effective_chat.id,
                text='🚀 Welcome to Olx Rss Bot!! 🚀',
                reply_markup=num_key)
        except:
            uname = update.effective_chat.username
            bot.send_message(
                parse_mode='HTML',
                chat_id=update.effective_chat.id,
                text=f'🚀 <b>Welcome back {uname}!!</b>',
                reply_markup=num_key)

    def add_member(bot, update, user_data):
        users = db.get_subs()
        chat_id = update.effective_chat.id
        if chat_id in users:
            bot.send_message(
                chat_id=update.effective_chat.id,
                text="You're already subscribed to the feed!! 🤦‍♂️")
        else:
            db.subscribe(chat_id)
            bot.send_message(
                chat_id=update.effective_chat.id,
                text='Successfully subscribed to the feed 👍.\n😍 We will send you updates every 10 minutes!!!')

    def del_member(bot, update, user_data):
        chat_id = update.effective_chat.id
        db.unsubscribe(chat_id)
        bot.send_message(
            chat_id=update.effective_chat.id,
            text='No more feedback for you!!')
    
    def send_rss_feed(bot, job):
        users = db.get_subs()
        new_items = Feed.get_items()
        items = [x+'\n'+new_items[x]['link'] for x in new_items.keys()]
        items = ('\n ――――――――――――\n\n').join(items)
        if items == []:
            for uid in users:
                bot.send_message(chat_id=uid, text="No Updates")
        else:
            for uid in users:
                for item in new_items:
                    try:
                        iphoto = new_items[item]['preview']
                        ilink = new_items[item]['link']
                        itile = item
                        capp = item + '\n' + ilink
                        bot.sendPhoto(chat_id=uid, photo=iphoto, caption=capp)
                        time.sleep(0.5)
                    except:
                        message = item + '\n ――――――――――――\n' +new_items[item]['link']
                        bot.send_message(chat_id=uid, text=item)
                        time.sleep(0.5)
