from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRequest(BaseModel):
    nome: str
    email: EmailStr
    password: str


class UserModel(BaseModel):
    id: str
    nome: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None


def helper(doc) -> dict:
    data = doc.to_dict()
    data["id"] = doc.id
    return data


