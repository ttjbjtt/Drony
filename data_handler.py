import os
import base64
import config
from datetime import datetime
from pytz import timezone
from fastapi import HTTPException
from pydantic import BaseModel

# 이미지 저장 디렉토리 설정
SAVE_DIR = config.SAVE_DIR
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 데이터 모델 정의
class Data(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    heading: float
    image: str  # Base64 인코딩된 이미지 데이터

# 수신 받은 데이터를 처리하는 함수
async def receive_data(data: Data):
    try:
        # 현재 시간 추가
        timestamp = datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")

        # 받은 GPS 데이터 로그 출력
        print(f"[{timestamp}] Received GPS Data - Latitude: {data.latitude}, Longitude: {data.longitude}, Altitude: {data.altitude}, Heading: {data.heading}")

        # Base64 이미지 데이터를 디코딩하여 파일로 저장
        image_data = base64.b64decode(data.image)
        image_filename = os.path.join(SAVE_DIR, f"image_{timestamp.replace(':', '').replace(' ', '_')}.jpg")

        with open(image_filename, "wb") as img_file:
            img_file.write(image_data)

        print(f"Image saved as {image_filename}")

        return {"status": "success", "message": "Data and image received successfully"}

    except Exception as e:
        # 예외 발생 시 오류 처리
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the data.")
