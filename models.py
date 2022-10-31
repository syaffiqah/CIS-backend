from unicodedata import name
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CustomerModel(db.Model):
    _tablename_ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    ic = db.Column(db.Integer())
    phone = db.Column(db.String(12))
    email = db.Column(db.String)

    def __init__(self, name, ic, phone, email):
        self.name = name
        self.ic = ic
        self.phone = phone
        self.email = email
    
    def json(self):
        return {"id":self.id,"name":self.name,"ic":self.ic,"phone":self.phone,"email":self.email}

# An Empty Array to hold our customer
new_Customer_arr = []