import shutil
from typing import List

from fastapi import APIRouter, File, Form, UploadFile

from models import User, Video

from schemas import GetVideo, UploadVideo

video_router = APIRouter()


@video_router.get('/videos', response_model=List[GetVideo])
async def get_video() -> List[Video]:
    videos = await Video.objects.select_related('user').all()
    return videos


@video_router.get('/videos/{video_id}', response_model=GetVideo)
async def get_video_by_id(video_id: int) -> Video:
    video = await Video.objects.select_related('user').get(pk=video_id)
    return video


@video_router.post('/videos', response_model=GetVideo)
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)) -> Video:
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    user = await User.objects.first()
    return await Video.objects.create(file=file.filename, user=user, **info.dict())
