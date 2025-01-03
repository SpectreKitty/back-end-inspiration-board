from flask import Blueprint, Response
from .route_utilities import validate_model
from app.models.card import Card
from ..db import db

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<card_id>/like")
def update_like_count_for_card(card_id):
    card = validate_model(Card, card_id)

    card.like_count += 1
    
    db.session.commit()

    return card.to_dict()