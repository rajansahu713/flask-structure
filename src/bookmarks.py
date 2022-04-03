import re
from flask import Blueprint, request, jsonify
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.constants.https_status_codes import *
from src.database import Bookmark, db

bookmarks = Blueprint('bookmarks', __name__, url_prefix='/api/v1/bookmarks')

@bookmarks.route('/', methods=['POST', 'GET'])
@jwt_required()
def handle_bookmarks():

    current_user = get_jwt_identity()

    if request.method == 'POST':
        print(request.json)
        body = request.json.get('body',"")
        url = request.json.get('url',"")

        if not validators.url(url):
            return jsonify({"message": "URL is not valid"}), HTTP_400_BAD_REQUEST
        
        if Bookmark.query.filter_by(url=url).first() is not None:
            return jsonify({"message": "URL is already in use"}), HTTP_409_CONFLICT 

        bookmark = Bookmark(body=body, url=url, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify(
            {'id':bookmark.id,
            "url":bookmark.url,
            "short_url":bookmark.short_url,
            "visits":bookmark.visits,
            "body":bookmark.body,
            "created_at":bookmark.created_at,
            "updated_at":bookmark.updated_at,
            }
        ),HTTP_201_CREATED

        

    if request.method == 'GET':

        """paginations"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        bookmarks = Bookmark.query.filter_by(user_id = current_user).paginate(page=page, per_page=per_page)

        data =[]
        for bookmark in bookmarks.items:
            data.append(
                {
                    "id":bookmark.id,
                    "url":bookmark.url,
                    "short_url":bookmark.short_url,
                    "visits":bookmark.visits,
                    "body":bookmark.body,
                    "created_at":bookmark.created_at,
                    "updated_at":bookmark.updated_at,
                }
            )
        meta ={
            "page":bookmarks.page,
            "pages":bookmarks.pages,
            "total_page":bookmarks.total,
            "prev_page":bookmarks.prev_num,
            "next_page":bookmarks.next_num,
            "has_next":bookmarks.has_next,
            "has_prev":bookmarks.has_prev,
            
        }
        return jsonify({"data":data, "meta":meta}),HTTP_200_OK
    

@bookmarks.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=id, user_id=current_user).first()
    if not bookmark:
        return jsonify({"message": "Bookmark not found"}), HTTP_404_NOT_FOUND

    return jsonify(    
        {
            "id":bookmark.id,
            "url":bookmark.url,
            "short_url":bookmark.short_url,
            "visits":bookmark.visits,
            "body":bookmark.body,
            "created_at":bookmark.created_at,
            "updated_at":bookmark.updated_at,
                }
    ),HTTP_200_OK


@bookmarks.delete('/<int:id>')
@jwt_required()
def update_bookmark(id):
    current_id = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=id, user_id=current_id).first()

    if not bookmark:
        return jsonify({"message": "Bookmark not found"}), HTTP_404_NOT_FOUND
    
    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({"message": "Bookmark deleted"}), HTTP_200_OK


@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@jwt_required()
def editbookmark(id):
    current_id = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(id=id, user_id=current_id).first()
    if not bookmark:
        return jsonify({"message": "Bookmark not found"}), HTTP_404_NOT_FOUND
    
    body = request.json.get('body',"")
    url = request.json.get('url',"")

    if not validators.url(url):
        return jsonify({"message": "URL is not valid"}), HTTP_400_BAD_REQUEST

    if len(body) > 0:
        bookmark.body = body
    if len(url) > 0:
        bookmark.url = url
    db.session.commit()

    
    return jsonify(    
        {
            "id":bookmark.id,
            "url":bookmark.url,
            "short_url":bookmark.short_url,
            "visits":bookmark.visits,
            "body":bookmark.body,
            "created_at":bookmark.created_at,
            "updated_at":bookmark.updated_at,
                }
    ),HTTP_200_OK


    

    