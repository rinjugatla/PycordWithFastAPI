import asyncio
from discord.ext import commands
from fastapi import FastAPI
import uvicorn
import const

from apis.v1 import ApiV1


class DiscordBot():
    def __init__(self):
        self.app = FastAPI()
        self.bot = commands.Bot(heartbeat_timeout=20)

        api_v1 = ApiV1(self.bot)
        self.app.include_router(api_v1.router)

        @self.app.on_event('startup')
        async def fastapi_startup():
            """FastAPIスタートアップ時にDiscordBotを起動
            """
            for name in const.COG_NAMES:
                self.bot.load_extension(name)
            asyncio.create_task(self.bot.start(const.BOT_TOKEN))

    def start(self):
        uvicorn.run(self.app, host=const.HOST, port=const.PORT)

bot = DiscordBot()
bot.start()