from json import JSONEncoder

from .models.model import Model


class CustomEncoder(JSONEncoder):

    def default(self, o: object) -> object:
        if isinstance(o, Model):
            return o.json
        # if isinstance(o, FlaskBaseModel):
        #     return o.to_dict(max_nesting=2)
        return JSONEncoder.default(self, o)
