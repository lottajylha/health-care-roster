from application import db

class User(db.Model):

    __tablename__ = "account"
  
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    weekMin = db.Column(db.Integer, nullable=False)
    weekMax = db.Column(db.Integer, nullable=False)

    def __init__(self, name, username, password, position, weekMin = 0, weekMax = 0):
        self.name = name
        self.username = username
        self.password = password
        self.position = position
        self.weekMin = weekMin
        self.weekMax = weekMax
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True