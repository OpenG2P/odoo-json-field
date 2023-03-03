import json

from psycopg2.extras import Json

from odoo import fields


class JSONField(fields.Field):

    type = "json"
    column_type = ("json", "json")

    def convert_to_column(self, value, record, values=None, validate=True):
        if value is None:
            return None
        else:
            return Json(value, dumps=lambda x: json.dumps(x, separators=(",", ":")))

    def convert_to_cache(self, value, record, validate=True):
        if not value:
            return "[]"
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value, separators=(",", ":"))
        return value

    def convert_to_read(self, value, record, use_name_get=True):
        if not value:
            return []
        elif isinstance(value, str):
            return json.loads(value)
        else:
            return value
