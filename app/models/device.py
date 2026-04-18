from datetime import date
from app.extensions import db

class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)

    device_id = db.Column(db.String(100), unique=True)
    device_name = db.Column(db.String(100))
    device_details = db.Column(db.String(255))
    device_serial = db.Column(db.String(100))

    cattle_id = db.Column(db.Integer, db.ForeignKey("cattle.id"))
    install_date = db.Column(db.Date)
    status = db.Column(db.String(30), default="Active")