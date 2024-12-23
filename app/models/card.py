from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey
from .board import Board

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    like_count: Mapped[int]
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"))
    board: Mapped["Board"] = relationship(back_populates="cards")

    def to_dict(self):
        card_dict = {
            "id": self.id,
            "message": self.message,
            "like_count": self.like_count,
            "board": self.board.id,
        }

        return card_dict
    
    @classmethod
    def from_dict(cls, card_data):
        new_card = cls(
            message=card_data["message"],
            like_count=card_data.get("like_count", 0),
            board_id=card_data["board_id"],
        )
        return new_card
    