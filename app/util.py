from app.classes.scoreboard import Scoreboard
from app.classes.characters import Characters
import os
import hashlib
salt = os.environ["thsalt"]

def hash_character_name(name):
    salted_name = salt+name    
    return hashlib.md5(salted_name.encode('utf-8')).hexdigest()

scoreboard = Scoreboard()
characters = Characters()