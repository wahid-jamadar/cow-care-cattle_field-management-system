from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models.health_data import HealthData
from app.models.cattle import Cattle
from app.services.report_service import build_csv_response, build_pdf_response

bp = Blueprint("reports", __name__)

@bp.route("/reports")
@login_required
def reports_page():
    cattle = Cattle.query.filter_by(owner_id=current_user.id).all()
    labels = [c.cattle_tag for c in cattle]
    values = []
    for c in cattle:
        latest = HealthData.query.filter_by(cattle_id=c.id).order_by(HealthData.timestamp.desc()).first()
        values.append(float(latest.temp) if latest else 0)

    return render_template("reports.html", labels=labels, values=values)

@bp.route("/reports/export/<fmt>")
@login_required
def export_report(fmt):
    if fmt == "csv":
        return build_csv_response()
    if fmt == "pdf":
        return build_pdf_response()
    return {"error": "Invalid format"}, 400