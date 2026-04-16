from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.cattle import Cattle
from app.models.device import Device
from app.models.health_data import HealthData
from app.models.alert import Alert
from app.services.simulator import simulate_for_all_cattle, dashboard_summary, health_status_from_latest

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/dashboard/summary", methods=["GET"])
@login_required
def api_dashboard_summary():
    return jsonify(dashboard_summary())

@bp.route("/cattle", methods=["GET"])
@login_required
def api_cattle():
    cattle = Cattle.query.filter_by(owner_id=current_user.id).order_by(Cattle.id.desc()).all()
    return jsonify([c.to_dict() for c in cattle])

@bp.route("/devices", methods=["GET"])
@login_required
def api_devices():
    devices = (
        Device.query.join(Device.cattle)
        .filter_by(owner_id=current_user.id)
        .order_by(Device.id.desc())
        .all()
    )
    return jsonify([d.to_dict() for d in devices])

@bp.route("/health-data", methods=["GET"])
@login_required
def api_health_data():
    latest = HealthData.query.order_by(HealthData.timestamp.desc()).limit(25).all()
    return jsonify([h.to_dict() for h in latest])

@bp.route("/health-data/simulate", methods=["POST"])
@login_required
def api_health_data_simulate():
    created = simulate_for_all_cattle()
    return jsonify({"success": True, "created": created})

@bp.route("/health-data/<int:cattle_id>/history", methods=["GET"])
@login_required
def api_cattle_history(cattle_id):
    cattle = Cattle.query.filter_by(id=cattle_id, owner_id=current_user.id).first_or_404()
    rows = HealthData.query.filter_by(cattle_id=cattle.id).order_by(HealthData.timestamp.asc()).all()
    return jsonify([r.to_dict() for r in rows])

@bp.route("/alerts", methods=["GET"])
@login_required
def api_alerts():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(25).all()
    return jsonify([a.to_dict() for a in alerts])

@bp.route("/alerts/read/<int:alert_id>", methods=["POST"])
@login_required
def api_mark_alert_read(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    alert.is_read = True
    db.session.commit()
    return jsonify({"success": True})

@bp.route("/cattle/<int:cattle_id>/status", methods=["GET"])
@login_required
def api_cattle_status(cattle_id):
    cattle = Cattle.query.filter_by(id=cattle_id, owner_id=current_user.id).first_or_404()
    latest = HealthData.query.filter_by(cattle_id=cattle.id).order_by(HealthData.timestamp.desc()).first()
    if not latest:
        return jsonify({"status": "No Data"})
    return jsonify({
        "status": health_status_from_latest(float(latest.temp), latest.spo2, latest.motion),
        "temp": float(latest.temp),
        "heart_rate": latest.heart_rate,
        "spo2": latest.spo2,
        "motion": latest.motion
    })