from io import BytesIO
from PIL import Image, ExifTags
from ultralytics import YOLO
import cv2
import numpy as np
import base64

def correct_image_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except Exception as e:
        print(f"Error correcting orientation: {e}")
    return image

def detect_and_draw_boxes(image_data, yolo_model):
    try:
        # PIL 이미지로 변환 (BytesIO 사용)
        image = Image.open(BytesIO(image_data))
        image = correct_image_orientation(image)
    except Exception as e:
        raise ValueError(f"Failed to open image data: {e}")

    # YOLO 모델 호출
    try:
        results = yolo_model(image)
        # 객체가 인식되지 않으면 메시지 출력 후 종료
        if len(results) == 0 or len(results[0].boxes) == 0:
            print("No objects detected by YOLO model")
            return None, []
    except Exception as e:
        raise ValueError(f"YOLO detection error: {e}")

    # 경계 박스를 그린 결과 이미지 생성
    try:
        result_image = results[0].plot()
        result_image = cv2.cvtColor(np.array(result_image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise ValueError(f"Failed to process result image: {e}")
    
    # 결과 이미지 JPG 인코딩
    try:
        success, buffer = cv2.imencode('.jpg', result_image)
        if not success:
            raise ValueError("Failed to encode result image as JPG")
        encoded_result_image = base64.b64encode(buffer).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Image encoding error: {e}")

    # 중앙 좌표 계산
    center_coordinates = []
    try:
        for box in results[0].boxes:
            xmin, ymin, xmax, ymax = box.xyxy[0]
            center_x = (xmin + xmax) / 2
            center_y = (ymin + ymax) / 2
            center_coordinates.append({"center_x": center_x.item(), "center_y": center_y.item()})
    except Exception as e:
        raise ValueError(f"Error calculating bounding box center coordinates: {e}")

    return encoded_result_image, center_coordinates
