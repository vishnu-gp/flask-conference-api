from flask import request
from flask_restful import Resource
from Model import db, Conference, ConferenceSchema

conferences_schema = ConferenceSchema(many=True)
conference_schema = ConferenceSchema()
response = {'status': 'success'}

class ConferenceResource(Resource):
    def get(self):
        conferences = Conference.query.all()
        conferences = conferences_schema.dump(conferences)
        response['data'] = conferences
        return response, 200