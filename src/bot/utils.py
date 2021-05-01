from flask import jsonify

import src.bot.settings as conf
from src.bot.init_bot import db
from src.db.models import Definition
from src.db.models import UserState


def set_user_data(chat_id, data):
    """
    Записываем юзера в игроки и запоминаем, что он должен ответить.
    Либо обновляем информацию.
    """
    try:
        user_state = UserState.query.filter_by(id=chat_id).first()
        if user_state is not None:
            user_state.update(**data)
            db.session.commit()
        else:
            new_user = UserState(
                id=chat_id
            )
            new_user.update(**data)
            db.session.add(new_user)
            db.session.commit()
    except Exception as e:
        print(str(e))


def get_user_data(chat_id):
    """
    Получаем правильный ответ для текущего юзера.
    В случае, если человек просто ввёл какие-то символы, не начав игру, возвращаем None
    """
    try:
        user_state = UserState.query.filter_by(id=chat_id).first()
        return user_state.serialize()
    except KeyError:
        return None


def set_user_state(chat_id, state):
    """
    Указываем позицию хода игрока.
    """
    try:
        user_state = UserState.query.filter_by(id=chat_id).first()
        user_state.state = int(state)
        db.session.commit()
    except AttributeError as e:
        print(str(e))


def get_user_state(chat_id):
    try:
        user_state = UserState.query.filter_by(id=chat_id).first()
        return conf.States(user_state.state)
    except AttributeError:
        return None


def finish_user_game(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    """
    try:
        UserState.query.filter_by(id=chat_id).delete()
    except Exception as e:
        print(str(e))


def add_definition(word, definition, guessed):
    try:
        new_def = Definition(
            word=word,
            definition=definition,
            guessed=guessed
        )
        db.session.add(new_def)
        db.session.commit()
        print("Def added. Def id={}".format(new_def.id))
    except Exception as e:
        print(str(e))


def get_all_defs():
    try:
        defs = Definition.query.all()
        return jsonify([e.serialize() for e in defs])
    except Exception as e:
        return str(e)
