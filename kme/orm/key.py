from kme.database import db


class Key(db.Model):  # type: ignore
    __tablename__ = "keys"
    key_id = db.Column(
        db.String,
        primary_key=True,
    )
    key_material = db.Column(
        db.String,
        nullable=False,
    )
