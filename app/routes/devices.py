import os
from uuid import uuid4
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.cattle import Cattle
from app.models.device import Device
from app.models.health_data import HealthData

# bp = Blueprint("cattle", __name__)
bp = Blueprint("devices", __name__)

def save_photo(file):
    if not file or file.filename == "":
        return None
    filename = secure_filename(file.filename)
    unique_name = f"{uuid4().hex}_{filename}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
    file.save(path)
    return f"uploads/cattle/{unique_name}"

@bp.route("/cattle")
@login_required
def list_cattle():
    cattle = Cattle.query.filter_by(owner_id=current_user.id).order_by(Cattle.id.desc()).all()
    return render_template("cattle.html", cattle=cattle)

@bp.route("/cattle/add", methods=["GET", "POST"])
@login_required
def add_cattle():
    if request.method == "POST":
        cattle_tag = request.form.get("cattle_tag")
        breed = request.form.get("breed")
        age = request.form.get("age")
        weight = request.form.get("weight")
        photo_path = save_photo(request.files.get("photo"))

        cattle = Cattle(
            cattle_tag=cattle_tag,
            breed=breed,
            age=int(age),
            weight=float(weight),
            photo=photo_path,
            owner_id=current_user.id
        )
        db.session.add(cattle)
        db.session.commit()

        flash("Cattle added successfully", "success")
        return redirect(url_for("cattle.list_cattle"))

    return render_template("cattle_form.html", cattle=None)

@bp.route("/cattle/<int:cattle_id>")
@login_required
def cattle_detail(cattle_id):
    cattle = Cattle.query.filter_by(id=cattle_id, owner_id=current_user.id).first_or_404()
    latest = HealthData.query.filter_by(cattle_id=cattle.id).order_by(HealthData.timestamp.desc()).first()
    device = Device.query.filter_by(cattle_id=cattle.id).first()
    history = HealthData.query.filter_by(cattle_id=cattle.id).order_by(HealthData.timestamp.asc()).all()[-15:]
    return render_template("cattle_detail.html", cattle=cattle, latest=latest, device=device, history=history)

@bp.route("/cattle/<int:cattle_id>/edit", methods=["GET", "POST"])
@login_required
def edit_cattle(cattle_id):
    cattle = Cattle.query.filter_by(id=cattle_id, owner_id=current_user.id).first_or_404()

    if request.method == "POST":
        cattle.cattle_tag = request.form.get("cattle_tag")
        cattle.breed = request.form.get("breed")
        cattle.age = int(request.form.get("age"))
        cattle.weight = float(request.form.get("weight"))

        new_photo = save_photo(request.files.get("photo"))
        if new_photo:
            cattle.photo = new_photo

        db.session.commit()
        flash("Cattle updated successfully", "success")
        return redirect(url_for("cattle.cattle_detail", cattle_id=cattle.id))

    return render_template("cattle_form.html", cattle=cattle)

@bp.route("/cattle/<int:cattle_id>/delete", methods=["POST"])
@login_required
def delete_cattle(cattle_id):
    cattle = Cattle.query.filter_by(id=cattle_id, owner_id=current_user.id).first_or_404()
    db.session.delete(cattle)
    db.session.commit()
    flash("Cattle deleted successfully", "success")
    return redirect(url_for("cattle.list_cattle"))