from .database import Database
import discord
import copy

base_character = {
    "name" : "",
    "total_correct_guesses": 0,
    "total_guesses": 0,
    "total_favorites": 0,
    "total_times_appeared": 0
}

class Characters(Database):
    def __init__(self) -> None:
        super().__init__("score", "characters")

    def get_character(self, char_name) -> dict:
        char_info = next(self.table.find({"name": char_name}))
        return char_info
    
    def create_entry(self, char_name):
        tmp = copy.deepcopy(base_character)
        tmp["name"] = char_name
        self.table.insert_one(tmp)

    def update_times_appeared(self, char_name):
        self.table.update_one(
        {"name": char_name},
        {
            "$inc": {
                "total_times_appeared": 1,
            }
        })

    def update_guesses(self, char_name):
        self.table.update_one(
        {"name": char_name},
        {
            "$inc": {
                f"total_guesses": 1,
            }
        })

    def update_correct_guesses(self, char_name):
        self.table.update_one(
        {"name": char_name},
        {
            "$inc": {
                "total_guesses": 1,
                "total_correct_guesses": 1,
            }
        })

    def update_favorites(self, char_name: str, decrement: bool):
        self.table.update_one(
        {"name": char_name},
        {
            "$inc": {
                f"total_favorites": -1 if decrement else 1,
            }
        })