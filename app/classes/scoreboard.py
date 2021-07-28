from .database import Database
import discord

class UserNotFoundError(Exception):
    pass

class Scoreboard(Database):
    def __init__(self) -> None:
        super().__init__("score", "score")
    
    def add_to_player_score(self,user: discord.User,score: int) -> None:
        """
        Adds to a user scores and increments games won by one
        """
        player_id = int(user.id)

        res = self.table.find({"player_id":player_id})

        if res.count() >= 1:
            player = res[0]
            print(player)
            self.update_player_score(player_id,score+player["score"],player["games_won"]+1)
        else:
            self.create_new_player_with_score(player_id,score)

    def create_new_player_with_score(self,player_id,score):
        self.table.insert_one({
            "player_id" : player_id,
            "score" : score,
            "games_won" : 1,
        })
    
    def update_player_score(self,player_id,score,games_won):
        self.table.update_one(
        {"player_id":player_id},
        {
            "$set":{
                "player_id" : player_id,
                "score" : score,
                "games_won" : games_won,
            }
        })

    def get_player_information(self, user: discord.User):
        player_info = self.table.find_one({
            "player_id": user.id
        })

        if player_info is None:
            raise UserNotFoundError

        return player_info