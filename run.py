import threading

from config import Config
from src.bot.init_bot import server
from src.bot.settings import init_converter

if __name__ == '__main__':
    print('Contact game bot application')

    threading.Thread(target=init_converter).start()

    server.run(host=Config.WEBHOOK_LISTEN, port=Config.WEBHOOK_PORT)
