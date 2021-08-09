from flask import request
from flask_restful import Resource
from Model import db, Conference, ConferenceSchema
from marshmallow import ValidationError

conferences_schema = ConferenceSchema(many=True)
conference_schema = ConferenceSchema()
response = {'status': 'success'}
error_response = {'status': 'error', 'message': 'Request failed.'}

class ConferenceResource(Resource):
    # To list all conferences
    def get(self):
        conferences = Conference.query.all()
        conferences = conferences_schema.dump(conferences)
        response['data'] = conferences

        return response, 200

    # To create a conference
    def post(self):
        input_data = request.get_data()
        if not input_data:
            error_response['message'] = 'No input data'

            return error_response, 400
        try:
            data = conference_schema.loads(input_data)
            conference = Conference(
                title=data['title'],
                description=data['description'] if 'description' in data else None,
                start_date=data['start_date'],
                end_date=data['end_date'],
                talks=[]
            )
            db.session.add(conference)
            db.session.commit()
            response['data'] = conference_schema.dump(conference)

            return response, 201
        except ValidationError as err:
            error_response['errors'] = err.messages
        except:
            return error_response, 400

    # To edit a conference
    def patch(self):
        input_data = request.get_data()
        if not input_data:
            error_response['message'] = 'No input data.'

            return error_response, 400
        try:
            data = conference_schema.loads(input_data, partial=True)
            if(not 'id' in data):
                error_response['message'] = 'No conference id passed.'

                return error_response, 400
            conference = Conference.query.filter_by(id=data['id']).first()
            if not conference:
                error_response['message'] = 'Conference does not exist.'
                
                return error_response, 400
            for key in data:
                setattr(conference, key, data[key])
            db.session.commit()
            response['data'] = conference_schema.dump(conference)

            return response, 201
        except ValidationError as err:
            error_response['errors'] = err.messages

            return error_response, 400