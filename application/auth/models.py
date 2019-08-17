from application import db
from sqlalchemy.sql import text

association_table = db.Table('usershift',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
    db.Column('shift_id', db.Integer, db.ForeignKey('shift.id'))
)


class User(db.Model):

    __tablename__ = "account"
  
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    weekmin = db.Column(db.Integer, nullable=False)
    weekmax = db.Column(db.Integer, nullable=False)
    shifts = db.relationship(
        "Shift",
        secondary=association_table,
        back_populates="users")

    def __init__(self, name, username, password, position, weekmin = 0, weekmax = 0):
        self.name = name
        self.username = username
        self.password = password
        self.position = position
        self.weekmin = weekmin
        self.weekmax = weekmax
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def find_users():
        stmt = text("SELECT * FROM account;")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append([row[0], row[1]])
        return response

    @staticmethod
    def get_position(user_id):
        stmt = text("SELECT position"
                    " FROM account WHERE account.id = :param;").params(param=user_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            rowstr = str(row[0])
            response.append(rowstr)
        
        return str(response[0])

    @staticmethod
    def get_weekminmax(user_id):
        stmt = text("SELECT weekmin, weekmax from account"
                    " WHERE account.id = :idparam;").params(idparam=user_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append(int(row[0]))

        return response

    @staticmethod
    def set_weekminmax(user_id, weekmin, weekmax):
        stmt = text("UPDATE account set weekmin = :minparam,"
                    " weekmax = :maxparam"
                    " WHERE account.id = :idparam;").params(minparam=weekmin, maxparam=weekmax, idparam=user_id)
        res = db.engine.execute(stmt)

    @staticmethod
    def find_user_shifts(user_id):
        user_position = User.get_position(user_id)
        
        stmt = text("SELECT Shift.day, Shift.hour"
                    " FROM shift JOIN usershift ON usershift.shift_id = shift.id"
                    " JOIN account ON usershift.account_id = :param AND account.id = :param"
                    " GROUP BY shift.day;").params(param=user_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append([row[0], row[1]])
        return response

    @staticmethod
    def user_has_shift(user_id, shiftid):
        stmt = text("SELECT * FROM usershift"
                    " WHERE account_id = :userparam"
                    " AND shift_id = :shiftparam;").params(userparam=user_id,shiftparam=shiftid)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({row[0], row[1]})
        if (len(response) == 0):
            return False
        else:
            return True
    
    @staticmethod
    def add_shift(user_id, shiftid):
        if (not User.user_has_shift(user_id, shiftid)):
            stmt = text("INSERT INTO usershift (account_id, shift_id)"
                        " VALUES (:userparam, :shiftparam);").params(userparam=user_id,shiftparam=shiftid)
            res = db.engine.execute(stmt)

    @staticmethod
    def remove_shift(user_id, shiftid):
        if User.user_has_shift(user_id, shiftid):
            stmt = text("DELETE FROM usershift WHERE"
                        " account_id = :userparam"
                        " AND shift_id = :shiftparam;").params(userparam=user_id,shiftparam=shiftid)
            res = db.engine.execute(stmt)
    
