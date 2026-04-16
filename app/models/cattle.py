from datetime import datetime
from app.extensions import db

class Cattle(db.Model):
    __tablename__ = "cattle"

    id = db.Column(db.Integer, primary_key=True)
    cattle_tag = db.Column(db.String(50), unique=True, nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Numeric(10, 2), nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    devices = db.relationship("Device", backref="cattle", lazy=True, cascade="all, delete-orphan")
    health_data = db.relationship("HealthData", backref="cattle", lazy=True, cascade="all, delete-orphan")
    alerts = db.relationship("Alert", backref="cattle", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "cattle_tag": self.cattle_tag,
            "breed": self.breed,
            "age": self.age,
            "weight": float(self.weight),
            "photo": self.photo,
            "owner_id": self.owner_id
        }