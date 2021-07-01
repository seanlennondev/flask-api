from datetime import timedelta
from functools import wraps
from flask import jsonify

from flask_jwt_extended import (
    JWTManager,
    verify_jwt_in_request,
    get_jwt,
)

from gameover.domain.models.user import User

jwt = JWTManager()

def configure(app):
    jwt.init_app(app)

    app.config['JWT_SECRET_KEY'] = 'JWJDHDOSHIIF747174BDIVQI@|Ü'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    user = User.query.filter_by(email=identity).one_or_none()
    if not user:
        raise Exception('Unauthorize')
    return user

def user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['is_superuser'] or claims['role'] == 'user_only':
                return fn(*args, **kwargs)
            else:
                return jsonify(
                    msg='Restricted for user'
                ), 403
        return decorator
    return wrapper

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['is_superuser'] or claims['role'] == 'admin_only':
                return fn(*args, **kwargs)
            else:
                return jsonify(
                    msg='Restricted for administrator'
                ), 403
        return decorator
    return wrapper

def journalist_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['is_superuser'] or claims['role'] == 'journalist_only':
                return fn(*args, **kwargs)
            else:
                return jsonify(
                    msg='Restricted for journalist'
                ), 403
        return decorator
    return wrapper

def superuser_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['is_superuser']:
                return fn(*args, **kwargs)
            else:
                return jsonify(
                    msg='Restricted for superuser'
                ), 403
        return decorator
    return wrapper
