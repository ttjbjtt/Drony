import os
import config
from fastapi import HTTPException
from fastapi.responses import FileResponse, HTMLResponse

# 이미지가 저장된 디렉토리 설정
IMAGE_FOLDER = config.SAVE_DIR  # 전송된 이미지 저장 경로
DETECTED_DIR = config.DETECTED_DIR  # 사람이 인식된 이미지 저장 경로

# 디렉토리가 없으면 생성
for folder in [IMAGE_FOLDER, DETECTED_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 이미지 목록을 반환하는 함수
async def list_images():
    try:
        # 전송된 이미지 목록
        transmitted_images = [
            f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]

        # 인식된 이미지 목록
        detected_images = [
            f for f in os.listdir(DETECTED_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]

        # HTML 콘텐츠 생성
        html_content = "<h1>Image Viewer</h1>"

        # 전송된 이미지 섹션
        html_content += "<h2>Transmitted Images:</h2>"
        if transmitted_images:
            html_content += "<ul>"
            for image in transmitted_images:
                html_content += f'<li><a href="/images/general/{image}">{image}</a></li>'
            html_content += "</ul>"
        else:
            html_content += "<p>No images found in the transmitted folder.</p>"

        # 인식된 이미지 섹션
        html_content += "<h2>Recognized Images:</h2>"
        if detected_images:
            html_content += "<ul>"
            for image in detected_images:
                html_content += f'<li><a href="/images/detected/{image}">{image}</a></li>'
            html_content += "</ul>"
        else:
            html_content += "<p>No images found in the recognized folder.</p>"

        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing images: {str(e)}")
    
# 특정 이미지를 반환하는 함수
async def get_image(image_name: str, folder: str):
    # 폴더 매핑
    if folder == "received_images":
        image_path = os.path.join(config.SAVE_DIR, image_name)
    elif folder == "DETECTED_DIR":
        image_path = os.path.join(config.DETECTED_DIR, image_name)
    else:
        raise HTTPException(status_code=400, detail="Invalid folder specified")

    # 디버깅: 요청된 경로 출력
    print(f"Requested folder: {folder}, Resolved path: {image_path}")

    # 이미지 존재 여부 확인
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail=f"Image not found at path: {image_path}")

    # 이미지 반환
    return FileResponse(image_path)