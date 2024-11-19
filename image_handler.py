import os
import config
from fastapi import HTTPException
from fastapi.responses import FileResponse, HTMLResponse

# 이미지가 저장된 디렉토리
IMAGE_FOLDER = config.IMAGE_FOLDER
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# 이미지 목록을 반환하는 함수
async def list_images():
    try:
        files = os.listdir(IMAGE_FOLDER)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if not image_files:
            return "<h1>No images found in the directory!</h1>"

        html_content = "<h1>Available Images:</h1><ul>"
        for image in image_files:
            html_content += f'<li><a href="/images/{image}">{image}</a></li>'
        html_content += "</ul>"
        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 특정 이미지를 반환하는 함수
async def get_image(image_name: str):
    image_path = os.path.join(IMAGE_FOLDER, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)
