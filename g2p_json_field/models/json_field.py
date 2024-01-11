import json

from psycopg2.extras import Json as PsycopgJson

from odoo import fields


class JSONField(fields.Json):
    def convert_to_column(self, value, record, values=None, validate=True):
        if not value:
            return None
        return PsycopgJson(value, dumps=lambda x: json.dumps(x, separators=(",", ":")))
