from app import db

class Reference(db.Model):
    __tablename__ = 'references'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    price = db.Column(db.Double)
    category = db.ForeignKey('categories.id')