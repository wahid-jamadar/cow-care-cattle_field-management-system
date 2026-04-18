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

@bp.route('/iot/send-data', methods=['POST'])
def receive_iot_data():
    """
    Receive real-time IoT sensor data from ESP32 / NodeMCU devices
    POST JSON:
    {
        "device_id": "ESP32_001",
        "temperature": 38.5,
        "heart_rate": 82,
        "spo2": 97,
        "motion_x": 0.15,
        "motion_y": 0.07,
        "motion_z": 0.96,
        "battery": 88
    }
    """

    try:
        data = request.get_json(force=True)

        # Validate required fields
        required_fields = [
            "device_id",
            "temperature",
            "heart_rate",
            "spo2",
            "motion_x",
            "motion_y",
            "motion_z"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "message": f"Missing field: {field}"
                }), 400

        # Read values
        device_id = str(data["device_id"]).strip()

        temperature = float(data["temperature"])
        heart_rate = int(data["heart_rate"])
        spo2 = int(data["spo2"])

        motion_x = float(data["motion_x"])
        motion_y = float(data["motion_y"])
        motion_z = float(data["motion_z"])

        battery = int(data.get("battery", 100))

        # Find device
        device = Device.query.filter_by(device_id=device_id).first()

        if not device:
            return jsonify({
                "success": False,
                "message": "Device not registered"
            }), 404

        # Motion Logic
        total_motion = abs(motion_x) + abs(motion_y) + abs(motion_z)

        if total_motion < 0.40:
            motion_status = "Low"
        elif total_motion < 1.20:
            motion_status = "Normal"
        else:
            motion_status = "High"

        # Save health data
        health = HealthData(
            cattle_id=device.cattle_id,
            temp=temperature,
            heart_rate=heart_rate,
            spo2=spo2,
            motion=motion_status,
            motion_x=motion_x,
            motion_y=motion_y,
            motion_z=motion_z,
            timestamp=datetime.utcnow()
        )

        db.session.add(health)

        # Update device heartbeat
        device.last_seen = datetime.utcnow()
        device.status = "Active"

        # Generate alerts
        alerts_created = []

        if temperature > 39.5:
            alert = Alert(
                cattle_id=device.cattle_id,
                device_id=device.id,
                message=f"High Temperature ({temperature}°C)",
                severity="High"
            )
            db.session.add(alert)
            alerts_created.append("Fever")

        if spo2 < 90:
            alert = Alert(
                cattle_id=device.cattle_id,
                device_id=device.id,
                message=f"Low SpO₂ ({spo2}%)",
                severity="High"
            )
            db.session.add(alert)
            alerts_created.append("Low Oxygen")

        if motion_status == "Low":
            alert = Alert(
                cattle_id=device.cattle_id,
                device_id=device.id,
                message="Low Movement Detected",
                severity="Medium"
            )
            db.session.add(alert)
            alerts_created.append("Low Movement")

        # Commit DB
        db.session.commit()

        # Response
        return jsonify({
            "success": True,
            "message": "IoT data received successfully",
            "device_id": device_id,
            "cattle_id": device.cattle_id,
            "motion_status": motion_status,
            "alerts": alerts_created,
            "timestamp": datetime.utcnow().isoformat()
        }), 200

    except ValueError:
        return jsonify({
            "success": False,
            "message": "Invalid numeric data"
        }), 400

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500