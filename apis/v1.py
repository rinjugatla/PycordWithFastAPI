import sys
import discord
from discord.ext import commands
from fastapi import APIRouter, Request
import const
from models.basic_post_api_model import BasicBotPostApiModel
from models.basic_response_model import BasicResponseModel


class ApiV1(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.router = APIRouter()

        @self.router.get('/')
        async def root(request: Request):
            """単純なAPI

            Args:
                request (Request): _description_

            Returns:
                _type_: _description_
            """
            return {'message': 'root'}

        @self.router.get('/hello/{name}', response_model=BasicResponseModel)
        async def hello(request: Request, name: str):
            """URL、レスポンスモデルの利用例

            Args:
                request (Request): _description_
                name (str): _description_

            Returns:
                _type_: _description_
            """
            return {'message': f'hello {name}'}

        @self.router.post('/body_test', response_model=BasicResponseModel)
        async def body_test(request: Request, model: BasicBotPostApiModel):
            """Bodyに{"body_test": "hoge"}がない場合エラー

            Args:
                request (Request): _description_
                model (BasicBotPostApiModel): _description_

            Returns:
                _type_: _description_
            """
            return {'message': 'ok'}


        @self.router.post('/bot/reload', response_model=BasicResponseModel)
        async def bot_reload(request: Request):
            """DiscordBotのcogをリロード

            Args:
                request (Request): _description_
            """
            is_valid = self.is_valid_token(request)
            if not is_valid:
                ip = request.client.host
                return {'message': f'不正なTOKEN {ip}'}

            for name in const.COG_NAMES:
                self.bot.reload_extension(name)
            return {'message': 'BOTリロード完了'}
            
        @self.router.post('/bot/quit', response_model=BasicResponseModel)
        async def bot_quit(request: Request):
            """DiscordBotを終了

            Args:
                request (Request): _description_
            """
            is_valid = self.is_valid_token(request)
            if not is_valid:
                ip = request.client.host
                return {'message': f'不正なTOKEN {ip}'}

            await self.bot.close()
            sys.exit()

    def is_valid_token(self, request: Request) -> bool:
        """API TOKENが有効か
        """
        headers = request.headers
        if not ('token' in headers):
            return False
        
        is_valid = headers.get('token') == const.API_TOKEN
        return is_valid