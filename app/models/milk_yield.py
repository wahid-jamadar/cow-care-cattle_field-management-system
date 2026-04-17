from app.extensions import db
from datetime import datetime

class MilkYield(db.Model):
    __tablename__ = "milk_yield"

    id = db.Column(db.Integer, primary_key=True)
    cattle_id = db.Column(db.Integer, db.ForeignKey("cattle.id"), nullable=False)
    yield_liters = db.Column(db.Numeric(5,2), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cattle = db.relationship("Cattle", backref="milk_records")

    def to_dict(self):
        return {
            "id": self.id,
            "cattle_id": self.cattle_id,
            "yield_liters": float(self.yield_liters),
            "record_date": self.record_date.strftime("%Y-%m-%d"),
            "notes": self.notes
        }