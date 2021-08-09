from flask import request
from flask_restful import Resource
from Model import db, Conference, ConferenceSchema, Talk, TalkSchema
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload, subqueryload

talks_schema = TalkSchema(many=True)
talk_schema = TalkSchema()

response = {'status': 'success'}
error_response = {'status': 'error', 'message': 'Request failed.'}

class TalkResource(Resource):
    # To list all talk in a particular conference
    def get(self):
        conference_id = request.args.get('conference_id')
        if(not conference_id):
            error_response['message'] = 'No conference id passed.'

            return error_response, 400
        conference = db.session.query(Conference).filter_by(id=conference_id).first()
        if not conference:
            error_response['message'] = 'Conference does not exist.'

            return error_response, 400
        talks = talks_schema.dump(conference.talks)
        response['data'] = talks

        return response, 200