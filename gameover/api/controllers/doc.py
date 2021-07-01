from flask import Blueprint, render_template, redirect, request

from gameover.domain.models.user import User

bp = Blueprint('Doc', __name__)

@bp.route('/')
def index():
    user = User.query.get(1)
    return render_template('index.html', title='Doc', msg='My Doc Page', user=user)

@bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        user = User.query.get(1)
        return render_template('login.html', title='Login', user=user)
    if request.method == 'POST':
        inputs = request.get_form()
        print(inputs)
        return redirect('/')
        
