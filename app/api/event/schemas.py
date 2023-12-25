from marshmallow import Schema, fields, validate, post_load, validates, ValidationError, validates_schema
from dataclasses import dataclass
from typing import List
from uuid import UUID
from datetime import datetime

@dataclass
class PostEvent:
    title: str
    start: str
    end: str
    description: str | None = None
    students: List[UUID]  | None = None

@dataclass
class GetEvent:
    start: str
    end: str



class PostEventSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(max=50))
    description = fields.Str(required=False, validate=validate.Length(max=500))
    students = fields.List(fields.UUID(), required=False, allow_none=True)
    start = fields.Str(
        required=True,
        format='%Y-%m-%dT%H:%M:%S',
        error_messages={"invalid": "Invalid date format. Please use YYYY-MM-DD HH:MM:SS format."}
    )
    end = fields.Str(
        required=True,
        format='%Y-%m-%dT%H:%M:%S',
        error_messages={"invalid": "Invalid date format. Please use YYYY-MM-DD HH:MM:SS format."}
    )

    @validates('start')
    def validate_start(self, value):
        try:
            start_datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except ValueError as err:
            raise ValidationError(str(err))
        if start_datetime < datetime.today():
            raise ValidationError(str(err))

    @validates('end')
    def validate_end(self, value):
        try:
            end_datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except ValueError as err:
            raise ValidationError(str(err))

    @validates_schema
    def validate_dates(self, data, **kwargs):
        start = datetime.strptime(data['start'], "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(data['end'], "%Y-%m-%dT%H:%M:%S")

        if start > end:
            raise ValidationError("Start datetime must be before or equal to End datetime.")

    @post_load
    def make_obj(self, data, **kwargs):
        return PostEvent(**data)
    


class GetEventSchema(Schema):
    start = fields.Str(
        required=True,
        format='%Y-%m-%dT%H:%M:%S',
        error_messages={"invalid": "Invalid date format. Please use YYYY-MM-DD HH:MM:SS format."}
    )
    end = fields.Str(
        required=True,
        format='%Y-%m-%dT%H:%M:%S',
        error_messages={"invalid": "Invalid date format. Please use YYYY-MM-DD HH:MM:SS format."}
    )
    @post_load
    def make_obj(self, data, **kwargs):
        return GetEvent(**data)
    
    @validates('start')
    def validate_start(self, value):
        try:
            start_datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except ValueError as err:
            raise ValidationError(str(err))

    @validates('end')
    def validate_end(self, value):
        try:
            end_datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except ValueError as err:
            raise ValidationError(str(err))

    @validates_schema
    def validate_dates(self, data, **kwargs):
        start = datetime.strptime(data['start'], "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(data['end'], "%Y-%m-%dT%H:%M:%S")

        if start > end:
            raise ValidationError("Start datetime must be before or equal to End datetime.")
