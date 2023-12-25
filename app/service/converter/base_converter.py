from werkzeug.routing import BaseConverter
import uuid
from flask import jsonify

class UUIDConverter(BaseConverter):

    def to_python(self, value):
        try:
            return uuid.UUID(value)
        except ValueError:
            return jsonify({"NotImplementedError", "UUID cannot convert"}), 403
    
    def to_url(self, value):
        return str(value)