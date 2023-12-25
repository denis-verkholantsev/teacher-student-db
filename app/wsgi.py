from flask import Flask
from config import DevelopmentConfig
from service.db.models import db, User
from service.converter.base_converter import UUIDConverter
from service.spec.spec_template import get_template
from flask_migrate import Migrate
from flasgger import Swagger
from flask_login import LoginManager
from api.user.endpoints import bp_log_reg, bp_user
from api.homework.endpoints import bp_homework
from api.exercise.endpoints import bp_exercise
from api.solution.endpoints import bp_solution
from api.file.endpoints import bp_file
from api.event.endpoints import bp_event
from flask.cli import FlaskGroup


app = Flask(__name__)
app.config.from_object(DevelopmentConfig())
app.url_map.converters['uuid'] = UUIDConverter
app.register_blueprint(bp_log_reg)
app.register_blueprint(bp_user)
app.register_blueprint(bp_homework)
app.register_blueprint(bp_solution)
app.register_blueprint(bp_exercise)
app.register_blueprint(bp_file)
app.register_blueprint(bp_event)
db.init_app(app)
migrate = Migrate(app=app, db=db, directory="app/service/db/migrations")
lm = LoginManager(app)
swagger = Swagger(app, template=get_template(app), parse=True)

@lm.user_loader
def load_user(id):
    return User.query.get(id)




