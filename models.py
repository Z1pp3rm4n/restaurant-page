from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from init import db, admin
from flask_admin.contrib.sqla import ModelView



class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    num_people = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="reservations")

    def __repr__(self):
        return "<Reservation %r>" % self.id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    reservations = db.relationship('Reservation', back_populates="user")

class ReservationView(ModelView):
    form_columns=["time", "num_people", "user"]
    column_list=["time", "num_people", "user.name", "user.email"]

admin.add_view(ReservationView(Reservation, db.session))
admin.add_view(ModelView(User, db.session))

