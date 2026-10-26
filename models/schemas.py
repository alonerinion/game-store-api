from pydantic import BaseModel, EmailStr
from typing import Optional

# 1. Modelo de Usuario
class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool = True  # Campo de estado para histórico

# 2. Modelo de Videojuego (Catálogo / Tienda)
class Game(BaseModel):
    id: str
    title: str            # Atributo clave para búsqueda diferente al ID
    category: str         # Atributo clave para el endpoint de filtrado
    price: float
    release_date: str
    is_active: bool = True  # Campo de estado para histórico

# 3. Modelo de Relación Usuario-Juego (Biblioteca y Deseados)
class UserGame(BaseModel):
    id: str
    user_id: str
    game_id: str
    status: str           # "owned" (biblioteca) o "wishlist" (deseados)
    is_active: bool = True  # Campo de estado para histórico