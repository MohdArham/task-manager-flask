from flask import Flask
from config import Config
from extensions import db, migrate, jwt
import models
from auth import bp as auth_bp
from routes import bp as tasks_bp
from flasgger import Swagger

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    template = {
        "swagger": "2.0",
        "info": {
            "title": "Task Manager API",
            "description": "Flask-based Task Manager with JWT authentication",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Bearer scheme. Copy from /login: 'Bearer {access_token}'"
            }
        },
        "security": [
            {"Bearer": []}
        ]
    }

    swagger = Swagger(app, template=template)

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    @app.route('/')
    def index():
        return 'Task Manager API. Visit /apidocs for Swagger UI.'
    return app

if __name__ == '__main__':
    app = create_app()
    print("=========================Flask Task Manager API Started=============================")
    app.run(debug=True,port=5000)
