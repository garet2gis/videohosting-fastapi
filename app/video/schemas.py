from typing import Optional

from app.user.schemas import User

from pydantic import BaseModel


class UploadVideo(BaseModel):
    title: str
    description: Optional[str]


class GetVideo(BaseModel):
    id: int
    title: str
    description: Optional[str]
    file: str
    user: User
