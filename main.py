from fastapi import FastAPI, HTTPException
from typing import List
from models.schemas import Game, User, LibraryWishlist
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


@app.put("/games/{game_id}", response_model=Game)
def update_game(game_id: str, updated_game: Game):
    games = get_all_from_csv(GAMES_CSV)
    found = False
    for i, g in enumerate(games):
        if g and "id" in g and g["id"] == game_id:
            games[i] = updated_game.model_dump()
            games[i]["id"] = game_id
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado para actualizar.")
    update_csv_file(GAMES_CSV, games, ["id", "title", "category", "price", "release_date", "is_active"])
    return updated_game


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

    update_csv_file(GAMES_CSV, games, ["id", "title", "category", "price", "release_date", "is_active"])
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


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, updated_user: User):
    users = get_all_from_csv(USERS_CSV)
    found = False
    for i, u in enumerate(users):
        if u and "id" in u and u["id"] == user_id:
            users[i] = updated_user.model_dump()
            users[i]["id"] = user_id
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="Usuario no encontrado para actualizar.")
    update_csv_file(USERS_CSV, users, ["id", "username", "email", "is_active"])
    return updated_user


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


# ==================== MÓDULO DE BIBLIOTECA / DESEADOS (LIBRARY_WISHLIST) ====================
LIBRARY_WISHLIST_CSV = "library_wishlist.csv"


@app.post("/library-wishlist/", response_model=LibraryWishlist)
def create_library_wishlist(item: LibraryWishlist):
    items = get_all_from_csv(LIBRARY_WISHLIST_CSV)
    for it in items:
        if it and "id" in it and it["id"] == item.id:
            raise HTTPException(status_code=400, detail="El ID del registro ya existe.")

    save_to_csv(LIBRARY_WISHLIST_CSV, item.model_dump())
    return item


@app.get("/library-wishlist/", response_model=List[LibraryWishlist])
def get_library_wishlists():
    items = get_all_from_csv(LIBRARY_WISHLIST_CSV)
    return [it for it in items if it and (it.get("is_active") == "True" or it.get("is_active") is True)]


@app.get("/library-wishlist/user/{user_id}", response_model=List[LibraryWishlist])
def get_library_wishlist_by_user(user_id: str):
    items = get_all_from_csv(LIBRARY_WISHLIST_CSV)
    results = [it for it in items if it and "user_id" in it and it["user_id"] == user_id and (
                it.get("is_active") == "True" or it.get("is_active") is True)]
    return results


@app.delete("/library-wishlist/{item_id}")
def delete_library_wishlist(item_id: str):
    items = get_all_from_csv(LIBRARY_WISHLIST_CSV)
    found = False
    for it in items:
        if it and "id" in it and it["id"] == item_id:
            it["is_active"] = False
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="Registro de biblioteca/deseados no encontrado.")

    update_csv_file(LIBRARY_WISHLIST_CSV, items, ["id", "user_id", "game_id", "status", "is_active"])
    return {"message": "Registro desvinculado exitosamente (histórico conservado)."}