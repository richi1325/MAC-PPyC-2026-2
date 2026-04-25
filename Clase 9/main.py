import os

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World", "public_ip": os.getenv("PUBLIC_IP")}