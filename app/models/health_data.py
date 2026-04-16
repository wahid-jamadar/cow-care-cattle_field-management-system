from datetime import datetime
from app.extensions import db

class HealthData(db.Model):
    __tablename__ = "health_data"

    id = db.Column(db.Integer, primary_key=True)
    cattle_id = db.Column(db.Integer, db.ForeignKey("cattle.id"), nullable=False)
    temp = db.Column(db.Numeric(4, 1), nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    spo2 = db.Column(db.Integer, nullable=False)
    motion = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "cattle_id": self.cattle_id,
            "temp": float(self.temp),
            "heart_rate": self.heart_rate,
            "spo2": self.spo2,
            "motion": self.motion,
            "timestamp": self.timestamp.isoformat()
        }