from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.device import Device
from app.models.health_data import HealthData
from app.models.alert import Alert

bp = Blueprint("iot", __name__, url_prefix="/api/iot")

@bp.route("/send-data", methods=["POST"])
def send_data():

    data = request.get_json()

    device_id = data.get("device_id")
    temp = data.get("temperature")
    hr = data.get("heart_rate")
    spo2 = data.get("spo2")
    mx = data.get("motion_x")
    my = data.get("motion_y")
    mz = data.get("motion_z")

    device = Device.query.filter_by(device_id=device_id).first()

    if not device:
        return jsonify({"error": "Device not found"}), 404

    motion_status = "Normal"

    if abs(mx) < 0.05 and abs(my) < 0.05:
        motion_status = "Low"

    health = HealthData(
        cattle_id=device.cattle_id,
        temp=temp,
        heart_rate=hr,
        spo2=spo2,
        motion=motion_status
    )

    db.session.add(health)

    # Alerts
    if temp > 39.5:
        alert = Alert(
            cattle_id=device.cattle_id,
            device_id=device.id,
            message="Fever Detected",
            severity="High"
        )
        db.session.add(alert)

    if spo2 < 90:
        alert = Alert(
            cattle_id=device.cattle_id,
            device_id=device.id,
            message="Low Oxygen Level",
            severity="High"
        )
        db.session.add(alert)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Data Stored"
    })