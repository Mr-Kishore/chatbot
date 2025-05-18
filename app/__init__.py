from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize routes (you can add more if needed)
    from app.routes import auth, employee, admin
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(employee.employee_bp)
    app.register_blueprint(admin.admin_bp)

    return app
