import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.card import Card
from app.models.board import Board

load_dotenv()

@pytest.fixture
def app():
    # create the app with a test configuration
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# This fixture gets called in every test that
# references "one_card"
# This fixture creates a card and saves it in the database
@pytest.fixture
def one_card(app, one_board):
    new_card = Card(message="test message", like_count=0, board_id=one_board.id)
    db.session.add(new_card)
    db.session.commit()
    return new_card


# This fixture gets called in every test that
# references "one_board"
# This fixture creates a board and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(title="test board", owner="team 6")
    db.session.add(new_board)
    db.session.commit()
    return new_board


@pytest.fixture
def multiple_cards(app, one_board):
    cards = [
        Card(message="test message 1", like_count=2, board_id=one_board.id),
        Card(message="test message 2", like_count=5, board_id=one_board.id),
        Card(message="test message 3", like_count=0, board_id=one_board.id)
    ]
    db.session.add_all(cards)
    db.session.commit()
    return cards

@pytest.fixture
def multiple_boards(app):
    boards = [
        Board(title="Board 1", owner="Owner 1"),
        Board(title="Board 2", owner="Owner 2"),
        Board(title="Board 3", owner="Owner 3")
    ]
    db.session.add_all(boards)
    db.session.commit()
    return boards
