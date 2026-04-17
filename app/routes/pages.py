from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.alert import Alert
from app.models.cattle import Cattle
from app.models.device import Device
from app.models.milk_yield import MilkYield
from app.extensions import db

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

@bp.route("/milk-yield", methods=["GET", "POST"])
@login_required
def milk_yield():

    if request.method == "POST":
        cattle_id = request.form.get("cattle_id")
        yield_liters = request.form.get("yield_liters")
        record_date = request.form.get("record_date")
        notes = request.form.get("notes")

        new_record = MilkYield(
            cattle_id=cattle_id,
            yield_liters=yield_liters,
            record_date=record_date,
            notes=notes
        )

        db.session.add(new_record)
        db.session.commit()

        flash("Milk yield added successfully!", "success")
        return redirect(url_for("pages.milk_yield"))

    cattle = Cattle.query.filter_by(owner_id=current_user.id).all()

    records = MilkYield.query.order_by(
        MilkYield.record_date.asc()
    ).all()

    chart_labels = [str(r.record_date) for r in records]
    chart_values = [float(r.yield_liters) for r in records]

    return render_template(
        "milk_yield.html",
        cattle=cattle,
        records=records,
        chart_labels=chart_labels,
        chart_values=chart_values
    )