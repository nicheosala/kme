from json import JSONEncoder

from .models.model import Model


class CustomEncoder(JSONEncoder):

    def default(self, o: object) -> object:
        if isinstance(o, Model):
            return o.json
        return JSONEncoder.default(self, o)
