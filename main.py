from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/about')
def about():
    return render_template("about.html")

@login_required
@main.route('/profile')
def profile():
    return current_user.name 


@login_required
@main.route('/reservation')
def reservation():
    return render_template('reservation.html')

@login_required
@main.route('/reservation', methods=["POST"])    
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