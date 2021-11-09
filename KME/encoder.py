from json import JSONEncoder

from .models.base_model_ import Model


class CustomEncoder(JSONEncoder):

    def default(self, o: object) -> object:
        return o.to_dict() if isinstance(o, Model) else JSONEncoder.default(self, o)
