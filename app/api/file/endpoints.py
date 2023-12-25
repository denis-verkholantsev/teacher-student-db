from service.db.models import FileStorage, Homework, Exercise, Student, Homework
from flask import request, jsonify, session, Blueprint
from api.file.schemas import PostFileSchema, PostFile
from marshmallow import ValidationError
from flask_login import current_user, login_required
from wsgi import db
from flasgger import swag_from
from dataclasses import asdict
from api.common import validate_id, teacher_required, student_required


bp_file = Blueprint('file', __name__, url_prefix='/user')


@bp_file.post("/file")
@login_required
@swag_from('doc/post.yaml')
def post_exercise():
    try:
        data = request.get_json()
        file_schema = PostFileSchema()
        file_data: PostFile = file_schema.load(data)
        file_data.filedata = file_data.filedata.encode('utf-8')

    except ValidationError as err:
        return jsonify({"message": "Validation Error", "errors": err.messages}), 400


    file = FileStorage(filename=file_data.filename, filedata=file_data.filedata)
    file.user_id = current_user.id

    db.session.add(file)    
    db.session.commit()
    return jsonify({"file_id": file.id}), 200


@bp_file.get('/files')
@login_required
@swag_from('doc/get_files.yaml')
def get_files():

    if not current_user.files:
        return jsonify({"files": []}), 200
    
    return jsonify({"files": [{"id": f.id, "title": f.filename} for f in current_user.files]}), 200


@bp_file.get('/homeworks/<uuid:homework_id>/files')
@login_required
@swag_from('doc/get_homework_files.yaml')
def get_homework_files(homework_id):

    if not validate_id(homework_id):
        return jsonify({"message": "No instances of UUID"}), 403
    
    homework = db.session.query(Homework).filter(Homework.id == homework_id).first()

    if not homework:
        return jsonify({"message": "homework not found"}), 404
    
    if current_user.type == "student":
        student = db.session.query(Student).filter(Student.id == current_user.id).first()
        if student not in homework.students:
            return jsonify({"message": "homework not found"}), 404
    else:
        if homework.teacher_id != current_user.id:
            return jsonify({"message": "homework not found"}), 404
        
    if not homework.files:
        return jsonify({"files": []}), 200
    
    return jsonify({"files": [{"id": f.id, "title": f.filename} for f in homework.files]}), 200


@bp_file.get('/exercises/<uuid:exercise_id>/files/')
@login_required
@swag_from('doc/get_exercise_files.yaml')
def get_exercise_files(exercise_id):
    if not validate_id(exercise_id):
        return jsonify({"message": "No instances of UUID"}), 403
    
    exercise = db.session.query(Exercise).filter(Exercise.id == exercise_id).first()

    if not exercise:
        return jsonify({"message": "exercise not found"}), 404
    
    if current_user.type == "student":
        
        student = db.session.query(Student).filter(Student.id == current_user.id).first()

        if not student.homeworks:
            return jsonify({"message": "exercise not found"}), 404
        
        
        for h in student.homeworks:
            if exercise in h.exercises:
                rights = True
                break
        
        if not rights:
            return jsonify({"message": "exercise not found"}), 404
    
    else:
        if exercise.teacher_id != current_user.id:
            return jsonify({"message": "exercise not found"}), 404
    

    if not exercise.files:
        return jsonify({"files": []}), 200
    
    return jsonify({"files": [{"id": f.id, "title": f.filename} for f in exercise.files]}), 200



@bp_file.get('files/<uuid:file_id>')
@login_required
@swag_from('doc/get_about.yaml')
def get_about(file_id):

    if not validate_id(file_id):
        return jsonify({"message": "No instances of UUID"}), 403
    
    file = db.session.query(FileStorage).filter(FileStorage.id == file_id).filter(FileStorage.user_id == current_user.id).first()

    if not file:
        return jsonify({"message": "file not found"}), 404

    return jsonify({"filename": file.filename, "filedata": file.filedata.decode('utf-8')}), 200


@bp_file.get('exercises/<uuid:exercise_id>/files/<uuid:file_id>')
@login_required
@teacher_required
@swag_from('doc/get_exercise_file_about.yaml')
def get_exercise_file_about(exercise_id, file_id):

    exercise = db.session.query(Exercise).filter(Exercise.id == exercise_id).filter(Exercise.teacher_id == current_user.id).first()
    if not exercise:
        return jsonify({"message" : "exercise not found"}), 404
    
    file = db.session.query(FileStorage).filter(FileStorage.id == file_id).filter(FileStorage.user_id == current_user.id).first()

    if file not in exercise.files:
        return jsonify({"message" : "file not found"}), 404
    
    return jsonify({"filename": file.filename, "filedata": file.filedata.decode('utf-8')}), 200
    

@bp_file.get('homeworks/<uuid:homework_id>/exercises/<uuid:exercise_id>/files/<uuid:file_id>')
@login_required
@swag_from('doc/get_homework_exercise_file_about.yaml')
def get_homework_exercise_file_about(homework_id, exercise_id, file_id):

    homework = db.session.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        return jsonify({"message" : "homework not found"}), 404
    
    if current_user.type == "student":
        student = db.session.query(Student).filter(Student.id == current_user.id).first()
    
        if not student in homework.students:
            return jsonify({"message" : "homework not found"}), 404
    else:
        if homework.teacher_id != current_user.id:
            return jsonify({"message" : "homework not found"}), 404

    exercise = db.session.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return jsonify({"message" : "exercise not found"}), 404
    
    if exercise not in homework.exercises:
        return jsonify({"message" : "exercise not found"}), 404
    
    file = db.session.query(FileStorage).filter(FileStorage.id == file_id).first()

    if file not in exercise.files:
        return jsonify({"message" : "file not found"}), 404
    
    return jsonify({"filename": file.filename, "filedata": file.filedata.decode('utf-8')}), 200


@bp_file.get('homeworks/<uuid:homework_id>/files/<uuid:file_id>')
@login_required
@swag_from('doc/get_homework_file_about.yaml')
def get_homework_file_about(homework_id, file_id):

    homework = db.session.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        return jsonify({"message" : "homework not found"}), 404
    
    if current_user.type == "teacher":

        if homework.teacher_id != current_user.id:
            return jsonify({"message" : "homework not found"}), 404
    else:
        student = db.session.query(Student).filter(Student.id == current_user.id).first()
    
        if not student in homework.students:
            return jsonify({"message" : "homework not found"}), 404
    
    file = db.session.query(FileStorage).filter(FileStorage.id == file_id).first()

    if file not in homework.files:
        return jsonify({"message" : "file not found"}), 404
    
    return jsonify({"filename": file.filename, "filedata": file.filedata.decode('utf-8')}), 200


    

