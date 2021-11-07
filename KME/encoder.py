from connexion.apps.flask_app import FlaskJSONEncoder

from .models.base_model_ import Model


class JSONEncoder(FlaskJSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return o.to_dict()
        return FlaskJSONEncoder.default(self, o)
