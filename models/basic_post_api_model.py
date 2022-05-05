from pydantic import BaseModel, Field


class BasicBotPostApiModel(BaseModel):
    body_test: str