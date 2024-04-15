from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User, Reservation
from datetime import datetime

reservation = Blueprint("reservation", __name__)

@login_required
@reservation.route('/reservation')
def index():
    return render_template('reservation.html')

@login_required
@reservation.route('/reservation', methods=["POST"])    
def reservation_post():
    user_id = current_user.id
    num_people = int(request.form["num_people"])
    datetimestring = request.form["date"]+ " " + request.form["time"]
    time = datetime.strptime(datetimestring, "%Y-%m-%d %H:%M")
    new_reservation = Reservation(user_id=user_id, num_people=num_people, time=time) # type: ignore
    try:
        db.session.add(new_reservation)
        db.session.commit()
        flash("Reservation successful")
        return redirect('/reservation')
    except Exception as e:
        print(e)
        return "Issue creating reservation"
