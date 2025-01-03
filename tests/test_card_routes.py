from app.models.board import Board
from app.models.card import Card
import pytest

def test_get_cards_for_board(client, one_board, multiple_cards):
    # Act
    response = client.get(f"/boards/{one_board.id}/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "cards" in response_body
    assert len(response_body["cards"]) == 3

def test_create_card_for_board(client, one_board):
    # Act
    response = client.post(f"/boards/{one_board.id}/cards", json={"message": "new card", "like_count": 0})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "id" in response_body
    new_card = Card.query.get(response_body["id"])
    assert new_card
    assert new_card.message == "new card"
    assert new_card.like_count == 0
    assert new_card.board_id == one_board.id

def test_delete_card(client, one_card):
    # Act
    response = client.delete(f"/cards/{one_card.id}")

    # Assert
    assert response.status_code == 204
    assert response.data == b''  # Check that the response body is empty
    deleted_card = Card.query.get(one_card.id)
    assert deleted_card is None

def test_update_like_count_for_card(client, one_card):
    # Act
    response = client.patch(f"/cards/{one_card.id}/like")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["like_count"] == 1