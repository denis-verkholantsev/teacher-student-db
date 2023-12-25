from service.db.models import FileStorage, Homework, Exercise, Solution, Student
from flask import request, jsonify, session, Blueprint
from api.solution.schemas import PostSolutionSchema, PostSolution, SearchSolution, SearchSolutionSchema
from marshmallow import ValidationError
from flask_login import login_user, current_user, login_required, logout_user
from wsgi import db
from sqlalchemy.exc import IntegrityError
from api.common import teacher_required, student_required
from datetime import datetime
from flasgger import swag_from
import json
from api.common import validate_id
from uuid import UUID

bp_solution = Blueprint('solution', __name__, url_prefix='/exercise')

@bp_solution.post("/<uuid:exercise_id>/solution")
@login_required
@student_required
@swag_from('doc/post.yaml')
def post_solution(exercise_id):

    if not validate_id(exercise_id):
        return jsonify({"meassage": "No instances of UUID"}), 403

    try:
        data = request.get_json()
        solution_schema = PostSolutionSchema()
        solution_data: PostSolution = solution_schema.load(data)
    except ValidationError as err:
        return jsonify({"message": "Validation Error", "errors": err.messages}), 400
    
    files = db.session.query(FileStorage).filter(FileStorage.user_id==current_user.id).filter(FileStorage.id.in_(solution_data.files)).all()
    exercise = db.session.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if not exercise:
        return jsonify({"message": "exercise not found"})

    student = db.session.query(Student).filter(Student.id == current_user.id).first()

    if not len(student.homeworks.intersection(exercise.homeworks)):
        return jsonify({"message": "exercise not found"})
    
    solution = Solution(description=solution_data.description)
    solution.student = student
    solution.exercise = exercise
    db.session.add(solution)
    solution.files.update(files)
    db.session.commit()
    
    return jsonify({"id": solution.id}), 200


@bp_solution.get("/<uuid:exercise_id>/solutions/<uuid:solution_id>")
@login_required
@swag_from('doc/get_about.yaml')
def get_about(exercise_id, solution_id):

    if not validate_id(exercise_id) or not validate_id(solution_id):
        return jsonify({"meassage": "No instances of UUID"}), 403

    exercise = db.session.query(Exercise).filter(Exercise.id == exercise_id).first()

    if not exercise:
        return jsonify({"message": "exercise not found"}), 404

    solution = db.session.query(Solution).filter(Solution.id == solution_id).filter(Solution.exercise_id == exercise_id).first()

    if not solution:
        return jsonify({"message": "solution not found"}), 404
    
    if current_user.type == "teacher":
        if exercise.teacher_id != current_user.id:
            return jsonify({"message": "solution not found"}), 404
    else:
        if solution.student_id != current_user.id:
            return jsonify({"message": "solution not found"}), 404
        
    formated_created = formated_updated = None
    if solution.created:
        formated_created = solution.created.strftime("%Y-%m-%dT%H:%M:%S")
    if solution.updated:
        formated_updated = solution.updated.strftime("%Y-%m-%dT%H:%M:%S")
    
    return jsonify({"author": solution.student_id,
                    "description": solution.description,
                    "created": formated_created,
                    "updated": formated_updated,
                    "status": solution.status
                    }
                ), 200


@bp_solution.get("/<uuid:exercise_id>/solutions")
@login_required
@swag_from('doc/get_exercise_solutions.yaml')
def get_exercise_solution(exercise_id):
    
    if not validate_id(exercise_id):
        return jsonify({"message": "No instances of UUID"}), 403
    
    student_id = None
    try:
        student_id = UUID(request.args.get('student_id'))
    except TypeError:
        pass

    if student_id:
        if not validate_id(student_id):
            return jsonify({"message": "No instances of UUID"}), 403
    

    exercise = db.session.query(Exercise).filter(Exercise.id == exercise_id).first()

    if not exercise:
        return jsonify({"message": "exercise not found"}), 404

    solutions = None

    if current_user.type == "teacher":
        if exercise.teacher_id != current_user.id:
            return jsonify({"message": "exercise not found"}), 404
        
        if student_id:
            solutions = db.session.query(Solution).filter(Solution.exercise_id == exercise_id).filter(Student.id == student_id).all()
        else:
            solutions = db.session.query(Solution).filter(Solution.exercise_id == exercise_id).all()

    else:
        if not student_id or student_id == current_user.id:
            solutions = db.session.query(Solution).filter(Solution.exercise_id == exercise_id).filter(Solution.student_id == current_user.id).all()
        
    if not solutions:
        return jsonify({"solutions": []}), 200
    
    return jsonify({"solutions": [{"id": s.id, "author": s.student_id} for s in solutions]})
    

@bp_solution.put("/<uuid:exercise_id>/<uuid:solution_id>/status")
@login_required
@teacher_required
@swag_from('doc/put_solution_status.yaml')
def put_solution_status(exercise_id, solution_id):

    if not validate_id(exercise_id) or not validate_id(solution_id):
        return jsonify({"message": "No instances of UUID"}), 403
    
    exercise =  db.session.query(Exercise).filter(Exercise.id == exercise_id).filter(Exercise.teacher_id == current_user.id).first()
    if not exercise:
        return jsonify({"message": "exercise not found"}), 404

    solution = db.session.query(Solution).filter(Solution.id == solution_id).filter(Solution.exercise_id == exercise_id).first()
    if not solution:
        return jsonify({"message": "exercise not found"}), 404
    
    solution.status = "approved"
    db.session.commit()

    return jsonify(), 200




    

    

