from src.bot.init_bot import server
import os


if __name__=='__main__':
    print('Contact game bot application')

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
