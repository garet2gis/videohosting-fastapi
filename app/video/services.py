from pathlib import Path
from typing import BinaryIO, Generator, Optional
from uuid import uuid4

import aiofiles

from app.user.models import User

from fastapi import HTTPException, UploadFile

import ormar

from starlette.requests import Request

from .models import Video
from .schemas import UploadVideo


async def write_video(file_name: str, file: UploadFile) -> None:
    async with aiofiles.open(file_name, 'wb') as buffer:
        data = await file.read()
        if type(data) == bytes:
            await buffer.write(data)


async def save_video(
        user: User,
        file: UploadFile,
        title: str,
        description: Optional[str] = None,
        # back_tasks: BackgroundTasks,
) -> Optional[Video]:
    file_name = f'app/media/{user.id}_{uuid4()}.mp4'
    if file.content_type == 'video/mp4':
        # back_tasks.add_task(write_video, file_name, file)
        await write_video(file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")

    if description is None:
        return await Video.objects.create(file=file_name, user=user.dict(), title=title)
    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, user=user.dict(), **info.dict())


def ranged(
        file: BinaryIO,
        start: int = 0,
        end: Optional[int] = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


async def open_file(request: Request, video_id: int) -> tuple:
    try:
        video = await Video.objects.get(pk=video_id)
    except ormar.exceptions.NoMatch:
        raise HTTPException(status_code=404, detail='Not found')
    path = Path(video.file)

    file = path.open('rb')
    print(file)
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    headers = {}
    content_range = request.headers.get('range')

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split('=')[-1]
        range_start_str, range_end_str, *_ = map(str.strip, (content_ranges + '-').split('-'))

        range_start = max(0, int(range_start_str)) if range_start_str else 0
        range_end = min(file_size - 1, int(range_end_str)) if range_end_str else file_size - 1

        print(range_start)
        print(range_end)

        content_length = (range_end - range_start) + 1
        result_file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'
        return result_file, status_code, content_length, headers

    return file, status_code, content_length, headers
