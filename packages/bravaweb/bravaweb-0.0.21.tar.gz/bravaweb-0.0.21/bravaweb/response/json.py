
import json
import datetime
import decimal

# configuration
import configuration

from bravaweb.response.lib.object import ResponseObject
from bravaweb.utils.encoder import CustomEncoder

class Json(ResponseObject):

    def Response(self, data, success=True, **args):
        _data = data

        _template = dict(self.template)
        _template["date"] = datetime.datetime.now()
        _template["itens"] = 0
        if success:

            if hasattr(_data, 'toJSON'):
                _data = _data.toJSON()

            _template["data"] = _data
            _template["date"] = datetime.datetime.now()

            try:
                _template["itens"] = len(_data) if isinstance(_data, list) else 1
            except TypeError:
                _template["itens"] = 1
            except Exception as e:
                _template["itens"] = 0

            for k,v in args.items():
                _template[k] = v

        else:
            _template["success"] = False
            _template["data"] = _data
            _template["date"] = datetime.datetime.now()
            _template["error"] = args["error"] if "error" in args else "Invalid Request"

        return json.dumps(_template, cls=CustomEncoder, indent=4).encode(configuration.api.encoding)
