from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from utils.html_generator import generate_image_list_html
from utils.file_handler import get_images_in_directory
import config

router = APIRouter()

@router.get("/detected", response_class=HTMLResponse)
async def list_detected_images():
    # 1. 인식된 이미지 목록 가져오기
    images = get_images_in_directory(config.DETECTED_DIR)

    # 2. 동적 콘텐츠 생성
    content = generate_image_list_html(images, "인식된 이미지")
    content = content.replace("margin: 50px;", "margin: 0;")

    # 3. 공통 템플릿(index.html) 로드
    with open("templates/index.html", "r", encoding="utf-8") as file:
        base_html = file.read()

    # 4. {content}에 동적 콘텐츠 삽입
    return HTMLResponse(base_html.replace("{content}", content))
