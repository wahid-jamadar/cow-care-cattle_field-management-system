from datetime import date
from app.extensions import db

class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), unique=True, nullable=False)
    device_serial = db.Column(db.String(100), nullable=False)
    cattle_id = db.Column(db.Integer, db.ForeignKey("cattle.id"), nullable=False)
    install_date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.Enum("Active", "Inactive", "Maintenance"), default="Active")

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "device_serial": self.device_serial,
            "cattle_id": self.cattle_id,
            "install_date": self.install_date.isoformat() if self.install_date else None,
            "status": self.status
        }