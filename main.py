from fastapi import FastAPI
from data_handler import Data, receive_data
from image_handler import list_images, get_image

# FastAPI 앱 초기화
app = FastAPI()

# GPS 데이터 수신 엔드포인트
@app.post("/gps-data")
async def gps_data_endpoint(data: Data):
    return await receive_data(data)

# 이미지 목록 조회 엔드포인트
@app.get("/")
async def list_images_endpoint():
    return await list_images()

# 특정 이미지 반환 엔드포인트
@app.get("/images/{image_name}")
async def get_image_endpoint(image_name: str):
    return await get_image(image_name)

# FastAPI 애플리케이션 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
