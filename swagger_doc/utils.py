import datetime
import json
import time

from pydantic import BaseModel


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(obj.timestamp() * 1000)
        elif isinstance(obj, datetime.date):
            return int(time.mktime(obj.timetuple()) * 1000)
        elif isinstance(obj, datetime.timedelta):
            return {
                "__type__": "timedelta",
                "days": obj.days,
                "seconds": obj.seconds,
                "microseconds": obj.microseconds,
            }
        elif isinstance(obj, BaseModel):
            return obj.dict()
        elif isinstance(obj, bytes):
            return obj.decode("utf8")
        else:
            return json.JSONEncoder.default(self, obj)
