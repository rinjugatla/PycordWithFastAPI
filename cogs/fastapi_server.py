import asyncio
from discord import Client, Cog

from fastapi import FastAPI
from uvicorn import Config, Server
from apis.v1 import ApiV1
import const


class FastApiServer(Cog):
    def __init__(self, bot: Client):
        self.bot = bot
    
    @Cog.listener(name='on_ready')
    async def on_ready(self):
        self.app = FastAPI()
        api_v1 = ApiV1(self.bot)
        self.app.include_router(api_v1.router)

        loop = asyncio.new_event_loop()
        config = Config(
            app=self.app,
            loop=loop,
            host=const.HOST,
            port=const.PORT)
        server = Server(config)

        loop.run_until_complete(await server.serve())

def setup(bot: Client):
    return bot.add_cog(FastApiServer(bot))