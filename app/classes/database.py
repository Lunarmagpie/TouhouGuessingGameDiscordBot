from pymongo import MongoClient
import os

URL = f"mongodb+srv://admin:{os.environ['thpassword']}@cluster0.sbdwo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


class Database():
    def __init__(self, database, table) -> None:
        self.client = MongoClient(URL)
        self.db = self.client[database]
        self.table = self.db[table]
