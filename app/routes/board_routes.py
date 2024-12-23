from flask import Blueprint, request, abort, make_response
from .route_utilities import create_model, validate_model
from ..db import db
from app.models.board import Board
from app.models.card import Card

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.post("")
def create_board():
    request_body = request.get_json()

    try:
        new_board = Board.from_dict(request_body)

    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_board)
    db.session.commit()

    return {"board": new_board.to_dict()}, 201

@bp.get("")
def get_all_boards():
    query = db.select(Board)
    boards = db.session.scalars(query)
    boards_response = [board.to_dict() for board in boards]
    return boards_response

@bp.get("/<board_id>/cards")
def get_cards_from_board(board_id):
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
    return create_model(Card, request_body)