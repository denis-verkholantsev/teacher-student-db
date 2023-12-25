from werkzeug.routing import BaseConverter
import uuid

class UUIDConverter(BaseConverter):

    def to_python(self, value):
        try:
            return uuid.UUID(value)
        except ValueError:
            raise NotImplementedError("UUID cannot convert")
    
    def to_url(self, value):
        return str(value)