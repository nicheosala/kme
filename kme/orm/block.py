from kme.database import db


class Block(db.Model):  # type: ignore
    __tablename__ = "blocks"
    block_id = db.Column(
        db.String,
        primary_key=True
    )
