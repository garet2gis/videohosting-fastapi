from typing import List

from fastapi import UploadFile, File, APIRouter, Form
import shutil
from schemas import UploadVideo, GetVideo
from models import Video, User

video_router = APIRouter()


@video_router.get('/videos', response_model=List[GetVideo])
async def get_video():
    videos = await Video.objects.select_related("user").all()
    return videos


@video_router.get('/videos/{video_id}', response_model=GetVideo)
async def get_video(video_id: int):
    videos = await Video.objects.select_related("user").get(pk=video_id)
    return videos


@video_router.post('/videos', response_model=GetVideo)
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    user = await User.objects.first()

    return await Video.objects.create(file=file.filename, user=user, **info.dict())

