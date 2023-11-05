import uuid
from utils import random_number
from typing import Union, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
class ShotBodyRequest(BaseModel):
    gameId: str
    userId: str
    x: int
    y: int
class GameBodyRequest(BaseModel):
    userId: str
class JoinGameBodyRequest(BaseModel):
    gameId: str
    userId: str

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

def init_game(first_player_id, second_player_id):
    new_game = {
        "id": first_player_id,
        "turn": first_player_id,
        "player1": {"id": first_player_id, "field": init_map(), "ships": 5},
        "player2": {"id": second_player_id, "field": init_map(), "ships": 5},
        "winner": None,
    }
    return new_game

def check_game_exist(gameId):
    if gameId not in games:
        raise HTTPException(status_code=400, detail="Game does not exist")

def check_user_exist(userId):
    if userId not in users:
        raise HTTPException(status_code=400, detail="User does not exist")

games = {}

users = {}

# Почитать про HTTP, GET vs POST
@app.post("/user")
def create_user():
    new_user_id = str(uuid.uuid4())
    users[new_user_id] = new_user_id
    return new_user_id


@app.post("/game")
def create_game(body: GameBodyRequest):
    check_user_exist(body.userId)
    new_game = {
        "id": body.userId,
        "turn": None,
        "player1": None,
        "player2": None,
        "winner": None,
    }
    games[body.userId] = new_game
    return new_game


@app.post("/game/join")
def join_game(body: JoinGameBodyRequest):
    check_user_exist(body.userId)
    check_game_exist(body.gameId)
    game = games[body.gameId]
    if game["player2"] is not None:
        raise HTTPException(status_code=400, detail="Game already filled")
    games[body.gameId] = init_game(body.gameId, body.userId)
    return games[body.gameId]


@app.get("/game")
def get_game(gameId: str):
    check_game_exist(gameId)
    return games[gameId]


@app.post("/game/shot")
def make_turn(body: ShotBodyRequest):
    gameId = body.gameId
    userId = body.userId
    x = body.x
    y = body.y
    check_game_exist(gameId)
    current_game = games[gameId]
    if current_game["winner"] is not None:
        raise HTTPException(status_code=400, detail="Game ended")
    print("current_game=",current_game)
    print("userId=",userId)
    if current_game["turn"] != userId:
        raise HTTPException(
            status_code=400, detail="Another player's turn"
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
    return "OK"
