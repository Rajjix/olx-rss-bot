from telegram.ext import Updater
from telegram.ext import CommandHandler, RegexHandler

from .main import RssBot

updater = Updater(token="XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

rss_bot = {
    'subscribe'  : RegexHandler('🔔 Subsscribe', RssBot.add_member, pass_user_data=True),
    'unsubscribe': RegexHandler('🚫 Unsubscribe', RssBot.del_member, pass_user_data=True),
    'start'      : CommandHandler('start', RssBot.start, pass_user_data=True),
    }
