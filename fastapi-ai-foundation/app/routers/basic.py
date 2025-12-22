# app/routers/basic.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import Message, EchoResponse

router = APIRouter()

@router.get("/hello")
async def hello():
    return {"message": "Hello Fatima"}

@router.post("/echo", response_model=EchoResponse)
async def echo(msg: Message):
    # simply returns the same payload
    return {"text": msg.text, "length": len(msg.text)}

@router.delete("/delete-item/{item_id}")
async def delete_item(item_id: int):
    # placeholder delete logic
    return {"status": "deleted", "id": item_id}

@router.post("/reverse")
async def reverse_text(msg: Message):
    return {"original": msg.text, "reversed": msg.text[::-1]}