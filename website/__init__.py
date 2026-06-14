from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from sqlalchemy import text
import os


db = SQLAlchemy()
DB_NAME = 'database.sqlite3'


def create_database():
    db.create_all()
    print('Database Created')


def ensure_database_schema():
    with db.engine.connect() as connection:
        result = connection.execute(text('PRAGMA table_info(product);'))
        columns = [row[1] for row in result.fetchall()]
        if 'subcategory' not in columns:
            connection.execute(text('ALTER TABLE product ADD COLUMN subcategory VARCHAR(100)'))
            print('Added missing product.subcategory column.')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hbnwdvbn ajnbsjn ahe'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer, Cart, Product, Order, Wishlist

    # Serve media folder - get the media folder path relative to the project root
    media_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')
    
    @app.route('/media/<path:filename>')
    def serve_media(filename):
        return send_from_directory(media_path, filename)
    
    # Add Jinja filter to convert media paths
    @app.template_filter('media_url')
    def media_url_filter(path):
        if not path:
            return 'https://via.placeholder.com/200x200?text=No+Image'
        # Normalize path - handle various input formats
        path = str(path).strip()
        
        # Remove ./ prefix if present
        if path.startswith('./'):
            path = path[2:]
        
        # Remove leading slashes
        path = path.lstrip('/')
        
        # Ensure path starts with /media/
        if not path.startswith('media/'):
            # If it doesn't start with media/, assume it's missing
            if not path.startswith('/media/'):
                path = f'media/{path}'
        
        # Convert to /media/ format
        path = '/' + path if not path.startswith('/') else path
        
        return path

    app.register_blueprint(views, url_prefix='/') # localhost:5000/about-us
    app.register_blueprint(auth, url_prefix='/') # localhost:5000/auth/change-password
    app.register_blueprint(admin, url_prefix='/')

    with app.app_context():
        create_database()
        ensure_database_schema()

    return app