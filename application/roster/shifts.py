from application import db
from sqlalchemy.sql import text
from application.auth.models import User, association_table

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    day = db.Column(db.String(20), nullable=False)
    hour =  db.Column(db.String(5), nullable=False)
    accepted = db.Column(db.Boolean, nullable=False)
    doctorsNeeded = db.Column(db.Integer, nullable=False)
    nursesNeeded = db.Column(db.Integer, nullable=False)
    practicalNursesNeeded = db.Column(db.Integer, nullable=False)
    users = db.relationship(
        "User",
        secondary=association_table,
        back_populates="shifts")

    def __init__(self, day, hour, doctorsNeeded = 0, nursesNeeded = 0, practicalNursesNeeded = 0):
        self.day = day
        self.hour = hour
        self.accepted = False
        self.doctorsNeeded = doctorsNeeded
        self.nursesNeeded = nursesNeeded
        self.practicalNursesNeeded = practicalNursesNeeded

    @staticmethod
    def find_users(shift_id):
        stmt = text("SELECT Account.name, Account.position"
                    " FROM account JOIN usershift ON usershift.account_id = account.id"
                    " JOIN shift ON usershift.shift_id = :param AND shift.id = :param"
                    " GROUP BY Account.name;").params(param=shift_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            rowstr = row[0] + " (" + row[1] + ")"
            response.append(rowstr)

        return response
    
    @staticmethod
    def employees_in_shift(shift_id, position):
        stmt = text("SELECT COUNT(*) FROM (SELECT Account.name, Account.position"
                    " FROM account, Usershift WHERE Usershift.shift_id = :shiftparam"
                    " AND Usershift.account_id = account.id "
                    " AND Account.position = :positionparam"
                    " GROUP BY Account.name);").params(shiftparam=shift_id, positionparam=position)
        res = db.engine.execute(stmt)
        return res.first()[0]

    @staticmethod
    def practicalNursesNeeded_shift(shift_id):
        stmt = text("SELECT practicalNursesNeeded FROM shift"
                    " WHERE shift.id = :shiftparam;").params(shiftparam=shift_id)
        res = db.engine.execute(stmt)
        value = 0
        for row in res:
            value = row[0]
        return int(value)

    @staticmethod
    def nursesNeeded_shift(shift_id):
        stmt = text("SELECT nursesNeeded FROM shift"
                    " WHERE shift.id = :shiftparam;").params(shiftparam=shift_id)
        res = db.engine.execute(stmt)
        value = 0
        for row in res:
            value = row[0]
        return int(value)


    @staticmethod
    def doctorsNeeded_shift(shift_id):
        stmt = text("SELECT doctorsNeeded FROM shift"
                    " WHERE shift.id = :shiftparam;").params(shiftparam=shift_id)
        res = db.engine.execute(stmt)
        value = 0
        for row in res:
            value = row[0]
        return int(value)

    @staticmethod
    def status(shift_id):
        practicalnurses = Shift.practicalNursesNeeded_shift(shift_id) - Shift.employees_in_shift(shift_id, 'Practical nurse')
        nurses = Shift.nursesNeeded_shift(shift_id) - Shift.employees_in_shift(shift_id, 'Nurse')
        doctors = Shift.doctorsNeeded_shift(shift_id) - Shift.employees_in_shift(shift_id, 'Doctor')
        if nurses == 0 and doctors == 0 and practicalnurses == 0:
            return "Accepted"
        else:
            statusstr = ""
            if doctors > 0:
                statusstr += (str(doctors) + " doctors missing ")
            if nurses > 0:
                statusstr += (str(nurses) + " nurses missing ")
            if practicalnurses > 0:
                statusstr += (str(practicalnurses) + " practical nurses missing ")
            return statusstr
