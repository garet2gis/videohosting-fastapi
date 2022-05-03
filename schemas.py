from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str


class UploadVideo(BaseModel):
    title: str
    description: str


class GetVideo(BaseModel):
    id: int
    title: str
    description: str
    file: str
    user: User
