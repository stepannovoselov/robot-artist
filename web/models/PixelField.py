from manage import db


class PixelField(db.Model):
    __tablename__ = 'pixels_field'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String, nullable=False)
