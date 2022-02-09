from app.db import db


class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    world_rank = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    score = db.Column(db.Numeric(4,1), nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    def __repr__(self):
        return f'University: {self.id} {self.name}'
