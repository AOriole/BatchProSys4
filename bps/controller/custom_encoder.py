import json
import datetime


class CustomEncoder(json.JSONEncoder):
    def default(self, o):                       # o stands for obj
        if "to_json" in dir(o):
            return o.to_json()
        elif isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)
