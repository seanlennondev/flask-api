import os
from flask import Flask
from flask_migrate import Migrate as MIGRATE

from gameover.api.ext.jwt import configure as JWT
from gameover.api.ext.database import db, configure as DATABASE
from gameover.domain.models.user import User

def create_app():
    template_dir = os.path.abspath('gameover/api/templates')
    static_dir = os.path.abspath('gameover/api/static')
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET'] = 'SJORHEOHSIM8F8EH9284738'

    JWT(app)
    DATABASE(app)
    MIGRATE(app, db)

    @app.cli.command()
    def init():
        db.drop_all()
        db.create_all()
        user = User(
            username='sean_ono',
            name='Sean',
            surname='Lennon',
            email='sean@gmail.com',
            password='12345'
        )
        user.superuser(True)
        user.add_role('superuser_only')

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            raise e

    from gameover.api.controllers.user import bp as bp_user
    from gameover.api.controllers.category import bp as bp_category
    from gameover.api.controllers.superuser.superuser import bp as bp_superuser
    from gameover.api.controllers.doc import bp as bp_doc

    app.register_blueprint(bp_user)
    app.register_blueprint(bp_superuser)
    app.register_blueprint(bp_category)
    app.register_blueprint(bp_doc)

    if __name__ == '__main__':
        app.run()

    return app
