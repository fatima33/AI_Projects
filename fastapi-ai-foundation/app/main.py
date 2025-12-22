# app/main.py
from fastapi import FastAPI
from app.routers import basic

app = FastAPI(title="FastAPI AI Foundation", version="0.1")

# include routers
app.include_router(basic.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI AI Foundation"}