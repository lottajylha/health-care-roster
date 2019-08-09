from application import db

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    day = db.Column(db.String(20), nullable=False)
    hour =  db.Column(db.String(5), nullable=False)
    accepted = db.Column(db.Boolean, nullable=False)
    doctorsNeeded = db.Column(db.Integer, nullable=False)
    nursesNeeded = db.Column(db.Integer, nullable=False)
    practicalNursesNeeded = db.Column(db.Integer, nullable=False)

    def __init__(self, day, hour, doctorsNeeded = 0, nursesNeeded = 0, practicalNursesNeeded = 0):
        self.day = day
        self.hour = hour
        self.accepted = False
        self.doctorsNeeded = doctorsNeeded
        self.nursesNeeded = doctorsNeeded
        self.practicalNursesNeeded = doctorsNeeded