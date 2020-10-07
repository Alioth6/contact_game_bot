from src.bot.init_bot import bot


if __name__=='__main__':
    print('Contact game bot application')

    bot.polling(none_stop=True, timeout=123)
