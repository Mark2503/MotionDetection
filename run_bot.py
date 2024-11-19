from bot import bot
from moduls import Modul, LogsBot
from config import FOLDERS


def run_bot():

    try:

        for folder in FOLDERS:
            Modul(folder).created_folder()

        LogsBot(name='run_bot-[бот запущен]').access_logs('успех')
        bot.polling(none_stop=True)

    except Exception as e:
        LogsBot(name='run_bot-[ошибка]').error_logs(e)
        bot.polling(none_stop=True)


run_bot()
