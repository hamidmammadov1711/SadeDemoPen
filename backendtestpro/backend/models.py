# models.py
# Request/Response modelleri
# backend/models.py
from pydantic import BaseModel

class TestRequest(BaseModel):
    target: str

class TestResponse(BaseModel):
    status: str
    details: str
# Bu modeller, API istek ve yanıtlarını tanımlamak için kullanılacak
# Veritabanı modelleri burada tanımlanacaq