from src.bot.init_bot import server
from src.bot.settings import fill_list_models
import threading
import os


if __name__ == '__main__':
    print('Contact game bot application')

    threading.Thread(target=fill_list_models).start()

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
