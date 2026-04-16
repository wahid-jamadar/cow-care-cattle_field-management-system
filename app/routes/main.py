from flask import Blueprint, render_template
from flask_login import login_required
from app.services.simulator import dashboard_summary

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def dashboard():
    summary = dashboard_summary()
    return render_template("dashboard.html", summary=summary)