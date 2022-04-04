from flask import Flask, redirect, jsonify
import os
from flask_jwt_extended import JWTManager

from src.database import db, Bookmark
from src.auth import auth
from src.bookmarks import bookmarks
from src.constants.https_status_codes import *

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        )

    else:
        app.config.from_mapping(test_config)
    
    
    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.get('/<short_url>')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first()
        if bookmark:
            bookmark.visits += 1
            db.session.commit()
            return redirect(bookmark.url)
        else:
            return jsonify({"message": "URL not found"}), HTTP_404_NOT_FOUND

    
    """handling error in applications"""
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_400(error):
        return jsonify({"message": "URL 404 not found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(error):
        return jsonify({"message": "Internal server error"}), HTTP_500_INTERNAL_SERVER_ERROR
    
    return app




