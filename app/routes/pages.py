from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models.alert import Alert
from app.models.cattle import Cattle
from app.models.device import Device

bp = Blueprint("pages", __name__)

@bp.route("/notifications")
@login_required
def notifications():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(100).all()
    return render_template("notifications.html", alerts=alerts)

@bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@bp.route("/vaccination-schedule")
@login_required
def vaccination_schedule():
    return render_template("vaccination.html")

@bp.route("/contact-vet", methods=["GET", "POST"])
@login_required
def contact_vet():
    sent = False
    if request.method == "POST":
        sent = True
    return render_template("contact_vet.html", sent=sent)

@bp.route("/milk-yield")
@login_required
def milk_yield():
    cattle = Cattle.query.filter_by(owner_id=current_user.id).all()
    return render_template("milk_yield.html", cattle=cattle)