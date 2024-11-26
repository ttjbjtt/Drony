from pydantic import BaseModel

class Data(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    heading: float
    image: str  # Base64 encoded image