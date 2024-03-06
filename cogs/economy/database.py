import aiosqlite
from discord.ext import commands


class Database(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.DB = "users.db"

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER,
                    guild_id INTEGER,
                    coins INTEGER DEFAULT 500,
                    xp INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, guild_id)
                )
            """)
            await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        await self.add_user(message.author, message.guild)
        await self.add_xp(message.author, message.guild, 5)

    async def add_user(self, user, guild):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("INSERT OR IGNORE INTO users (user_id, guild_id) VALUES (?, ?)", (user.id, guild.id))
            await db.commit()

    async def add_coins(self, user, guild, amount):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("UPDATE users SET coins = coins + ? WHERE user_id = ? AND guild_id = ?",
                             (amount, user.id, guild.id))
            await db.commit()

    async def add_xp(self, user, guild, amount):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("UPDATE users SET xp = xp + ? WHERE user_id = ? AND guild_id = ?",
                             (amount, user.id, guild.id))
            await db.commit()

    async def get_coins(self, user, guild):
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT coins FROM users WHERE user_id = ? AND guild_id = ?",
                                  (user.id, guild.id)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0

    async def get_xp(self, user, guild):
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT xp FROM users WHERE user_id = ? AND guild_id = ?",
                                  (user.id, guild.id)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0


def setup(client):
    client.add_cog(Database(client))
