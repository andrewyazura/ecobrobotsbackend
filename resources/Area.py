from os import environ
from urllib.parse import parse_qs

from flask_restful import Resource, request
from models import AreaModel
from sqlalchemy import desc
from common.convert_types_to_names import convert_types_to_names


class Area(Resource):
    def get(self):
        try:
            args = request.query_string

            if not args:
                args = environ.get('QUERY_STRING')  # if using CGI server

            args = parse_qs(args).items()

            try:
                args = [(i[0].decode('utf-8'), i[1][0].decode('utf-8'))
                        for i in args]
            except:
                args = [(i[0], i[1][0]) for i in args]

            latitude, longitude = args[0][1], args[1][1]
            area = AreaModel.query \
                .filter_by(latitude=latitude) \
                .filter_by(longitude=longitude) \
                .order_by(desc(AreaModel.created)).first()

            if not area:
                return {'code': 404, 'message': 'Area not found'}, 404

        except:
            return {'code': 404, 'message': 'Area not found'}, 404

        return convert_types_to_names(area)
