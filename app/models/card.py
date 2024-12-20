from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey

class Card(db.model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    like_count: Mapped[int]
    board_id: Mapped[int] = mapped_column(ForeignKey("board.board_id"))
    board: Mapped["Board"] = relationship(back_populates="cards")

    def to_dict(self):
        card_dict = {
            "card_id": self.card_id,
            "message": self.message,
            "like_count": self.like_count,
            "board_id": self.board_id,
        }

        return card_dict
    
    @classmethod
    def from_dict(cls, card_data):
        new_card = cls(
            message=card_data["message"],
            like_count=card_data["like_count"],
            board_id=card_data["board_id"],
        )
        return new_card
    