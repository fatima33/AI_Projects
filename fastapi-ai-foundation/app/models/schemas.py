# app/models/schemas.py
from pydantic import BaseModel

class Message(BaseModel):
    text: str

class EchoResponse(BaseModel):
    text: str
    length: int