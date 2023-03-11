from ..utils import db

class User(db.Model):
    __tablename__ = 'users'
    id =db.Column(db.Integer(), primary_key=True)
    username =db.Column(db.String(45), nullable=False,unique=True)
    email =db.Column(db.String(50), nullable=False,unique=True)
    password_hash =db.Column(db.Text(), nullable=False)
    is_staff =db.Column(db.Boolean(), default=False)
    is_active =db.Column(db.Boolean(), default=False)
    order=db.relationship('Order',backref='user',lazy=True)#every user to its order
    
    def __repr__(self):
        return f"<User {self.username}>"
 
    
    #Add new user every time a request is made
    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)