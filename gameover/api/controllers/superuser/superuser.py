from flask import Blueprint, jsonify, request
from gameover.api.ext.jwt import (
    superuser_required,
    admin_required
)

from gameover.domain.models.user import User

bp = Blueprint('SuperUser', __name__, url_prefix='/api')

@bp.route('/users/restrict', methods=['POST'])
@superuser_required()
def create_superuser():
    try:
        inputs = request.get_json()
        user = create_user(inputs)
        return {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
            'password': user._password,
            'is_superuser': user.__is_superuser,
            'role': user.role,
            'is_active': user.is_active
        }, 200
    except Exception as e:
        raise e

def create_user(inputs):
    user = User(**inputs)
    user.add_superuser()
    user.add_role('superuser_only')
    user.insert()
    user.commit()
    return user

@bp.route('/users/admin', methods=['POST'])
@superuser_required()
def create_admin():
    try:
        (username, name, surname, email, password) = (
            request.json.get('username', None),
            request.json.get('name', None),
            request.json.get('surname', None),
            request.json.get('email', None),
            request.json.get('password', None)
        )
        if not username:
            return jsonify(msg='O campo nome de usuário é obrigatório'), 422
        elif not name:
            return jsonify(msg='O campo nome é obrigatório'), 422
        elif not surname:
            return jsonify(msg='O campo sobrenome é obrigatório'), 422
        elif not email:
            return jsonify(msg='O campo e-mail é obrigatório'), 422
        elif not password:
            return jsonify(msg='O campo senha é obrigatório'), 422
        
        user = User(username, name, surname, email, password)
        user.add_role('admin_only')
        user.insert()
        user.commit()
        return jsonify(
            success=True,
            msg='Admin registrado com sucesso',
            data=user.jsonify(),
            errors=[]
        ), 200
    except Exception as e:
        raise e

@bp.route('/users/admin/<int:id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
@superuser_required()
def delete_admin(id):
    try:
        errors = []
        user = User.query.filter_by(id=id).one_or_none()
        if not user:
            return jsonify(msg='Admin não encontrado'), 404

        if request.method == 'PUT':
            (name, surname) = (
                request.json.get('name', None),
                request.json.get('surname', None)
            )
            if not name:
                return jsonify(msg='O campo nome é obrigatório'), 422
            if not surname:
                return jsonify(msg='O campo sobrenome é obrigatório'), 422
            
            user.update(name, surname)
            user.commit()
            return jsonify(msg='Admin alterado com sucesso'), 200

        if request.method == 'PATCH':
            (current_password, new_password) = (
                request.json.get('current_password', None),
                request.json.get('new_password', None)
            )
            if not current_password:
                # errors.append('O campo senha atual é obrigatório')
                return jsonify(msg='O campo senha atual é obrigatório'), 422

            elif not new_password:
                return jsonify(msg='O campo nova senha é obrigatório'), 422

            elif not user.check_password(current_password):
                return jsonify(msg='Senha atual inválida'), 422

            user.change_password(new_password)
            user.commit()
            return jsonify(
                success=True,
                msg='Senha alterada com sucesso',
                data=user.jsonify(),
                errors=[]
            ), 200

        if request.method == 'DELETE':
            user.delete()
            user.commit()
            return jsonify(
                success=True,
                msg='Admin excluído com sucesso',
                data=None,
                errors=errors
            ), 200

        if request.method == 'GET':
            return jsonify(
                success=True,
                msg='Admin encontrado com sucesso',
                data=user.jsonify(),
                errors=errors
            ), 200
    except Exception as e:
        raise e
