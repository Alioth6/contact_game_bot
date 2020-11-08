import src.bot.settings as config
from src.bot.init_bot import db


class Definition(db.Model):
    __tablename__ = 'defs'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String())
    definition = db.Column(db.String())
    guessed = db.Column(db.Boolean())

    def __init__(self, word, definition, guessed):
        self.word = word
        self.definition = definition
        self.guessed = guessed

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'word': self.word,
            'definition': self.definition,
            'guessed': self.guessed
        }


class UserState(db.Model):
    __tablename__ = 'users_state'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String())
    definition = db.Column(db.String())
    gold = db.Column(db.String())
    index = db.Column(db.Integer)
    state = db.Column(db.Integer)

    def __init__(self, id):
        self.id = id
        self.word = ''
        self.definition = ''
        self.gold = ''
        self.index = 0
        self.state = int(config.States.S_ENTER_DEFINITION)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def serialize(self):
        return {
            'id': self.id,
            'word': self.word,
            'definition': self.definition,
            'gold': self.gold,
            'index': self.index,
            'state': config.States(self.state)
        }
