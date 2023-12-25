from marshmallow import Schema, fields, validate, post_load, validates, ValidationError
from dataclasses import dataclass
from typing import List
from uuid import UUID
from datetime import datetime

@dataclass
class PostFile:
    filename: str
    filedata: bytes | None = None
    

class PostFileSchema(Schema):
    filename = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    filedata = fields.Str(required=False)
    @post_load
    def make_obj(self, data, **kwargs):
        return PostFile(**data)
        