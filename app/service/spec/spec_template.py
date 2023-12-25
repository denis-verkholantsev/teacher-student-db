from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec
from api.user.schemas import LoginUserSchema,  RegisterUserSchema, SearchUserSchema, AddRelationUserSchema
from api.homework.schemas import PostHomeworkSchema
from api.exercise.schemas import PostExerciseSchema
from api.file.schemas import PostFileSchema
from api.solution.schemas import PostSolutionSchema
from api.event.schemas import PostEventSchema


def get_template(app):
    plugins = [FlaskPlugin(), MarshmallowPlugin()]
    spec = APISpec("My api docs", '1.0', "2.0", plugins=plugins)
    template = spec.to_flasgger(app, definitions=[
                                    LoginUserSchema,  
                                    RegisterUserSchema,
                                    SearchUserSchema, 
                                    AddRelationUserSchema,
                                    PostHomeworkSchema,
                                    PostFileSchema,
                                    PostExerciseSchema,
                                    PostSolutionSchema,
                                    PostEventSchema,
                                    ]
                                    )
    
    return template

    