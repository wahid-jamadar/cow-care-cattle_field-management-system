import random
from datetime import datetime
from app.extensions import db
from app.models.cattle import Cattle
from app.models.device import Device
from app.models.health_data import HealthData
from app.models.alert import Alert
from .alerts import get_alert_from_sample

def generate_sample():
    temp = round(random.uniform(37.0, 41.0), 1)
    heart_rate = random.randint(60, 120)
    spo2 = random.randint(85, 100)
    motion = random.choices(["High", "Normal", "Low"], weights=[2, 6, 2])[0]
    return temp, heart_rate, spo2, motion

def simulate_for_all_cattle():
    created = []

    cattle_list = Cattle.query.all()
    for cattle in cattle_list:
        temp, heart_rate, spo2, motion = generate_sample()

        record = HealthData(
            cattle_id=cattle.id,
            temp=temp,
            heart_rate=heart_rate,
            spo2=spo2,
            motion=motion
        )
        db.session.add(record)
        db.session.flush()

        device = Device.query.filter_by(cattle_id=cattle.id).first()
        for message, severity in get_alert_from_sample(temp, spo2, motion):
            alert = Alert(
                cattle_id=cattle.id,
                device_id=device.id if device else None,
                message=message,
                severity=severity
            )
            db.session.add(alert)

        created.append({
            "cattle_id": cattle.id,
            "temp": temp,
            "heart_rate": heart_rate,
            "spo2": spo2,
            "motion": motion
        })

    db.session.commit()
    return created

def health_status_from_latest(temp, spo2, motion):
    if temp > 39.5 or spo2 < 90 or motion == "Low":
        return "At Risk"
    return "Healthy"

def dashboard_summary():
    total_cattle = Cattle.query.count()
    attached_devices = Device.query.filter_by(status="Active").count()
    latest_records = (
        db.session.query(HealthData)
        .order_by(HealthData.timestamp.desc())
        .limit(50)
        .all()
    )

    latest_per_cattle = {}
    for r in latest_records:
        if r.cattle_id not in latest_per_cattle:
            latest_per_cattle[r.cattle_id] = r

    healthy = 0
    at_risk = 0
    for cattle_id, r in latest_per_cattle.items():
        if health_status_from_latest(float(r.temp), r.spo2, r.motion) == "Healthy":
            healthy += 1
        else:
            at_risk += 1

    alerts_count = Alert.query.count()

    trend = (
        HealthData.query
        .order_by(HealthData.timestamp.desc())
        .limit(15)
        .all()
    )[::-1]

    alerts_list = Alert.query.order_by(Alert.timestamp.desc()).limit(10).all()

    return {
        "total_cattle": total_cattle,
        "attached_devices": attached_devices,
        "healthy": healthy,
        "alerts": alerts_count,
        "at_risk": at_risk,
        "last_sync": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "trend": [
            {
                "label": r.timestamp.strftime("%H:%M:%S"),
                "temp": float(r.temp)
            } for r in trend
        ],
        "alerts_list": [a.to_dict() for a in alerts_list]
    }