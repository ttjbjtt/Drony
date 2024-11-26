import os
import base64
import config
from datetime import datetime
from pytz import timezone
from fastapi import HTTPException
from pydantic import BaseModel
from ultralytics import YOLO

from models import Data
from deepLearning import *
from coordinate import CalculateCoordinate

# 이미지 저장 디렉토리 설정
SAVE_DIR = config.SAVE_DIR
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

DETECTED_DIR = config.DETECTED_DIR
if not os.path.exists(DETECTED_DIR):
    os.makedirs(DETECTED_DIR)

MODEL_PATH = config.MODEL_PATH
try:
    model_path = YOLO(MODEL_PATH)
except Exception as e:
    raise ValueError(f"Failed to load YOLO model: {e}")

# 수신 받은 데이터를 처리하는 함수
async def receive_data(data: Data):
    try:
        # 현재 시간 추가
        timestamp = datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d_%H%M%S")  # 띄어쓰기와 : 제거
        print(f"[{timestamp}] Received GPS Data - Latitude: {data.latitude}, Longitude: {data.longitude}, Altitude: {data.altitude}, Heading: {data.heading}")

        # Base64 이미지 데이터를 디코딩
        try:
            image_data = base64.b64decode(data.image)
        except Exception as e:
            print(f"Base64 decoding error: {e}")
            raise HTTPException(status_code=400, detail="Invalid Base64 image data")

        # 원본 이미지 파일 이름 생성 및 저장
        image_filename = os.path.join(SAVE_DIR, f"image_{timestamp}.jpg")
        try:
            with open(image_filename, "wb") as img_file:
                img_file.write(image_data)
            print(f"Original image saved as: {image_filename}")
        except Exception as e:
            print(f"Error saving original image: {e}")
            raise HTTPException(status_code=500, detail="Failed to save the original image")

        # YOLO 모델을 사용한 객체 감지
        try:
            encoded_image, center_coordinates = detect_and_draw_boxes2(image_data, model_path)
            print(f"YOLO detection completed. Objects detected: {len(center_coordinates)}")
        except Exception as e:
            print(f"Error during YOLO detection: {e}")
            raise HTTPException(status_code=500, detail="YOLO detection failed")

        # 객체가 검출된 경우
        if len(center_coordinates) > 0:
            # 첫 번째 객체의 중앙 좌표를 사용하여 좌표 계산
            try:
                CalculateCoordinate(center_coordinates[0]["center_x"], center_coordinates[0]["center_y"], data, encoded_image)
            except Exception as e:
                print(f"Error during coordinate calculation: {e}")
                raise HTTPException(status_code=500, detail="Coordinate calculation failed")

            # 검출된 이미지 파일 이름 생성 및 저장
            encoded_image = base64.b64decode(encoded_image)
            detected_image_filename = os.path.join(DETECTED_DIR, f"detected_{timestamp}.jpg")
            try:
                with open(detected_image_filename, "wb") as detected_img_file:
                    detected_img_file.write(encoded_image)
                print(f"Detected image saved as: {detected_image_filename}")
            except Exception as e:
                print(f"Error saving detected image: {e}")
                raise HTTPException(status_code=500, detail="Failed to save the detected image")
        else:
            print("No objects detected in the image.")

    except Exception as e:
        # 예외 발생 시 오류 처리
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the data")