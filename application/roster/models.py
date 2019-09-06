from application import db
from sqlalchemy.sql import text
from application.auth.models import User, association_table

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    day = db.Column(db.String(20), nullable=False)
    hour =  db.Column(db.String(5), nullable=False)
    accepted = db.Column(db.Boolean, nullable=False)
    doctors_needed = db.Column(db.Integer, nullable=False)
    nurses_needed = db.Column(db.Integer, nullable=False)
    practical_nurses_needed = db.Column(db.Integer, nullable=False)
    users = db.relationship(
        "User",
        secondary=association_table,
        back_populates="shifts")

    def __init__(self, day, hour, doctors_needed = 0, nurses_needed = 0, practical_nurses_needed = 0):
        self.day = day
        self.hour = hour
        self.accepted = False
        self.doctors_needed = doctors_needed
        self.nurses_needed = nurses_needed
        self.practical_nurses_needed = practical_nurses_needed

    @staticmethod
    def find_employees_in_shift(shift_id):
        stmt = text("SELECT Account.name, Account.position"
                    " FROM account JOIN usershift ON usershift.account_id = account.id"
                    " JOIN shift ON usershift.shift_id = :param AND shift.id = :param"
                    " GROUP BY Account.name, Account.position;").params(param=shift_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            rowstr = row[0] + " (" + row[1] + ")"
            response.append(rowstr)

        return response
    
    @staticmethod
    def count_employees_in_shift(shift_id, position):
        stmt = text("SELECT COUNT(*) FROM (SELECT Account.name, Account.position"
                    " FROM Account, Usershift WHERE Usershift.shift_id = :shiftparam"
                    " AND Usershift.account_id = account.id AND Account.position = :positionparam"
                    " GROUP BY Account.name, Account.position) AS alias;").params(shiftparam=shift_id, positionparam=position)
        res = db.engine.execute(stmt)
        return res.first()[0]

    @staticmethod
    def practical_nurses_needed_shift(shift_id):
        stmt = text("SELECT practical_nurses_needed FROM shift"
                    " WHERE shift.id = :shiftparam;").params(shiftparam=shift_id)
        res = db.engine.execute(stmt)
        value = 0
        for row in res:
            value = row[0]
        return int(value)

    @staticmethod
    def nurses_needed_shift(shift_id):
        stmt = text("SELECT nurses_needed FROM shift"
                    " WHERE shift.id = :shiftparam;").params(shiftparam=shift_id)
        res = db.engine.execute(stmt)
        value = 0
        for row in res:
            value = row[0]
        return int(value)


    @staticmethod
    def doctors_needed_shift(shift_id):
        stmt = text("SELECT doctors_needed FROM shift"
                    " WHERE shift.id = :shiftparam;").params(shiftparam=shift_id)
        res = db.engine.execute(stmt)
        value = 0
        for row in res:
            value = row[0]
        return int(value)

    @staticmethod
    def status(shift_id):
        practicalnurses = Shift.practical_nurses_needed_shift(shift_id) - Shift.count_employees_in_shift(shift_id, 'Practical nurse')
        nurses = Shift.nurses_needed_shift(shift_id) - Shift.count_employees_in_shift(shift_id, 'Nurse')
        doctors = Shift.doctors_needed_shift(shift_id) - Shift.count_employees_in_shift(shift_id, 'Doctor')
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

    @staticmethod
    def delete_shift(shiftid):
        stmt = text("DELETE FROM usershift WHERE shift_id = :param;").params(param=shiftid)
        res = db.engine.execute(stmt)
        stmt = text("DELETE FROM shift WHERE shift.id = :param;").params(param=shiftid)
        res = db.engine.execute(stmt)
        