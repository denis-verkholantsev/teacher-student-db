from service.db.models import FileStorage, Homework, Exercise, Student
from flask import request, jsonify, session, Blueprint
from api.homework.schemas import PostHomeworkSchema, PostHomework
from marshmallow import ValidationError
from flask_login import login_user, current_user, login_required, logout_user
from wsgi import db
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from api.common import teacher_required
from datetime import datetime
from flasgger import swag_from
from dataclasses import asdict
from api.common import validate_id
from uuid import UUID

bp_homework = Blueprint('homework', __name__, url_prefix="/user")

@bp_homework.post("/homework")
@login_required
@teacher_required
@swag_from('doc/post.yaml')
def post_homework():
    try:
        data = request.get_json()
        homework_schema = PostHomeworkSchema()
        homework_data: PostHomework = homework_schema.load(data)

    except ValidationError as err:
        return jsonify({"message": "Validation Error", "errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"message": "Value Error", "errors": str(err)}), 400

    files = exercises = students = None
    if homework_data.files:
        files = db.session.query(FileStorage).filter(FileStorage.user_id == current_user.id).filter(FileStorage.id.in_(homework_data.files)).all()
    if homework_data.exercises:
        exercises = db.session.query(Exercise).filter(Exercise.teacher_id == current_user.id).filter(Exercise.id.in_(homework_data.exercises)).all()
    if homework_data.students:
        students = db.session.query(Student).filter(Student.id == current_user.id).filter(Student.id.in_(homework_data.students)).all()

    homework = Homework(title=homework_data.title, 
                        description=homework_data.description,
                        deadline=datetime.strptime(homework_data.deadline, '%Y-%m-%dT%H:%M:%S')
                        )
    
    if files:
        homework.files.update(files)

    if exercises:
        homework.exercises.update(exercises)

    if students:
        homework.students.update(students)
    
    homework.teacher_id = current_user.id

    db.session.add(homework)
    try:
        db.session.commit()
    except IntegrityError as err:
        err_message = str(err.orig) if err.orig else str(err.args[0]) if err.args else "Unknown error"
        return jsonify({"message": err_message}), 403

    return jsonify({"id": homework.id}), 200
    


@bp_homework.get("/homeworks/<uuid:homework_id>")
@login_required
@swag_from('doc/get_about.yaml')
def get_about(homework_id):
    if not validate_id(homework_id):
        return jsonify({"meassage": "No instances of UUID"}), 403
    
    homework = db.session.query(Homework).filter(Homework.id == homework_id).first()

    if current_user.type == "teacher":
        if homework.teacher_id != current_user:
            return jsonify({"message": "homework not found"}), 404
    else:
        if homework not in current_user.homeworks:
            return jsonify({"message": "homework not found"}), 404

    if not homework:
        return jsonify({"message": "homework not found"}), 404
    
    formated_created = formated_updated = None
    if homework.created:
        formated_created = homework.created.strftime("%Y-%m-%dT%H:%M:%S")
    if homework.updated:
        formated_updated = homework.updated.strftime("%Y-%m-%dT%H:%M:%S")
    
    return jsonify({
            "title": homework.title,
            "description": homework.description,
            "created": formated_created,
            "updated": formated_updated,
            }
        ), 200


@bp_homework.get("/homeworks")
@login_required
@swag_from('doc/get_homeworks.yaml')
def get_homeworks():
    homeworks = current_user.homeworks
    out_homeworks = []
    if not homeworks:
        return jsonify({"homeworks": out_homeworks}), 200
    
    for h in homeworks:
        out_homeworks.append({"id": h.id, "title": h.title})
    
    return jsonify({"homeworks": out_homeworks}), 200


    
    



    
        
