from functools import wraps
from flask import redirect, url_for, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from app import app,db
from app.models import User

@app.route('/')
def role_required(role):
    def decorator (f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                return jsonify({"error": "Access denied"}), 403
            return f(*args, **kwargs)

        return decorated_function
    return decorator
@app.route('/signup', methods = ['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already in use"}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already in use"}), 409
    role = data.get('role', 'user')
    if role == 'admin' and data.get('admin_key') != "my_secretkey":
        return jsonify({"error":"Invalid admin key"}), 403

    user = User(username=data['username'], email=data.get('email', f"{data['username']}@test.com"),role=data.get('role', 'user'))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"User created successfully"}), 201

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({"message":"User logged in"}), 200
    return jsonify({"error": "Invalid credentials"})

@app.route('/user/dashboard')
@role_required('user')
def user_dashboard():
    return f"Welcome User {current_user.username}"

@app.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    return f" Welcome Admin {current_user.username}"