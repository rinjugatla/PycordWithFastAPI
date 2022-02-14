from pydantic import BaseModel, Field


class BasicResponseModel(BaseModel):
    message: str = Field(description='説明', example='例')