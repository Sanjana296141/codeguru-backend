from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db, bcrypt, jwt, migrate
from config import Config
from routes.upload import upload_bp
from routes.review import review_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp
from routes.export import export_bp
from routes.ai import ai_bp
from routes.documentation import documentation_bp
import os

def create_app():

    app = Flask(__name__)
    
    app.config.from_object(Config)
    os.makedirs(
    Config.UPLOAD_FOLDER,
    exist_ok=True
   )

    os.makedirs(
    Config.REPORT_FOLDER,
    exist_ok=True
   )

    CORS(app)

    db.init_app(app)

    bcrypt.init_app(app)

    jwt.init_app(app)

    migrate.init_app(app, db)

    from models.user import User
    from models.project import Project
    from models.review import Review
    from models.finding import ReviewFinding
    

    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(
    documentation_bp
)
    return app


app = create_app()

if __name__ == "__main__":

    app.run(debug=True)