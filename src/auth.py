from flask import Blueprint, request, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from src.constants.https_status_codes import *
from src.database import User,db

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.post('/register')
def register():

    """
    Register a new user
    response from font-end:
    {
    "username":"admin123",
    "email":"admin123@gmail.com",
    "password":"123456789"
    }
    """

    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters long"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error':'Username must be at least 3 characters long'}),HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error':'Username must contain at least one special character'}),HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error':'Email is not valid'}),HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error':'Email is already in use'}),HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error':'Username is already in use'}),HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)
    user = User(username=username, email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {'message':'User created successfully',
        'user':{
            'username':username,
            'email':email,
        }
    }
    ),HTTP_201_CREATED


@auth.post('/login')
def login():
    """
    Login a user
    response from font-end:
    {
    "email":"admin123@gmail.com",
    "password":"123456789"
    }
    """
    email = request.json.get('email','')
    password = request.json.get('password',"")

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)
        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)
            return jsonify(
                {'message':'Login successful',
                'user':{
                    "username":user.username,
                    'email':user.email,

                    'refresh':refresh,
                    'access':access,
                }
            }
            ),HTTP_200_OK

        else:
            return jsonify(
                {'error':'Invalid password'}
            ),HTTP_401_UNAUTHORIZED

    else:
        return jsonify(
            {'error':'User does not exist'}
        ),HTTP_404_NOT_FOUND



@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    print(user_id)
    user = User.query.filter_by(id=user_id).first()
    return jsonify(
        {'message':'User found',
        
        'user':{"username":user.username,
                'email':user.email,        
                }
        }
    ), HTTP_200_OK

@auth.post('token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    return jsonify(
        {'access_token':access_token}
    ), HTTP_200_OK



