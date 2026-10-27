from pydantic import BaseModel, EmailStr
from typing import Optional

class Game(BaseModel):
    id: str
    title: str
    category: str
    price: float
    release_date: str
    is_active: bool = True

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool = True

class LibraryWishlist(BaseModel):
    id: str
    user_id: str
    game_id: str
    status: str  # Ej: "comprado" o "deseado"
    is_active: bool = True