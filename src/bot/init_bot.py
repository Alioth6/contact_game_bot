from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from telebot import types

from config import Config

server = Flask(__name__)

server.config.from_object(Config)
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

from src.bot.bot_logic import bot
from src.bot import utils as db_utils


@server.route("/getdefs")
def get_all():
    return db_utils.get_all_defs()


@server.route('/' + Config.TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    webhook_url = ''.join([
        Config.WEBHOOK_HOST,
        '/',
        Config.TOKEN
    ])
    bot.set_webhook(url=webhook_url)
    return "!", 200
