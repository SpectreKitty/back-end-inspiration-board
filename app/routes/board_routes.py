from flask import Blueprint, request, abort, make_response, Response
from ..db import db
from app.models.board import Board
from app.models.card import Card

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")