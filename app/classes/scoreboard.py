from .database import Database
import discord
import copy

base_player = {
    "player_id" : 0, #must be set before use
    "score" : 0,
    "games_won" : 0,
    "guesses" : 0,
    "challenge_mode_games_played" : 0,
    "challange_mode_games_won" : 0,
    "username" : "",
    "guessed_characters" : {},
    "servers" : []
}

class UserNotFoundError(Exception):
    pass

class Scoreboard(Database):
    def __init__(self) -> None:
        super().__init__("score", "score")

    def get_base_player(self,player_id):
        tmp = copy.deepcopy(base_player)
        tmp["player_id"] = player_id
        return tmp

    def get_player(self,player_id):
        res = self.table.find({"player_id":player_id})
        if res.count() >= 1:
            return res[0]
        else:
            base_player = self.get_base_player(player_id)
            self.table.insert_one(base_player)
            return base_player

    def is_in_database(self,player_id):
        res = self.table.find({"player_id":player_id})
        if res.count() >= 1:
            return True

    def update_attr(self,user: discord.User,attr: str, increment: int) -> None:
        player_id = user.id
        player = self.get_player(player_id)
        self.table.update_one(
        {"player_id":player_id},
        {
            "$inc":{
                attr : increment,
            }
        })

    def update_character_guessed_count(self,user: discord.User,character_name: str):
        player_id = user.id
        player = self.get_player(player_id)
        self.table.update_one(
        {"player_id":player_id},
        {
            "$inc":{
                f"guessed_characters.{character_name}" : 1,
            }
        })

    def update_username(self,user: discord.User):
        player_id = user.id
        player = self.get_player(player_id)
        self.table.update_one(
        {"player_id":player_id},
        {
            "$set":{
                f"username" : user.name,
            }
        })

    def update_serverlist(self, user: discord.User, server_id: int):
        player_id = user.id
        player = self.get_player(player_id)
        self.table.update_one(
        {"player_id":player_id},
        {
            "$addToSet":{
                f"servers" : server_id,
            }
        })

    def get_player_information(self, user: discord.User) -> dict:
        player_info = self.get_player(user.id)
        return player_info
