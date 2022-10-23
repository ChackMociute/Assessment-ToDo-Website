from app import db

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    # Wanted to cap code strings at 8 for UoL courses but decided on a
    # greater limit for possible applicability at other universities
    code = db.Column(db.String(20))
    deadline = db.Column(db.Date)
    description = db.Column(db.String(1000))
    complete = db.Column(db.Boolean)