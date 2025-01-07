from app.models.board import Board
from app.models.card import Card
import pytest

def test_get_board_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_board_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [{
        "id": 1,
        "owner": "team 6",
        "title": "test board"
    }]

def test_get_all_boards_on_multiple_boards(client, multiple_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
            {"id": 1,
            "title": "Board 1",
            "owner" : "Owner 1"},
            {"id": 2,
            "title": "Board 2",
            "owner" : "Owner 2"},
            {"id": 3,
            "title": "Board 3",
            "owner" : "Owner 3"}
            ]

def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 404
    assert 'message' in response_body
    assert response_body['message'] == "Board 1 not found"

def test_create_board(client):
    # Act
    response = client.post("/boards", json={"title": "test board", "owner": "team 6"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
        "id": 1,
        "title": "test board",
        "owner": "team 6",
    }}
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "test board"
    assert new_board.owner == "team 6"

def test_create_board_missing_title(client):
    # Act
    response = client.post("/boards", json={"owner": "team 6"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid data: title and owner cannot be blank"}

def test_create_board_missing_owner(client):
    # Act
    response = client.post("/boards", json={"title": "test board"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid data: title and owner cannot be blank"}
