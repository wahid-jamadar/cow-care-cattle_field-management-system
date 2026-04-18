from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.health_data import HealthData
from app.models.device import Device
from app.models.alert import Alert

bp = Blueprint("hardware", __name__, url_prefix="/api/device")

@bp.route("/upload", methods=["POST"])
def upload_data():
    data = request.get_json()

    device_id = data["device_id"]
    cattle_id = data["cattle_id"]

    record = HealthData(
        cattle_id=cattle_id,
        temp=data["temp"],
        heart_rate=data["heart_rate"],
        spo2=data["spo2"],
        motion=data["motion"]
    )

    db.session.add(record)

    # Alerts
    if data["temp"] > 39.5:
        db.session.add(Alert(
            cattle_id=cattle_id,
            message="Fever Detected",
            severity="High"
        ))

    if data["spo2"] < 90:
        db.session.add(Alert(
            cattle_id=cattle_id,
            message="Low Oxygen Risk",
            severity="High"
        ))

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Data Uploaded"
    })

@bp.route("/config/<device_id>")
def get_config(device_id):
    return jsonify({
        "interval": 30,
        "server_status": "online"
    })

@bp.route("/alerts/<device_id>")
def get_alerts(device_id):
    alerts = Alert.query.order_by(Alert.id.desc()).limit(5).all()

    return jsonify([
        {
            "message": a.message,
            "severity": a.severity
        } for a in alerts
    ])