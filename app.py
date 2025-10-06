from flask import Flask
from extensions import db


def create_app():
    app = Flask(__name__)
    
    # Configure SQLAlchemy
    # Use absolute path to ensure consistency with Alembic
    import os
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Import models to ensure they're registered with SQLAlchemy
    with app.app_context():
        import models
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
