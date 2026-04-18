import os
from flask import Flask
from .config import Config
from .extensions import db, login_manager, bcrypt
from .routes.hardware import bp as hardware_bp
from .routes.iot import bp as iot_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .routes.auth import bp as auth_bp
    from .routes.main import bp as main_bp
    from .routes.cattle import bp as cattle_bp
    from .routes.devices import bp as devices_bp
    from .routes.reports import bp as reports_bp
    from .routes.pages import bp as pages_bp
    from .routes.api import bp as api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(cattle_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(hardware_bp)
    app.register_blueprint(iot_bp)

    from .models.user import User
    from .models.cattle import Cattle
    from .models.device import Device
    from .models.health_data import HealthData
    from .models.alert import Alert

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app