from typing import List, Optional

from app.user.models import User

from fastapi import APIRouter, File, Form, UploadFile

from starlette.requests import Request
from starlette.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates, _TemplateResponse

from .models import Video
from .schemas import GetVideo
from .services import open_file, save_video

video_router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@video_router.post('/videos', response_model=GetVideo)
async def create_video(
        # back_tasks: BackgroundTasks,
        title: str = Form(...),
        description: Optional[str] = Form(None),
        file: UploadFile = File(...),
) -> Optional[Video]:
    """ Add video """

    # TODO: fix user identification
    user = await User.objects.first()

    return await save_video(user, file, title, description)


@video_router.get('/videos', response_model=List[GetVideo])
async def get_videos() -> List[Video]:
    return await Video.objects.select_related('user').all()


@video_router.get('/index/{video_id}', response_class=HTMLResponse)
async def get_video(request: Request, video_id: int) -> _TemplateResponse:
    return templates.TemplateResponse('index.html', {'request': request, 'path': video_id})


@video_router.get('/video/{video_id}')
async def get_video_stream(request: Request, video_id: int) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_id)
    print(f'con: {content_length}')
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response
