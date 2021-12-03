import os
import hashlib
from contextlib import suppress

from pincer.commands import command as _command

from app.classes.scoreboard import Scoreboard
from app.classes.characters import Characters
salt = os.environ["thsalt"]


def hash_character_name(name):
    salted_name = salt+name
    return hashlib.md5(salted_name.encode('utf-8')).hexdigest()


scoreboard = Scoreboard()
characters = Characters()


def command(*args, **kwargs):

    with suppress(KeyError):
        guild = os.environ["guild"]
        return _command(*args, **kwargs, guild=guild)

    return _command(*args, **kwargs)
