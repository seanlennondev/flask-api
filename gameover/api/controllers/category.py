from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt
)

from gameover.domain.models.category import Category
from gameover.domain.models.user import User

bp = Blueprint('Category', __name__, url_prefix='/api')

@bp.route('/categories')
def get():
    categories = Category.query.all()
    return {
        'success': True,
        'message': 'Categorias encontradas com sucesso',
        'data': [{
            'id': category.id,
            'name': category.name,
            'created_at': category.created_at
        } for category in categories]
    }, 200

@bp.route('/categories', methods=['POST'])
@jwt_required()
def create():
    identity = get_jwt_identity()    
    user = User.query.filter_by(email=identity, is_superuser=True).one_or_none()
    if not user:
        return 'Usuário náo autorizado', 401

    try:
        body = request.get_json()
        category = Category(**body)
        category.create()
        category.commit()
        return jsonify(category), 200
    except Exception as e:
        raise e
