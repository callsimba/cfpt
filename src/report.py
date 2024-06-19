import logging
import telepot

# Set up logging
logging.basicConfig(filename='activity.log', level=logging.INFO, format='%(asctime)s %(message)s')

def log_activity(message):
    logging.info(message)

def send_report_to_telegram(bot_token, chat_id, message):
    bot = telepot.Bot(bot_token)
    bot.sendMessage(chat_id, message)
