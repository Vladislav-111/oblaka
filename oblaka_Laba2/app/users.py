from flask import Blueprint, flash, redirect, render_template, request, flash, url_for
from app import db
from models import User, Role
from auth import check_rights

bp = Blueprint('users', __name__, url_prefix='/users')

USER_PARAMS = [
    'first_name', 'last_name', 'middle_name', 'role_id','login' 
]

def params():
    return { p: request.form.get(p) for p in USER_PARAMS }

@bp.route('/')
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)

@bp.route('/new')
def new():
    roles = Role.query.all()
    users = User.query.all()
    return render_template('users/new.html', roles=roles, users=users)

@bp.route('/create', methods=['POST'])
def create():
    user = User(**params())
    password = request.form.get('password')
    user.set_password(password)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        flash('Неверно заполнены поля.', 'danger')
        return redirect(url_for('users.new'))
    
    flash('Пользователь создан', 'success')
    return redirect(url_for('users.index'))
