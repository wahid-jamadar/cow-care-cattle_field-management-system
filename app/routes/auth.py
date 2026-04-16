from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, bcrypt
from app.models.user import User

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            if request.is_json:
                return jsonify({"success": False, "message": "Invalid email or password"}), 401
            flash("Invalid email or password", "danger")
            return render_template("login.html")

        login_user(user)

        if request.is_json:
            return jsonify({"success": True, "user": user.to_dict()})

        return redirect(url_for("main.dashboard"))

    return render_template("login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        role = data.get("role", "Farmer")

        if User.query.filter_by(email=email).first():
            msg = "Email already exists"
            if request.is_json:
                return jsonify({"success": False, "message": msg}), 400
            flash(msg, "danger")
            return render_template("register.html")

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(name=name, email=email, password=hashed, role=role)
        db.session.add(user)
        db.session.commit()

        if request.is_json:
            return jsonify({"success": True, "message": "Registered successfully"})

        flash("Registered successfully. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("auth.login"))