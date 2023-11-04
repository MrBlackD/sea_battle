import uuid
from utils import random_number

from typing import Union, List

from fastapi import FastAPI, HTTPException

app = FastAPI()

def init_map():
    battle_map = [[0 for i in range(5)] for i in range(5)]
    placed_ships = 0
    while placed_ships != 5:
        x = random_number(0, 4)
        y = random_number(0, 4)
        if battle_map[x][y] == 0:
            battle_map[x][y] = 1
            placed_ships += 1
    return battle_map


def init_game(game_id, first_player_id, second_player_id):
    new_game = {
        "id": game_id,
        "turn": first_player_id,
        "player1": {"id": first_player_id, "field": init_map(), "ships": 5},
        "player2": {"id": second_player_id, "field": init_map(), "ships": 5},
        "winner": None
    }
    print(new_game)
    return new_game

rooms = []

games = []


@app.get("/room/create")
def create_room(userId: Union[str, None] = None):
    new_room = {"player1": userId, "player2": None, "gameId": None}
    rooms.append(new_room)
    return new_room


@app.get("/room/join")
def join_room(roomId: str, userId: str):
    print(rooms)
    for room in rooms:
        if room["player1"] == roomId:
            if room["player2"] is not None:
                raise HTTPException(status_code=400, detail="Room already filled")
            else:
                room["player2"] = userId
                game_id = str(uuid.uuid4())
                room["gameId"] = game_id
                new_game = init_game(game_id, room["player1"], room["player2"])
                games.append(new_game)

                return room
    raise HTTPException(status_code=400, detail="Room not found")


@app.get("/room")
def view_room(roomId: str):
    for room in rooms:
        if room["player1"] == roomId:
            return room
    raise HTTPException(status_code=400, detail="Room not found")


@app.get("/game")
def view_game(gameId: str):
    for game in games:
        if game["id"] == gameId:
            return game
    raise HTTPException(status_code=400, detail="Game not found")


@app.get("/game/{gameId}/shot")
def shot(gameId: str, userId: str, x: int, y: int):
    current_game = None
    for game in games:
        if game["id"] == gameId:
            current_game = game
            break
    if current_game is None:
        raise HTTPException(status_code=400, detail="Game not found")
    if current_game["winner"] is not None:
        raise HTTPException(status_code=400, detail="Game ended")
    if current_game["turn"] != userId:
        raise HTTPException(
            status_code=400, detail="Another player's turn, motherf*cker"
        )
    if x > 4 or x < 0 or y > 4 or y < 0:
        raise HTTPException(status_code=400, detail="Out of field")
    target_player = current_game["player1"]
    if current_game["player1"]["id"] == userId:
        target_player = current_game["player2"]
    cell = target_player["field"][x][y]
    if cell == 1:
        target_player["ships"] -= 1
    target_player["field"][x][y] = -1

    if target_player["ships"] == 0:
        current_game["winner"] = userId
    else:
        current_game["turn"] = target_player["id"]

def new_good_function():
    pass
