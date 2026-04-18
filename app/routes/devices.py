import os
from uuid import uuid4
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.cattle import Cattle
from app.models.device import Device
from app.models.health_data import HealthData

bp = Blueprint("devices", __name__)

# Devices List Page
@bp.route("/devices")
@login_required
def devices_page():

    devices = Device.query.join(Cattle)\
        .filter(Cattle.owner_id == current_user.id)\
        .all()

    return render_template("devices.html", devices=devices)


# Add Device
@bp.route("/devices/add", methods=["GET", "POST"])
@login_required
def add_device():

    cattle = Cattle.query.filter_by(owner_id=current_user.id).all()

    if request.method == "POST":

        device = Device(
            device_id=request.form["device_id"],
            device_name=request.form["device_name"],
            device_details=request.form["device_details"],
            device_serial=request.form["device_serial"],
            cattle_id=request.form["cattle_id"],
            status="Active"
        )

        db.session.add(device)
        db.session.commit()

        flash("Device Added Successfully", "success")
        return redirect(url_for("devices.devices_page"))

    return render_template("device_form.html", cattle=cattle)