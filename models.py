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
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    reservations = db.relationship('Reservation', back_populates="user")
    orders = db.relationship("Order", back_populates="user")


class Dish(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo_url = db.Column(db.String(300))
    order_items = db.relationship("OrderItem", back_populates="dish")

    type_id = db.Column(db.Integer, db.ForeignKey("type.id"))
    dish_type = db.relationship("Type", back_populates="dishes")

class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    dishes = db.relationship("Dish", back_populates="dish_type")

    def __str__(self):
        return self.name

    

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order")      

class OrderItem(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey("dish.id"))
    quantity = db.Column(db.Integer, nullable=False)
    dish = db.relationship("Dish", back_populates="order_items")
    order = db.relationship("Order", back_populates="order_items")


class ReservationView(ModelView):
    form_columns=["time", "num_people", "user"]
    column_list=["time", "num_people", "user.name", "user.email"]

# class UserView(ModelView)
#     column_list = ["name, "email", "password", "reserva"]

admin.add_view(ReservationView(Reservation, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Dish, db.session))
admin.add_view(ModelView(Type, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(OrderItem, db.session))
