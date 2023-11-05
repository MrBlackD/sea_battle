from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_shot():
    response = client.post("/user")
    assert response.status_code == 200
    player1 = response.json()
    print(player1)

    response = client.post("/game", json={"userId": player1})
    print(response.json())
    assert response.status_code == 200

    response = client.post("/user")
    assert response.status_code == 200
    player2 = response.json()

    response = client.post("/game/join", json={"gameId": player1, "userId": player2})
    assert response.status_code == 200
    print(response.json())
    game = response.json()
    x = y = None
    field = game["player2"]["field"]
    for i, row in enumerate(field):
        for j, value in enumerate(row):
            if value == 1:
                x = i
                y = j
                break
        if x is not None:
            break
    print("x=",x)
    print("y=",y)
    response = client.post(
        "/game/shot", json={"gameId": player1, "userId": player1, "x": x, "y": y}
    )
    print(response.json())
    assert response.status_code == 200

    response = client.get("/game?gameId=" + player1)
    print(response.json())
    assert response.status_code == 200
