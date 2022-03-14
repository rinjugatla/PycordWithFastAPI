import asyncio
import discord
from discord.ext import commands
from fastapi import FastAPI
import uvicorn
import const

from apis.v1 import ApiV1


class DiscordBot():
    def __init__(self, is_debug: bool = False):
        self.app = FastAPI()
        self.bot = commands.Bot(
            heartbeat_timeout=20,
            intents=self.create_intents(),
            chunk_guilds_at_startup=False,
            enable_debug_events = is_debug)

        api_v1 = ApiV1(self.bot)
        self.app.include_router(api_v1.router)

        @self.app.on_event('startup')
        async def fastapi_startup():
            """FastAPIスタートアップ時にDiscordBotを起動
            """
            for name in const.COG_NAMES:
                self.bot.load_extension(name)
            asyncio.create_task(self.bot.start(const.BOT_TOKEN))

    def create_intents(self) -> discord.Intents:
        """インテンツ作成

        https://github.com/Pycord-Development/pycord/issues/872
        サーバへの参加人数が非常に多く、guilds, membersが同時に有効な場合エラー
        chunk_guilds_at_startup=Falseで対策

        Returns:
            discord.Intents: _description_
        """
        intents = discord.Intents.all()
        intents.typing = False
        intents.presences = False
        return intents

    def start(self):
        uvicorn.run(self.app, host=const.HOST, port=const.PORT)

bot = DiscordBot()
bot.start()