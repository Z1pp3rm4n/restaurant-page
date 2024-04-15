from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from models import db, Reservation, Type
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/profile')
@login_required
def profile():
    return current_user.name 


@main.route('/menu')
def menu():
    dish_groups = Type.query.order_by(Type.name).all()
    return render_template("menu.html", dish_groups=dish_groups)



@main.route('/reservation')
@login_required
def reservation():
    return render_template('reservation.html')

@main.route('/reservation', methods=["POST"])    
@login_required
def reservation_post():
    user_id = current_user.id
    num_people = int(request.form["num_people"])
    datetimestring = request.form["date"]+ " " + request.form["time"]
    time = datetime.strptime(datetimestring, "%Y-%m-%d %H:%M")
    new_reservation = Reservation(user_id=user_id, num_people=num_people, time=time) # type: ignore
    try:
        db.session.add(new_reservation)
        db.session.commit()
        flash("Reservation successful", 'success')
        return redirect('/reservation')
    except Exception as e:
        print(e)
        return "Issue creating reservation"