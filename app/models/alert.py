from datetime import datetime
from app.extensions import db

class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    cattle_id = db.Column(db.Integer, db.ForeignKey("cattle.id"), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=True)
    message = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.Enum("Low", "Medium", "High"), default="Medium")
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "cattle_id": self.cattle_id,
            "device_id": self.device_id,
            "message": self.message,
            "severity": self.severity,
            "is_read": self.is_read,
            "timestamp": self.timestamp.isoformat()
        }