from marshmallow import Schema, fields, validate, post_load, validates, ValidationError
from dataclasses import dataclass
from typing import List
from uuid import UUID
from datetime import datetime

@dataclass
class PostHomework:
    title: str
    deadline: str
    description: str | None = None
    files: List[UUID] | None = None
    exercises: List[UUID] | None = None
    students: List[UUID]  | None = None
    

class PostHomeworkSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(max=50))
    description = fields.Str(required=False, validate=validate.Length(max=500))
    files = fields.List(fields.UUID(), required=False, allow_none=True)
    exercises = fields.List(fields.UUID(), required=False, allow_none=True)
    students = fields.List(fields.UUID(), required=False, allow_none=True)
    deadline = fields.Str(
        required=True,
        format='%Y-%m-%dT%H:%M:%S',
        error_messages={"invalid": "Invalid date format. Please use YYYY-MM-DD HH:MM:SS format."}
    )

    @validates('deadline')
    def validate_deadline(self, value):
        try:
            parsed_deadline = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except ValueError as err:
            return ValidationError(str(err))
        if parsed_deadline:
            if not isinstance(parsed_deadline, datetime):
                return ValidationError("Invalid datetime format.")
            if parsed_deadline <= datetime.now():
                return ValidationError("Deadline cannot be in previous")

    @post_load
    def make_obj(self, data, **kwargs):
        return PostHomework(**data)