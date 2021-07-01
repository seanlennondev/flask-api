from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    current_user
)

from gameover.api.ext.jwt import (
    admin_required,
    superuser_required,
    user_required
)

from gameover.domain.models.user import User

bp = Blueprint('User', __name__, url_prefix='/api')

@bp.route('/users/auth', methods=['POST'])
def autheticate():
    try:
        (email, password) = (
            request.json.get('email'),
            request.json.get('password')
        )
        if not email or not password:
            return 'Os campos são obrigatórios', 422

        user = User.query.filter_by(email=email).one_or_none()
        if not user or not user.check_password(current_password=password):
            return 'E-mail ou senha inválidos', 422

        token = user.generate_access_token()
        return {
            'access_token': token
        }, 200
    except Exception as e:
        raise e

@bp.route('/users', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        users = User.query.all()
        return {
            'data': [{
                'id': user.id,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
                'role': user.role,
                'password': user.password,
                'is_superuser': user.is_superuser,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            } for user in users]
        }, 200

    if request.method == 'POST':
        body = request.get_json()
        if not body:
            return 'Os campos são obrigatórios', 422

        user = User(**body)
        user.add_role('user_only')
        user.insert()
        user.commit()
        return 'Usuário registrado com sucesso', 200

@bp.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get(id):
    try:
        user = User.query.get(id)
        if request.method == 'GET':
            return {
                'data': {
                    'name': user.name
                }
            }
        if request.method == 'PUT':
            body = request.get_json()
            user.update(**body)
            user.commit()
            return {
                'id': user.id,
                'name': user.name,
                'surname': user.surname
            }, 200

        if request.method == 'DELETE':
            user.delete()
            user.commit()
            return 'Usuário deletado com sucesso', 200
    except Exception as e:
        raise e

@bp.route('/users/<int:id>/change-password', methods=['PATCH'])
def change_password(id):
    try:
        user = User.query.get(id)
        (current_password, new_password) = (
            request.json.get('current_password', None),
            request.json.get('new_password', None),
        )
        if not user.check_password(current_password):
            return 'Falha ao alterar senha', 422

        user.change_password(new_password)
        user.commit()
        return 'Senha alterada com sucesso', 200
    except Exception as e:
        raise e
