from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Board(db.Model):
    board_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]
    cards: Mapped[list["Card"]] = relationship(back_populates="board")

    def to_dict(self):
        board_to_dict = {
            "board_id": self.board_id,
            "title": self.title, 
            "owner": self.owner,
        }

        return board_to_dict
    
    @classmethod
    def from_dict(cls, board_data):
        new_board = cls(
            title=board_data["title"],
            owner=board_data["owner"],
        )
        return new_board