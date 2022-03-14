import datetime
from discord.ext import commands
import discord
import os

class MyCog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener(name='on_ready')
    async def on_ready(self):
        """BOT起動時にフック
        """
        print(f'BOT起動: {self.bot.user.name}')

    @commands.Cog.listener(name='on_socket_raw_receive')
    async def on_socket_raw_receive(self, message: str):
        """受信メッセージをすべてログに出力

        利用する場合はBOT起動時にis_debug=Trueを指定
        """
        print(f'on_socket_raw_receive: {message}')

    # reload_extension確認時にコメントアウト解除
    # @commands.Cog.listener(name='on_typing')
    # async def on_typing(self, channel: discord.TextChannel, user: discord.User, when: datetime.datetime):
    #     """ユーザの入力にフック

    #     Args:
    #         channel (discord.TextChannel): _description_
    #         user (discord.User): _description_
    #         when (datetime.datetime): _description_
    #     """
    #     await channel.send(f'<@{user.id}>が入力中')

# 必須
def setup(bot: discord.Client):
    return bot.add_cog(MyCog(bot))