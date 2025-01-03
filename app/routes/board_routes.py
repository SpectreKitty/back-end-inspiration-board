from flask import Blueprint, Response, request, abort, make_response
from .route_utilities import create_model, validate_model
from ..db import db
from app.models.board import Board
from app.models.card import Card
import requests
import os

SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]
SLACK_API_URL = os.environ["SLACK_API_URL"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")


@bp.post("")
def create_board():
    request_body = request.get_json()

    # Validate title and owner are not blank
    if not request_body.get("title") or not request_body.get("owner"):
        response = {"details": "Invalid data: title and owner cannot be blank"}
        abort(make_response(response, 400))

    try:
        new_board = Board.from_dict(request_body)

    except KeyError as error:
        response = {"details": f"Invalid data: {error}"}
        abort(make_response(response, 400))

    db.session.add(new_board)
    db.session.commit()

    return {"board": new_board.to_dict()}, 201


@bp.get("")
def read_all_boards():
    query = db.select(Board)
    boards = db.session.scalars(query)
    boards_response = [board.to_dict() for board in boards]
    return boards_response

@bp.delete("")
def delete_all_boards():
    Card.query.delete()
    Board.query.delete()
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.get("/<board_id>")
def read_one_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict(), 200


@bp.get("/<board_id>/cards")
def read_cards_for_board(board_id):
    board = validate_model(Board, board_id)
    cards = [card.to_dict() for card in board.cards]

    response = board.to_dict()
    response["cards"] = cards
    return response


@bp.post("/<board_id>/cards")
def create_card_for_board(board_id):
    board = validate_model(Board, board_id)

    request_body = request.get_json()
    request_body["board_id"] = board.id

    new_card = create_model(Card, request_body)
    post_to_slack(new_card)

    return new_card


def post_to_slack(card):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    }

    data = {
        "channel": SLACK_CHANNEL,
        "text": f"New card added to board {card.board.title}: {card.message}",
    }

    r = requests.post(SLACK_API_URL, headers=headers, data=data)
