from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import models so Alembic can detect them
    from app import models

    # Register routes
    from app.auth import auth_bp
    from app.routes import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    # REGISTER CLI COMMANDS HERE
    register_cli_commands(app)
    
    return app

def register_cli_commands(app):
    @app.cli.command("seed")
    def seed_command():
        from werkzeug.security import generate_password_hash
        from app.models import User, Customer, Bill

        db.session.add(User(
            username='admin',
            password_hash=generate_password_hash('admin123')
        ))

        c1 = Customer(name='Alice', phone='9876543210')
        c2 = Customer(name='Bob', phone='9123456780')
        db.session.add_all([c1, c2])
        db.session.commit()

        db.session.add_all([
            Bill(amount=499, month='2025-01', customer_id=c1.id),
            Bill(amount=699, month='2025-02', customer_id=c1.id),
            Bill(amount=299, month='2025-02', customer_id=c2.id),
        ])
        db.session.commit()

        print("Seed completed!")
