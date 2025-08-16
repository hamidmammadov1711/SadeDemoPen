# main.py
# Backend ana dosyası
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "CTF platforması hazırdır"}
