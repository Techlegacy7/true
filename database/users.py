from motor.motor_asyncio import AsyncIOMotorClient


class UserConfig:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db["users"]

    async def get_user(
        self,
        user_id,
    ) -> dict:
        user_id = int(user_id)
        user = await self.col.find_one({"user_id": user_id})
        return user or False

    async def add_user(self, user_id):
        res = {
            "user_id": user_id,
            "banned": False,
        }
        await self.col.insert_one(res)
        return True

    async def update_user_info(self, user_id, value: dict, tag="$set"):
        user_id = int(user_id)
        myquery = {"user_id": user_id}
        newvalues = {tag: value}
        await self.col.update_one(myquery, newvalues)

    async def filter_users(self, dict):
        return self.col.find(dict)

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        return await self.col.find({}).to_list(None)

    async def delete_user(self, user_id):
        await self.col.delete_one({"user_id": int(user_id)})

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def is_user_exist(self, id):
        user = await self.col.find_one({"user_id": int(id)})
        return bool(user)

    async def count_users(self):
        return await self.col.count_documents({})
