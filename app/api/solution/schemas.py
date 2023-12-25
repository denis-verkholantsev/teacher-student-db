from marshmallow import Schema, fields, validate, post_load, validates, ValidationError
from dataclasses import dataclass
from typing import List
from uuid import UUID
from datetime import datetime


@dataclass
class PostSolution:
    description: str | None = None
    files: List[UUID] | None = None


@dataclass
class SearchSolution:
    student_id: UUID | None = None
    

class PostSolutionSchema(Schema):
    description = fields.Str(required=False, validate=validate.Length(max=500))
    files = fields.List(fields.UUID(), required=False, allow_none=True)
    @post_load
    def make_obj(self, data, **kwargs):
        return PostSolution(**data)


class SearchSolutionSchema(Schema):
    student_id: UUID = fields.UUID(required=False)
        