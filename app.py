4# app.py
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# GPS 데이터를 받을 모델 정의
class GPSData(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    heading: float

# /gps-data 엔드포인트로 POST 요청을 받는 API 생성
@app.post("/gps-data")
async def receive_gps_data(data: GPSData):
    # 받은 데이터를 로그로 출력
    print(f"Received GPS Data: {data}")
    return {"status": "success", "message": "Data received successfully"}
    

# 이 파일이 직접 실행될 때 main() 함수 호출
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)