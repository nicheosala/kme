from connexion.apps.flask_app import FlaskJSONEncoder

from .models.model import Model


class CustomEncoder(FlaskJSONEncoder):

    def default(self, o: object) -> object:
        if isinstance(o, Model):
            return o.json
        # if isinstance(o, FlaskBaseModel):
        #     return o.to_dict(max_nesting=2)
        return FlaskJSONEncoder.default(self, o)
