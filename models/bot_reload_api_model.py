from pydantic import BaseModel, Field


class BotReloadApiModel(BaseModel):
    token: str