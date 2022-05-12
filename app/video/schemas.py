from app.user.schemas import User

from pydantic import BaseModel


class UploadVideo(BaseModel):
    title: str
    description: str


class GetVideo(BaseModel):
    id: int
    title: str
    description: str
    file: str
    user: User
