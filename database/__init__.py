from .users import UserConfig
from bot.config import Config

class Database:
    def __init__(self, uri, database_name):
        self.users = UserConfig(uri, database_name)


db = Database(Config.DATABASE_URL, Config.DATABASE_NAME)
