from .database import Database
import discord
import copy
from time import time

base_player = {
    "player_id": 0,  # must be set before use
    "score": 0,
    "games_won": 0,
    "guesses": 0,
    "challenge_mode_games_played": 0,
    "challange_mode_games_won": 0,
    "username": "",
    "guessed_characters": {},
    "servers": [],
    "favorite": "",
    "time_last_updated": int(time()),
}


class UserNotFoundError(Exception):
    pass


class Scoreboard(Database):
    def __init__(self) -> None:
        super().__init__("score", "score")

    def add_commas_to_number(self, n):
        n = str(n)
        length = len(n)
        out = ""
        for index, value in enumerate(n):
            out += value
            if (length-index-1) % 3 == 0:
                out += ","
        return out[:-1]

    def get_base_player(self, player_id):
        tmp = copy.deepcopy(base_player)
        tmp["player_id"] = player_id
        return tmp

    def get_player(self, player_id):
        res = self.table.find({"player_id": player_id})
        if res.count() >= 1:
            return res[0]
        else:
            base_player = self.get_base_player(player_id)
            self.table.insert_one(base_player)
            return base_player

    def get_every_player(self):
        out = []
        res = self.table.find()
        for i in range(0,self.table.count()):
            out.append(res[i])
        return out

    def is_in_database(self, player_id):
        res = self.table.find({"player_id": player_id})
        if res.count() >= 1:
            return True

    def return_old_data(self, bot):
        servers = [guild.id for guild in bot.guilds]
        self.table.remove({
            "servers": {
                "$not": {
                    "$in": servers
                }
            },
            "time_last_updated": {
                "$lt": int(time()) - 2_592_000
            }
        })

    def update_attr(self, user: discord.User, attr: str, increment: int) -> None:
        player_id = user.id
        player = self.get_player(player_id)
        self.table.update_one(
            {"player_id": player_id},
            {
                "$inc": {
                    attr: increment,
                }
            })

    def time_last_updated(self, user: discord.User):
        player_id = user.id
        player = self.get_player(player_id)
        self.table.update_one(
            {"player_id": player_id},
            {
                "$set": {
                    "time_last_updated": int(time()),
                }
            })

    def update_character_guessed_count(self, user: discord.User, character_name: str):
        player_id = user.id
        player = self.get_player(player_id)
        self.table.update_one(
            {"player_id": player_id},
            {
                "$inc": {
                    f"guessed_characters.{character_name}": 1,
                }
            })

    def update_username(self, user: discord.User):
        player_id = user.id
        player = self.get_player(player_id)
        self.table.update_one(
            {"player_id": player_id},
            {
                "$set": {
                    "username": user.name,
                }
            })

    def update_serverlist(self, user: discord.User, server_id: int):
        player_id = user.id
        player = self.get_player(player_id)
        self.table.update_one(
            {"player_id": player_id},
            {
                "$addToSet": {
                    "servers": server_id,
                }
            })

    def update_favorite_chracter(self, user: discord.User, favorite: str):
        player_id = user.id
        player = self.get_player(player_id)
        self.table.update_one(
            {"player_id": player_id},
            {
                "$set": {
                    "favorite": favorite,
                }
            })

    def get_player_information(self, user: discord.User) -> dict:
        player_info = self.get_player(user.id)
        return player_info
