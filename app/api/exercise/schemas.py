from marshmallow import Schema, fields, validate, post_load, validates, ValidationError
from dataclasses import dataclass
from typing import List
from uuid import UUID
from datetime import datetime

@dataclass
class PostExercise:
    title: str | None = None
    description: str | None = None
    files: List[UUID] | None = None
    

class PostExerciseSchema(Schema):
    title = fields.Str(required=False, validate=validate.Length(max=50))
    description = fields.Str(required=False, validate=validate.Length(max=500))
    files = fields.List(fields.UUID(), required=False, allow_none=True)
    @post_load
    def make_obj(self, data, **kwargs):
        return PostExercise(**data)
        