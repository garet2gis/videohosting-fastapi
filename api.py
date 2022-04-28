from fastapi import UploadFile, File, APIRouter
import shutil

video_router = APIRouter()


@video_router.post('/')
async def root(file: UploadFile = File(...)):
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_name": file.filename}


@video_router.post('/upload_image')
async def upload_image(files: list[UploadFile] = File(...)):
    for img in files:
        with open(f'{img.filename}', "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {"file_name": img.filename}
