from service.db.models import FileStorage, Homework, Exercise, Student
from flask import request, jsonify, session, Blueprint
from api.exercise.schemas import PostExerciseSchema, PostExercise
from marshmallow import ValidationError
from flask_login import login_user, current_user, login_required, logout_user
from wsgi import db
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from api.common import teacher_required, student_required, validate_id
from datetime import datetime
from flasgger import swag_from
bp_exercise = Blueprint('exercise', __name__, url_prefix='/user')


@bp_exercise.post("/exercise")
@login_required
@teacher_required
@swag_from('doc/post.yaml')
def post_exercise():
    try:
        data = request.get_json()
        exercise_schema = PostExerciseSchema()
        exercise_data: PostExercise = exercise_schema.load(data)
    except ValidationError as err:
        return jsonify({"message": "Validation Error", "errors": err.messages}), 400
    files=None
    if exercise_data.files:
        files = db.session.query(FileStorage).filter(FileStorage.user_id == current_user.id).filter(FileStorage.id.in_(set(exercise_data.files))).all()

    exercise = Exercise(
                title=exercise_data.title,
                description=exercise_data.description,
                )
    
    if files:
        exercise.files.update(files)
        
    exercise.teacher_id = current_user.id
    db.session.add(exercise)    
    db.session.commit()
    return jsonify({"id": exercise.id}), 200

    
@bp_exercise.get("/exercises")
@login_required
@teacher_required
@swag_from('doc/get_exercises.yaml')
def get_exercises():
    exercises = current_user.exercises
    out_exs = []
    if not exercises:
        return jsonify({"exercises": out_exs}), 200
    
    for e in exercises:
        out_exs.append({"id": e.id, "title": e.title})
    
    return jsonify({"exercises": out_exs}), 200
    

@bp_exercise.get("/exercises/<uuid:exercise_id>")
@login_required
@teacher_required
@swag_from('doc/get_about_from_teacher.yaml')
def get_about_from_teacher(exercise_id):
    if not validate_id(exercise_id):
        return jsonify({"meassage": "No instances of UUID"}), 403

    exercise = db.session.query(Exercise).filter(Exercise.id == exercise_id).filter(Exercise.teacher_id == current_user.id).first()

    if not exercise:
        return jsonify({"message": "exercise not found"}), 404

    
    return jsonify({
        "title": exercise.title,
        "description": exercise.description,
        "created": exercise.created,
        "updated": exercise.updated,
        "homeworks": [{"id": h.id, "username": h.title} for h in exercise.homeworks]
        }
    ), 200


@bp_exercise.get("homeworks/<uuid:homewrok_id>/exercises/<uuid:exercise_id>")
@login_required
@student_required
@swag_from('doc/get_about_from_student.yaml')
def get_about_from_student(homework_id, exercise_id):

    if not validate_id(exercise_id) or not validate_id(homework_id):
        return jsonify({"meassage": "No instances of UUID"}), 403
    

    exercise = db.session.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return jsonify({"message": "exercise not found"}), 404
    
    homework = db.session.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        return jsonify({"message": "homework not found"}), 404
    
    student = db.session.query(Student).filter(Student.id == current_user.id).first()

    if exercise not in homework.exercises or student not in homework.students:
        return jsonify({"message": "exercise not found"}), 404

    
    return jsonify({
        "title": exercise.title,
        "description": exercise.description,
        "created": exercise.created,
        "updated": exercise.updated,
        }
    ), 200




@bp_exercise.get("homework/<uuid:homework_id>/exercises")
@login_required
@swag_from('doc/get_homework_exercises.yaml')
def get_homework_exercises(homework_id):
    if not validate_id(homework_id):
        return jsonify({"meassage": "No instances of UUID"}), 403

    homework = db.session.query(Homework).filter(Homework.id == homework_id).first()

    if not homework:
        return jsonify({"message": "homework not found"}), 404
    
    if current_user.type == "student":
        student = db.session.query(Student).filter(Student.id == current_user.id).first()
        if student not in homework.students:
            return jsonify({"message": "homework not found"}), 403
    else:
        if homework.teacher_id != current_user.id:
            return jsonify({"message": "homework not found"}), 403
    
    return jsonify({
        "exercises": [{"id": e.id, "title": e.title} for e in homework.exercises]
    }), 200
    
