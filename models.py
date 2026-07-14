from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tourist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15))
    password = db.Column(db.String(200))
    emergency_contact = db.Column(db.String(15))


