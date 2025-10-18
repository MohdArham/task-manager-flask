from flask import Blueprint, request, jsonify
from extensions import db
import models
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """
        Register a new user
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
        responses:
          201:
            description: User created successfully
          400:
            description: Bad request or user already exists
        """
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'username and password required'}), 400
    if models.User.query.filter_by(username=username).first():
        return jsonify({'msg': 'username already exists'}), 400
    user = models.User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 201

@bp.route('/login', methods=['POST'])
def login():
    """
        User login
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: Returns JWT token
          401:
            description: Invalid credentials
    """
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'username and password required'}), 400

    user = models.User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'bad credentials'}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"username": user.username, "role": user.role}
    )
    return jsonify({'access_token': token}), 200
