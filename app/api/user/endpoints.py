from service.db.models import User, Student, Teacher
from flask import request, jsonify, Blueprint
from api.user.schemas import LoginUser, LoginUserSchema,  RegisterUserSchema, RegisterUser, SearchUser, SearchUserSchema, AddRelationUserSchema, AddRelationUser 
from marshmallow import ValidationError
from flask_login import login_user, current_user, login_required, logout_user
from wsgi import db
from sqlalchemy import and_
from api.common import teacher_required, student_required
from sqlalchemy.exc import IntegrityError
from flasgger import swag_from
from api.common import validate_id
from json import load
from dataclasses import asdict


bp_log_reg = Blueprint('login_logout_registration', __name__)

@bp_log_reg.post("/login")
@swag_from('doc/login.yaml')
def post_user_login():
    if current_user.is_authenticated:
       return jsonify({"message": "AlreadyLoggedIn"}), 403
    try:
        
        data = request.get_json()
        user_login_schema = LoginUserSchema()
        user_data: LoginUser = user_login_schema.load(data)

    except ValidationError as err:
        return jsonify({"message": "Validation Error", "errors": err.messages}), 400
    
    user = db.session.query(User).filter(and_(Teacher.email == user_data.email, Teacher.password == user_data.password)).first()
    if not user:
        return jsonify({"message": "UserNotFound"}), 404

    login_user(user)

    return  jsonify({"id":user.id, "type": user.type}), 200
    

@bp_log_reg.post("/register")
@swag_from('doc/register.yaml')
def post_user_register():
    if current_user.is_authenticated:
       return jsonify({"message": "AlreadyLoggedIn"}), 403
    try:
        data = request.get_json()
        user_register_schema = RegisterUserSchema()
        user_data: RegisterUser = user_register_schema.load(data)
    except ValidationError as err:
        return jsonify({"message": "Validation Error", "errors": err.messages}), 400
    try:
        user = None
        if user_data.type == "student":
            user = Student(**asdict(user_data))
        else:
            user = Teacher(**asdict(user_data))

        db.session.add(user)
        db.session.commit()

    except IntegrityError as err:
        db.session.rollback()
        return jsonify({"message": "Integrity Error"}), 400
    
    return jsonify(), 200


@bp_log_reg.post("/logout")
@login_required
@swag_from('doc/logout.yaml')
def logout():
    logout_user()
    return jsonify(), 200


bp_user = Blueprint("user_actions", __name__)


@bp_user.get('/user')
@login_required
@swag_from('doc/get_teachers_or_students.yaml')
def get_teachers_or_students():
    users = []
    if current_user.type == "teacher":
        teacher = db.session.query(Teacher).filter(Teacher.id==current_user.id).first()
        if teacher:
            users = [{"id": student.id, "username": student.username} for student in teacher.students]
    else:
        student = db.session.query(Student).filter(Student.id==current_user.id).first()
        if student:
            users = [{"id": teacher.id, "username": teacher.username} for teacher in student.teachers]    

    return jsonify({"users": users}), 200


@bp_user.get('/user/<uuid:user_id>')
@login_required
@swag_from('doc/get_about.yaml')
def get_about(user_id):
    if user_id == current_user.id:
        user = current_user
    else:
        user = db.session.query(User).filter(User.id == user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404
  
    return jsonify(
        {
          "username": user.username,
          "email": user.email,
          "first_name": user.first_name,
          "last_name": user.last_name,
          "birthdate": user.birthdate
        }
    ), 200


@bp_user.get('/user/search')
@login_required
@teacher_required
@swag_from('doc/search_by_username.yaml')
def search_by_username():
    try:
        data = request.args
        search_schema = SearchUserSchema()
        search_data = search_schema.load(data)
    except ValidationError as err:
        jsonify({"message": err.messages}), 403
    
    student = db.session.query(Student).filter(Student.username == search_data.username).first()
    
    return jsonify({"id": student.id} if student else {}), 200


@bp_user.post('/user/relationship')
@login_required
@teacher_required
@swag_from('doc/add_relation.yaml')
def add_relation():
    try:
        
        data = request.get_json()
        add_relation_schema = AddRelationUserSchema()
        add_relation_data = add_relation_schema.load(data)
        
    except ValidationError as err:
        return jsonify({"ValidationError": err.messages}), 403
    
    student = db.session.query(Student).filter(Student.username == add_relation_data.username).first()

    if not student:
        return jsonify({"message": "UserNotFound"}), 404
    
    current_user.students.add(student)
    db.session.commit()

    return jsonify(), 200
    


    



    


    

    
        
        
    
    


    

            

    
    

    
    
    
    

    



