import math
import folium
import numpy as np
from data_handler import Data
from folium.raster_layers import ImageOverlay
from folium.plugins import FloatImage  # 이미지 위치 고정
import base64

def CalculateCoordinate(x, y, gpsData: Data, Image):  # 좌표 계산 함수
    try:
        # 각도를 라디안으로 변환
        CameraAngle = math.radians(45)  # 카메라 기울기(임의 설정)
        horizontalFov = math.radians(84)  # 수평 화각
        verticalFov = math.radians(62)  # 수직 화각
        heading = math.radians(gpsData.heading)  # 드론 헤딩 방향

        IW = 8160
        IH = 6120  # 촬영된 이미지의 픽셀 가로 세로(임의 설정)

        # 드론 고도, 위경도
        height = 6
        DroneLAT = gpsData.latitude
        DroneLNG = gpsData.longitude

        # 가장 먼 촬영 지점까지 거리, 가장 가까운 촬영 지점까지 거리
        dFar = height * (math.cos(CameraAngle) + math.tan(verticalFov / 2) * math.sin(CameraAngle)) / (
                    math.sin(CameraAngle) - math.tan(verticalFov / 2) * math.cos(CameraAngle))
        dNear = height * (math.cos(CameraAngle) - math.tan(verticalFov / 2) * math.sin(CameraAngle)) / (
                    math.sin(CameraAngle) + math.tan(verticalFov / 2) * math.cos(CameraAngle))

        # 중심을 기준으로 한 좌우 길이(가로 길이/2)
        wNear = dNear * math.tan(horizontalFov / 2)
        wFar = dFar * math.tan(horizontalFov / 2)

        # 거리를 도 단위로 변환
        dFar = dFar / 111320  # 1도 위도가 약 111320 미터
        dNear = dNear / 111320
        wFar = wFar / (111320 * math.cos(DroneLAT))  # 위도에 따른 경도의 미터당 변환
        wNear = wNear / (111320 * math.cos(DroneLAT))

        # 위도 경도 증가 비를 이용하여 객체의 위도 경도 구하기
        X = (2 * wNear + abs(2 * wFar - 2 * wNear) / IH * (IH - y)) / IW * abs(x - IW / 2)
        Y = dNear + abs(dFar - dNear) / IH * (IH - y)

        # 헤딩 방향 고려
        ObjectLNG = DroneLNG + X * math.cos(heading) + Y * math.sin(heading)
        ObjectLAT = DroneLAT - X * math.sin(heading) + Y * math.cos(heading)

        Object = [ObjectLAT, ObjectLNG]

        # 지도 생성
        m = folium.Map(location=[DroneLAT, DroneLNG], zoom_start=17)
        folium.Marker(location=[DroneLAT, DroneLNG], popup="드론 위치", icon=folium.Icon(color="blue")).add_to(m)
        folium.Marker(Object, popup="실종자 위치", icon=folium.Icon(color="red", icon='user')).add_to(m)

        # 경계 지정 (이미지가 위치할 좌표)
        bounds = [[Object[0] - 0.001, Object[1] - 0.002], [Object[0], Object[1]]]

        # 이미지 디코딩
        if gpsData.image.startswith("data:image"):
            gpsData.image = gpsData.image.split(",")[1]

        try:
            image = base64.b64decode(Image)
            with open("./map/drone_image.png", "wb") as file:
                file.write(image)
        except base64.binascii.Error:
            raise ValueError("이미지 디코딩 실패. 올바른 base64 데이터가 아닙니다.")

        # 이미지 오버레이 추가
        try:
            ImageOverlay(
                image='./map/drone_image.png',  # 로컬 이미지 경로
                bounds=bounds,
                opacity=1.0,  # 투명도 (0.0 ~ 1.0)
            ).add_to(m)
        except Exception as e:
            raise RuntimeError(f"이미지 오버레이 생성 실패: {e}")

        # HTML로 저장
        m.save('./map/map.html')

        return Object

    except Exception as e:
        print(f"에러 발생: {e}")
        return None
