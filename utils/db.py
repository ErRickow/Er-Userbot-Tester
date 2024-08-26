import re
import json
import threading
import sqlite3
from dns import resolver
import pymongo
from utils import config

resolver.default_resolver = resolver.Resolver(configure=False)
resolver.default_resolver.nameservers = ["1.1.1.1"]


class Database:
    def get(self, module: str, variable: str, default=None):
        """Get value from database"""
        raise NotImplementedError

    def set(self, module: str, variable: str, value):
        """Set key in database"""
        raise NotImplementedError

    def remove(self, module: str, variable: str):
        """Remove key from database"""
        raise NotImplementedError

    def get_collection(self, module: str) -> dict:
        """Get database for selected module"""
        raise NotImplementedError

    def close(self):
        """Close the database"""
        raise NotImplementedError

    def get_datetime(self) -> str:
        return datetime.datetime.now().strftime("%d/%m/%Y - %H:%M")

    async def set_env(self, name: str, value: str) -> None:
        await self.env.update_one(
            {"name": name}, {"$set": {"value": value}}, upsert=True
        )

    async def get_env(self, name: str) -> str | None:
        if await self.is_env(name):
            data = await self.env.find_one({"name": name})
            return data["value"]
        return None

    async def rm_env(self, name: str) -> None:
        await self.env.delete_one({"name": name})

    async def is_env(self, name: str) -> bool:
        if await self.env.find_one({"name": name}):
            return True
        return False

    async def get_all_env(self) -> list:
        return [i async for i in self.env.find({})]

    async def is_stan(self, client: int, user_id: int) -> bool:
        if await self.stan_users.find_one({"client": client, "user_id": user_id}):
            return True
        return False

    async def add_stan(self, client: int, user_id: int) -> bool:
        if await self.is_stan(client, user_id):
            return False
        await self.stan_users.insert_one(
            {"client": client, "user_id": user_id, "date": self.get_datetime()}
        )
        return True

    async def rm_stan(self, client: int, user_id: int) -> bool:
        if not await self.is_stan(client, user_id):
            return False
        await self.stan_users.delete_one({"client": client, "user_id": user_id})
        return True

    async def get_stans(self, client: int) -> list:
        return [i async for i in self.stan_users.find({"client": client})]

    async def get_all_stans(self) -> list:
        return [i async for i in self.stan_users.find({})]

    async def is_session(self, user_id: int) -> bool:
        if await self.session.find_one({"user_id": user_id}):
            return True
        return False

    async def update_session(self, user_id: int, session: str) -> None:
        await self.session.update_one(
            {"user_id": user_id},
            {"$set": {"session": session, "date": self.get_datetime()}},
            upsert=True,
        )

    async def rm_session(self, user_id: int) -> None:
        await self.session.delete_one({"user_id": user_id})

    async def get_session(self, user_id: int):
        if not await self.is_session(user_id):
            return False
        data = await self.session.find_one({"user_id": user_id})
        return data

    async def get_all_sessions(self) -> list:
        return [i async for i in self.session.find({})]

    async def is_gbanned(self, user_id: int) -> bool:
        if await self.gban.find_one({"user_id": user_id}):
            return True
        return False

    async def add_gban(self, user_id: int, reason: str) -> bool:
        if await self.is_gbanned(user_id):
            return False
        await self.gban.insert_one(
            {"user_id": user_id, "reason": reason, "date": self.get_datetime()}
        )
        return True

    async def rm_gban(self, user_id: int):
        if not await self.is_gbanned(user_id):
            return None
        reason = (await self.gban.find_one({"user_id": user_id}))["reason"]
        await self.gban.delete_one({"user_id": user_id})
        return reason

    async def get_gban(self) -> list:
        return [i async for i in self.gban.find({})]

    async def get_gban_user(self, user_id: int) -> dict | None:
        if not await self.is_gbanned(user_id):
            return None
        return await self.gban.find_one({"user_id": user_id})


class MongoDatabase(Database):
    def __init__(self, url, name):
        self._client = pymongo.MongoClient(url)
        self._database = self._client[name]

    def set(self, module: str, variable: str, value):
        if not isinstance(module, str) or not isinstance(variable, str):
            raise ValueError("Module and variable must be strings")
        self._database[module].replace_one(
            {"var": variable}, {"var": variable, "val": value}, upsert=True
        )

    def get(self, module: str, variable: str, default=None):
        if not isinstance(module, str) or not isinstance(variable, str):
            raise ValueError("Module and variable must be strings")
        doc = self._database[module].find_one({"var": variable})
        return default if doc is None else doc["val"]

    def get_collection(self, module: str):
        if not isinstance(module, str):
            raise ValueError("Module must be a string")
        return {item["var"]: item["val"] for item in self._database[module].find()}

    def remove(self, module: str, variable: str):
        if not isinstance(module, str) or not isinstance(variable, str):
            raise ValueError("Module and variable must be strings")
        self._database[module].delete_one({"var": variable})

    def close(self):
        self._client.close()

    def add_chat_history(self, user_id, message):
        chat_history = self.get_chat_history(user_id, default=[])
        chat_history.append(message)
        self.set(f"core.cohere.user_{user_id}", "chat_history", chat_history)

    def get_chat_history(self, user_id, default=None):
        if default is None:
            default = []
        return self.get(f"core.cohere.user_{user_id}", "chat_history", default=[])

    def addaiuser(self, user_id):
        chatai_users = self.get("core.chatbot", "chatai_users", default=[])
        if user_id not in chatai_users:
            chatai_users.append(user_id)
            self.set("core.chatbot", "chatai_users", chatai_users)

    def remaiuser(self, user_id):
        chatai_users = self.get("core.chatbot", "chatai_users", default=[])
        if user_id in chatai_users:
            chatai_users.remove(user_id)
            self.set("core.chatbot", "chatai_users", chatai_users)

    def getaiusers(self):
        return self.get("core.chatbot", "chatai_users", default=[])


