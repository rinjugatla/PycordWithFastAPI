from pydantic import BaseModel, Field


class BasicBotPostApiModel(BaseModel):
    token: str