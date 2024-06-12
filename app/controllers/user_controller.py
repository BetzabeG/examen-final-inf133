from flask import Blueprint, request, jsonify
from app.models.user_model import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    password = data.get("password")
    
    if not name or not password:
        return jsonify({"error": "Se requiere nombre de usuario y contrasena"}), 400
    existing_user = User.find_by_name(name)
    if existing_user:
        return jsonify({"error": "El nombre de usuario ya esta en uso"}), 400
    
    new_user = User(name, password)
    new_user.save()
    return jsonify({"message": "Usuario creado exitosamente"}), 201

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data.get("name")
    password = data.get("password")
    
    user = User.find_by_name(name)
    if user and check_password_hash(user.password_hash, password):

        access_token = create_access_token(
            identity={"name": name, "roles": user.roles}
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales invalidas"}), 401