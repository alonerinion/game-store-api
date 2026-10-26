from fastapi import FastAPI, HTTPException
from typing import List
from models.schemas import Game, User, UserGame
from database import get_all_from_csv, save_to_csv, update_csv_file

app = FastAPI(title="Game Store API", version="1.0")

# ==================== MÓDULO DE JUEGOS ====================
GAMES_CSV = "games.csv"


@app.post("/games/", response_model=Game)
def create_game(game: Game):
    games = get_all_from_csv(GAMES_CSV)
    for g in games:
        if g and "id" in g and g["id"] == game.id:
            raise HTTPException(status_code=400, detail="El ID del juego ya existe.")

    save_to_csv(GAMES_CSV, game.model_dump())
    return game


@app.post("/games/bulk/", response_model=List[Game])
def create_multiple_games(games_list: List[Game]):
    """Permite registrar múltiples videojuegos en una sola petición."""
    existing_games = get_all_from_csv(GAMES_CSV)
    existing_ids = {g["id"] for g in existing_games if g and "id" in g}

    for game in games_list:
        if game.id in existing_ids:
            raise HTTPException(
                status_code=400,
                detail=f"El ID del juego '{game.id}' ya existe en el sistema."
            )
        save_to_csv(GAMES_CSV, game.model_dump())
        existing_ids.add(game.id)

    return games_list


@app.get("/games/", response_model=List[Game])
def get_games():
    games = get_all_from_csv(GAMES_CSV)
    return [g for g in games if g and (g.get("is_active") == "True" or g.get("is_active") is True)]


@app.get("/games/{game_id}", response_model=Game)
def get_game_by_id(game_id: str):
    games = get_all_from_csv(GAMES_CSV)
    for g in games:
        if g and "id" in g and g["id"] == game_id:
            return g
    raise HTTPException(status_code=404, detail="Videojuego no encontrado.")


@app.get("/games/search/title", response_model=List[Game])
def search_games_by_title(title: str):
    games = get_all_from_csv(GAMES_CSV)
    results = [g for g in games if g and "title" in g and title.lower() in g["title"].lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron juegos con ese título.")
    return results


@app.get("/games/filter/category", response_model=List[Game])
def filter_games_by_category(category: str):
    games = get_all_from_csv(GAMES_CSV)
    results = [g for g in games if g and "category" in g and category.lower() == g["category"].lower()]
    return results


@app.delete("/games/{game_id}")
def delete_game(game_id: str):
    games = get_all_from_csv(GAMES_CSV)
    game_found = False
    for g in games:
        if g and "id" in g and g["id"] == game_id:
            g["is_active"] = False
            game_found = True
            break

    if not game_found:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado para eliminar.")

    fieldnames = ["id", "title", "category", "price", "release_date", "is_active"]
    update_csv_file(GAMES_CSV, games, fieldnames)
    return {"message": "Videojuego marcado como inactivo exitosamente (histórico conservado)."}


# ==================== MÓDULO DE USUARIOS ====================
USERS_CSV = "users.csv"


@app.post("/users/", response_model=User)
def create_user(user: User):
    users = get_all_from_csv(USERS_CSV)
    for u in users:
        if u and "id" in u and u["id"] == user.id:
            raise HTTPException(status_code=400, detail="El ID del usuario ya existe.")

    save_to_csv(USERS_CSV, user.model_dump())
    return user


@app.get("/users/", response_model=List[User])
def get_users():
    users = get_all_from_csv(USERS_CSV)
    return [u for u in users if u and (u.get("is_active") == "True" or u.get("is_active") is True)]


@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: str):
    users = get_all_from_csv(USERS_CSV)
    for u in users:
        if u and "id" in u and u["id"] == user_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")


@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    users = get_all_from_csv(USERS_CSV)
    found = False
    for u in users:
        if u and "id" in u and u["id"] == user_id:
            u["is_active"] = False
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="Usuario no encontrado para eliminar.")

    update_csv_file(USERS_CSV, users, ["id", "username", "email", "is_active"])
    return {"message": "Usuario marcado como inactivo (histórico conservado)."}


# ==================== MÓDULO DE BIBLIOTECA / DESEADOS (USER_GAMES) ====================
USER_GAMES_CSV = "user_games.csv"


@app.post("/user-games/", response_model=UserGame)
def create_user_game(user_game: UserGame):
    user_games = get_all_from_csv(USER_GAMES_CSV)
    for ug in user_games:
        if ug and "id" in ug and ug["id"] == user_game.id:
            raise HTTPException(status_code=400, detail="El ID de la relación ya existe.")

    save_to_csv(USER_GAMES_CSV, user_game.model_dump())
    return user_game


@app.get("/user-games/", response_model=List[UserGame])
def get_user_games():
    user_games = get_all_from_csv(USER_GAMES_CSV)
    return [ug for ug in user_games if ug and (ug.get("is_active") == "True" or ug.get("is_active") is True)]


@app.get("/user-games/user/{user_id}", response_model=List[UserGame])
def get_games_by_user(user_id: str):
    user_games = get_all_from_csv(USER_GAMES_CSV)
    results = [ug for ug in user_games if ug and "user_id" in ug and ug["user_id"] == user_id and (
                ug.get("is_active") == "True" or ug.get("is_active") is True)]
    return results


@app.delete("/user-games/{user_game_id}")
def delete_user_game(user_game_id: str):
    user_games = get_all_from_csv(USER_GAMES_CSV)
    found = False
    for ug in user_games:
        if ug and "id" in ug and ug["id"] == user_game_id:
            ug["is_active"] = False
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="Relación usuario-juego no encontrada.")

    update_csv_file(USER_GAMES_CSV, user_games, ["id", "user_id", "game_id", "status", "is_active"])
    return {"message": "Registro desvinculado exitosamente (histórico conservado)."}