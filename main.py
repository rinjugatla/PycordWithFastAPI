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
            intents=self.create_intents(),
            enable_debug_events = is_debug)

    def create_intents(self) -> discord.Intents:
        """インテンツ作成

        https://github.com/Pycord-Development/pycord/issues/872
        bot.start(token)かつguilds, membersが同時に有効な場合エラー

        Returns:
            discord.Intents: _description_
        """
        intents = discord.Intents.all()
        intents.typing = False
        intents.presences = False
        return intents

    def start(self):
        for name in const.COG_NAMES:
            self.bot.load_extension(name)
        self.bot.run(const.BOT_TOKEN)

bot = DiscordBot()
bot.start()