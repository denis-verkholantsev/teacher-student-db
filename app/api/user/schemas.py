from marshmallow import Schema, fields, post_load, validate, validates, ValidationError
from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class RegisterUser:
    username: str
    email: str
    password: str
    type: str
    birthdate: date | None = None
    last_name: str | None = None
    first_name: str | None = None


@dataclass
class LoginUser:
    email: str
    password: str


@dataclass
class SearchUser:
    username: str


@dataclass
class AddRelationUser:
    username: str


class LoginUserSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=62))
    password = fields.Str(
        required=True, 
        validate=[
            validate.Length(min=8),
            validate.Regexp(
                regex="[A-Za-z\d@$!%*?&]+",
                error="Password must contain at least one lowercase letter, \
                        one number, and one special character."
            )
        ]
    )
    @post_load
    def make_obj(self, data, **kwargs):
        return LoginUser(**data)


class RegisterUserSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=62))
    password = fields.Str(
        required=True, 
        validate=[
            validate.Length(min=8),
            validate.Regexp(
                regex="[A-Za-z\d@$!%*?&]+",
                error="Password must contain at least one lowercase letter, \
                    one number, and one special character."
            )
        ]
    )
    username = fields.String(
        required=True,
        validate=[
            validate.Length(min=3, max=30, error="Username must be between 3 and 30 characters."),
            validate.Regexp(
                regex='^[a-zA-Z0-9_-]+$',  # Adjust the regex pattern based on your requirements
                error="Invalid characters in username."
            )
        ]
    )

    first_name: str | None = fields.String(
        required=False,
        allow_none=True,
        validate=[
            validate.Length(max=50, error="First name must be between 1 and 50 characters."),
            validate.Regexp(
                regex='^[a-zA-Z-\' -]*$',
                error="Invalid characters in first name."
            )
        ]
    )
    
    last_name: str | None = fields.String(
        required=False,
        allow_none=True,
        validate=[
            validate.Length(max=50, error="Last name must be between 1 and 50 characters."),
            validate.Regexp(
                regex='^[a-zA-Z-\' -]*$',
                error="Invalid characters in last name."
            )
        ]
    )

    birthdate: date | None = fields.Date(
        required=False,
        allow_none=True,
        format='%Y-%m-%d',
        error_messages={"invalid": "Invalid date format. Please use YYYY-MM-DD format."}
    )
    
    @validates('birthdate')
    def validate_birthdate(self, value):
        if value:
            if not isinstance(value, date):
                raise ValidationError("Invalid date format.")
            if value < date(1900, 1, 1):
                raise ValidationError("Birthdate must be after 1900-01-01.")
            if value > date.today():
                raise ValidationError("Birthdate cannot be in the future.")

    type = fields.String(
        required=True,
        validate=[
            validate.OneOf(choices=['teacher', 'student']),
        ]
    )

    @post_load
    def make_obj(self, data, **kwargs):
        return RegisterUser(**data)


class SearchUserSchema(Schema):
    username: str = fields.Str(
           required=True,
        validate=[
            validate.Length(min=3, max=30, error="Username must be between 3 and 30 characters."),
            validate.Regexp(
                regex='^[a-zA-Z0-9_-]+$',  # Adjust the regex pattern based on your requirements
                error="Invalid characters in username."
            )
        ]
    )
    
    @post_load
    def make_obj(self, data, **kwargs):
        return SearchUser(**data)
    

class AddRelationUserSchema(Schema):
    username = fields.Str(
                required=True,
            validate=[
                    validate.Length(min=3, max=30, error="Username must be between 3 and 30 characters."),
                    validate.Regexp(
                        regex='^[a-zA-Z0-9_-]+$',  # Adjust the regex pattern based on your requirements
                        error="Invalid characters in username."
                    )
                ]
        )
    
    @post_load
    def make_obj(self, data, **kwargs):
        return AddRelationUser(**data)


