from json.encoder import JSONEncoder


class Encoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, 'json_dict'):
            return o.json_dict()
        else:
            return o.__dict__
