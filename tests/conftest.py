import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.card import Card
from app.models.board import Board
from datetime import datetime

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


# # This fixture gets called in every test that
# # references "three_tasks"
# # This fixture creates three tasks and saves
# # them in the database
# @pytest.fixture
# def three_tasks(app):
#     db.session.add_all([
#         Task(title="Water the garden 🌷", 
#              description="", 
#              completed_at=None),
#         Task(title="Answer forgotten email 📧", 
#              description="", 
#              completed_at=None),
#         Task(title="Pay my outstanding tickets 😭", 
#              description="", 
#              completed_at=None)
#     ])
#     db.session.commit()



# This fixture gets called in every test that
# references "one_board"
# This fixture creates a board and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(title="test board", owner="team 6")
    db.session.add(new_board)
    db.session.commit()


# This fixture gets called in every test that
# references "one_task_belongs_to_one_goal"
# This fixture creates a task and a goal
# It associates the goal and task, so that the
# goal has this task, and the task belongs to one goal
# @pytest.fixture
# def one_task_belongs_to_one_goal(app, one_goal, one_task):
#     task = Task.query.first()
#     goal = Goal.query.first()
#     goal.tasks.append(task)
#     db.session.commit()
