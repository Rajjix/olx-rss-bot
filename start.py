import logging

from telegram.ext import Updater

from telegram_bot.main import RssBot
from telegram_bot.dispatchers import updater, rss_bot

logging.basicConfig(
    format='%(asctime)s - %(name)s = %(levelname)s - %(message)s',
    level=logging.INFO
)

dispatcher = updater.dispatcher.add_handler


if __name__ == '__main__':
    """ Dispatchers """
    dispatcher(rss_bot['start'])
    dispatcher(rss_bot['subscribe'])
    dispatcher(rss_bot['unsubscribe'])

    """ Job that runs every 10 minutes to send the feed. """
    feed = updater.job_queue
    job_minute = feed.run_repeating(
        RssBot.send_rss_feed,
        interval=600,
        first=0
    )

    updater.start_polling()