class SqliteDatabase(Database):
    def __init__(self, file):
        self._conn = sqlite3.connect(file, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()
        self._lock = threading.Lock()

    @staticmethod
    def _parse_row(row: sqlite3.Row):
        if row["type"] == "bool":
            return row["val"] == "1"
        if row["type"] == "int":
            return int(row["val"])
        if row["type"] == "str":
            return row["val"]
        return json.loads(row["val"])

    def _execute(self, module: str, *args, **kwargs) -> sqlite3.Cursor:
        pattern = r"^(core|custom)"
        if not re.match(pattern, module):
            raise ValueError(f"Invalid plugins name format: {module}")

        self._lock.acquire()
        try:
            cursor = self._conn.cursor()
            return cursor.execute(*args, **kwargs)
        except sqlite3.OperationalError as e:
            if str(e).startswith("no such table"):
                sql = f"""
                CREATE TABLE IF NOT EXISTS '{module}' (
                var TEXT UNIQUE NOT NULL,
                val TEXT NOT NULL,
                type TEXT NOT NULL
                )
                """
                cursor = self._conn.cursor()
                cursor.execute(sql)
                self._conn.commit()
                return cursor.execute(*args, **kwargs)
            raise e from None
        finally:
            self._lock.release()

    def get(self, module: str, variable: str, default=None):
        sql = f"SELECT * FROM '{module}' WHERE var=?"
        cur = self._execute(module, sql, (variable,))

        row = cur.fetchone()
        if row is None:
            return default
        return self._parse_row(row)

    def set(self, module: str, variable: str, value) -> bool:
        sql = f"""
        INSERT INTO '{module}' VALUES ( ?, ?, ? )
        ON CONFLICT (var) DO
        UPDATE SET val=?, type=? WHERE var=?
        """

        if isinstance(value, bool):
            val = "1" if value else "0"
            typ = "bool"
        elif isinstance(value, str):
            val = value
            typ = "str"
        elif isinstance(value, int):
            val = str(value)
            typ = "int"
        else:
            val = json.dumps(value)
            typ = "json"

        self._execute(module, sql, (variable, val, typ, val, typ, variable))
        self._conn.commit()

        return True

    def remove(self, module: str, variable: str):
        sql = f"DELETE FROM '{module}' WHERE var=?"
        self._execute(module, sql, (variable,))
        self._conn.commit()

    def get_collection(self, module: str) -> dict:
        pattern = r"^(core|custom)"
        if not re.match(pattern, module):
            raise ValueError(f"Invalid nama plugins format: {module}")

        sql = f"SELECT * FROM '{module}'"
        cur = self._execute(module, sql)

        collection = {}
        for row in cur:
            collection[row["var"]] = self._parse_row(row)

        return collection

    def close(self):
        self._conn.commit()
        self._conn.close()

    def add_chat_history(self, user_id, message):
        chat_history = self.get_chat_history(user_id, default=[])
        chat_history.append(message)
        self.set(f"core.cohere.user_{user_id}", "chat_history", chat_history)

    def get_chat_history(self, user_id, default=None):
        if default is None:
            default = []
        return self.get(f"core.cohere.user_{user_id}", "chat_history", default=[])

    def addaiuser(self, user_id):
        chatai_users = self.get("core.chatbot", "chatai_users", default=[])
        if user_id not in chatai_users:
            chatai_users.append(user_id)
            self.set("core.chatbot", "chatai_users", chatai_users)

    def remaiuser(self, user_id):
        chatai_users = self.get("core.chatbot", "chatai_users", default=[])
        if user_id in chatai_users:
            chatai_users.remove(user_id)
            self.set("core.chatbot", "chatai_users", chatai_users)

    def getaiusers(self):
        return self.get("core.chatbot", "chatai_users", default=[])


if config.db_type in ["mongo", "mongodb"]:
    db = MongoDatabase(config.db_url, config.db_name)
else:
    db = SqliteDatabase(config.db_name)
