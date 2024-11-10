import math
import folium
import numpy as np
from charset_normalizer.md__mypyc import exports

from app import GPSData
# (x, y):객체의 픽셀좌표 gpsData:드론의 위경도 좌표,드론 고도,헤딩방향 클래스
def CalculateCoordinate(x, y, gpsData: GPSData): #좌표계산 함수
    # 각도를 라디안으로 변환
    CameraAngle = math.radians(30)  # 카메라 기울기(임의 설정)
    horizontalFov = math.radians(84)  # 수평 화각
    verticalFov = math.radians(62)  # 수직 화각
    heading = math.radians(gpsData.heading)  # 드론 헤딩 방향
    IW = 8160
    IH = 6120  # 촬영된 이미지의 픽셀 가로 세로(임의 설정)
    # 드론 고도, 위경도, 헤딩방향
    height = gpsData.altitude
    DroneLAT = gpsData.latitude
    DroneLNG = gpsData.longitude

    # 지면상 거리 계산
    dCenter = height * np.tan(CameraAngle) #카메라 시야 중심으로부터 지면까지의 거리
    width = 2 * (height / np.cos(CameraAngle)) * np.tan(horizontalFov / 2)
    height = 2 * (height / np.cos(CameraAngle)) * np.tan(verticalFov / 2)

    # 모서리의 상대 위치 계산
    corners = [
        (-width / 2, dCenter + height / 2),  # 좌상단
        (width / 2, dCenter + height / 2),  # 우상단
        (width / 2, dCenter - height / 2),  # 우하단
        (-width / 2, dCenter - height / 2) # 좌하단
    ]


    # 회전 변환과 위도/경도 변환
    geo_corners = []

    for a, b in corners:
        # 회전 적용
        X = a * np.cos(heading) - b * np.sin(heading)
        Y = a * np.sin(heading) + b * np.cos(heading)

        # 위도 및 경도 변화량 계산
        Lat = Y / 111320  # 위도 변화량 (m -> 도)
        Lon = X / (111320 * np.cos(np.radians(DroneLAT)))  # 경도 변화량 (m -> 도)

        # 모서리의 실제 위도와 경도 계산
        corner_lat = DroneLAT + Lat
        corner_lon = DroneLNG + Lon
        geo_corners.append((corner_lat, corner_lon))

    # 지리 좌표를 numpy 배열로 변환 (위도, 경도 -> x, y 순서로 변환 필요)
    geo_points = np.array([(lon, lat) for lat, lon in geo_corners])

    # 위도 경도 증가 비를 이용하여 객체의 위도 경도 구하기
    ObjectLAT = DroneLAT + abs((geo_points[0][1] - geo_points[2][1])+(geo_points[1][1] - geo_points[3][1])/2) / IH * (IH - y)
    ObjectLNG = DroneLNG + 2 / IW * abs(
        geo_points[0][0] - geo_points[1][0] - geo_points[2][0] + geo_points[3][0]) / IH * (IH - y) * x

    Object = [ObjectLAT, ObjectLNG]

    m = folium.Map(location=[DroneLAT, DroneLNG], zoom_start=18)
    folium.Marker(location=[DroneLAT, DroneLNG], popup="드론 위치", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker(Object, popup="실종자 위치", icon=folium.Icon(color="red")).add_to(m)
    m.save('./static/index.html')

    return Object