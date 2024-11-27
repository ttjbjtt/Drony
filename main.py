from fastapi import FastAPI, BackgroundTasks
from routers import root, transmitted, detected, result
from data_handler import receive_data
from models import Data
from image_handler import get_image  # 추가: get_image 함수 임포트
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# FastAPI 앱 초기화
app = FastAPI()

# GPS 데이터 수신 엔드포인트
@app.post("/gps-data")
async def gps_data_endpoint(data: Data, background_tasks: BackgroundTasks):
    background_tasks.add_task(receive_data, data)
    return {"status": "success", "message": "Data received successfully. Processing in background."}

# 정적 파일 경로 설정 (CSS 파일)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 루트 경로로 HTML 반환
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # 홈 화면 콘텐츠
    content = """
    <h2>Drony - Image Viewer</h2>
    <p>Select an option from the header to proceed.</p>
    """
    # index.html 템플릿 로드
    with open("templates/index.html", "r", encoding="utf-8") as file:
        base_html = file.read()
    
    # {content} 부분에 홈 화면 콘텐츠 삽입
    return HTMLResponse(base_html.replace("{content}", content))

# 특정 이미지 반환 엔드포인트 추가
@app.get("/images/{folder}/{image_name}")
async def get_image_endpoint(folder: str, image_name: str):
    return await get_image(image_name, folder)

# 루트 디렉토리 엔드포인트
app.include_router(root.router)

# 모든 이미지 목록 엔드포인트
app.include_router(transmitted.router)

# 인식된 이미지 목록 엔드포인트
app.include_router(detected.router)

# 실종자 좌표 HTML 엔드포인트
app.include_router(result.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)