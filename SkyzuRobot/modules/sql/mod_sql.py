import threading

from sqlalchemy import Column, String, Integer

from SungJinwooRobot.modules.sql import BASE, SESSION


class Mods(BASE):
    __tablename__ = "mod"
    chat_id = Column(String(14), primary_key=True)
    user_id = Column(Integer, primary_key=True)

    def __init__(self, chat_id, user_id):
        self.chat_id = str(chat_id)  # ensure string
        self.user_id = user_id

    def __repr__(self):
        return "<Mod %s>" % self.user_id


Mods.__table__.create(checkfirst=True)

MOD_INSERTION_LOCK = threading.RLock()


def mod(chat_id, user_id):
    with MOD_INSERTION_LOCK:
        mod_user = Mods(str(chat_id), user_id)
        SESSION.add(mod_user)
        SESSION.commit()


def is_modd(chat_id, user_id):
    try:
        return SESSION.query(Mods).get((str(chat_id), user_id))
    finally:
        SESSION.close()


def dismod(chat_id, user_id):
    with MOD_INSERTION_LOCK:
        dismod_user = SESSION.query(Mods).get((str(chat_id), user_id))
        if dismod_user:
            SESSION.delete(dismod_user)
            SESSION.commit()
            return True
        else:
            SESSION.close()
            return False


def list_modd(chat_id):
    try:
        return (
            SESSION.query(Mods)
            .filter(Mods.chat_id == str(chat_id))
            .order_by(Mods.user_id.asc())
            .all()
        )
    finally:
        SESSION.close()
