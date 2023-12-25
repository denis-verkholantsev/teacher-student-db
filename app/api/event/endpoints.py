from service.db.models import FileStorage, Homework, Exercise, Student, Homework, Event
from flask import request, jsonify, session, Blueprint
from api.event.schemas import PostEventSchema, PostEvent, GetEventSchema, GetEvent
from marshmallow import ValidationError
from flask_login import current_user, login_required
from wsgi import db
from sqlalchemy import and_
from flasgger import swag_from
from dataclasses import asdict
from api.common import is_base64, validate_id, teacher_required
from base64 import b64decode
from datetime import datetime

bp_event = Blueprint('event', __name__, url_prefix="/user")


@bp_event.post('/event')
@login_required
@teacher_required
@swag_from('doc/post.yaml')
def post_event():
    try:
        data = request.get_json()
        post_event_schema = PostEventSchema()
        event_data: PostEvent = post_event_schema.load(data)
        formated_start = datetime.strptime(event_data.start, '%Y-%m-%dT%H:%M:%S')
        formated_end = datetime.strptime(event_data.end, '%Y-%m-%dT%H:%M:%S')
    except ValidationError as err:
        return jsonify({"message": "Validation Error", "errors": err.messages}), 400
    except ValueError as err:
         return jsonify({"message": "Value Error", "errors": str(err)}), 400

    event = Event(title=event_data.title, 
                  description=event_data.description,
                  start=formated_start,
                  end=formated_end
                  )
    students = db.session.query(Student).filter(Student.id.in_(event_data.students)).all()
    db.session.add(event)
    event.teacher_id = current_user.id
    event.students.update(students)
    db.session.commit()
    return jsonify({"id": event.id}), 200


@bp_event.get('/timetable')
@login_required
@swag_from('doc/get_timetable.yaml')
def get_timetable():
    try:
        data = request.args
        get_event_schema = GetEventSchema()
        event_data: GetEvent = get_event_schema.load(data)
        formated_start = datetime.strptime(event_data.start, '%Y-%m-%dT%H:%M:%S')
        formated_end = datetime.strptime(event_data.end, '%Y-%m-%dT%H:%M:%S')
    except ValidationError as err:
        return jsonify({"message": "Validation Error", "errors": err.messages}), 400
    except ValueError as err:
         return jsonify({"message": "Value Error", "errors": str(err)}), 400
    
    events = None
    if current_user.type == "student":
        student = db.session.query(Student).filter(Student.id == current_user.id).first()
        events = []
        for e in student.events:
            if formated_end >= e.end and formated_start <= e.start:
                events.append(e)
        return jsonify({"events": [{"id": e.id, "title": e.title, "start": e.start, "end": e.end, "teacher": e.teacher_id} for e in events]}), 200
    else:
        events = db.session.query(Event).filter(Event.teacher_id == current_user.id).filter(and_(
            Event.start >= formated_start,
            Event.end <= formated_end
            )
        )
    
    if not events:
        return jsonify({"events": {}}), 200

    return jsonify({"events": [{"id": e.id, 
                                "title": e.title, 
                                "start": e.start, 
                                "end": e.end, 
                                "students": [{"id": s.id, "username": s.username} for s in e.students]}
                                for e in events]}), 200
    
    
    
    