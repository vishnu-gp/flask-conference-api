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
        conference = Conference.query.filter_by(id=conference_id).first()
        if not conference:
            error_response['message'] = 'Conference does not exist.'

            return error_response, 400
        talks = talks_schema.dump(conference.talks)
        response['data'] = talks

        return response, 200

    # To add a talk
    def post(self):
        input_data = request.get_data()
        if not input_data:
            error_response['message'] = 'No input data'

            return error_response, 400
        try:
            data = talk_schema.loads(input_data)

            conference = Conference.query.filter_by(id=data['conference_id']).first()
            if not conference:
                error_response['message'] = 'Conference does not exist.'

                return error_response, 400
            talk = Talk(
                title=data['title'],
                description=data['description'] if 'description' in data else None,
                scheduled_at=data['scheduled_at'],
                duration_min=data['duration_min'],
                speakers=[],
                participants=[]
            )
            talk.conference_id = conference.id
            db.session.add(talk)
            db.session.commit()
            response['data'] = talk_schema.dump(talk)

            return response, 201
        except ValidationError as err:
            error_response['errors'] = err.messages

            return error_response, 400
        except:
            return error_response, 400
    
    # To edit a talk
    def patch(self):
        input_data = request.get_data()
        if not input_data:
            error_response['message'] = 'No input data.'

            return error_response, 400
        try:
            data = talk_schema.loads(input_data, partial=True)
            if(not 'id' in data):
                error_response['message'] = 'No talk id passed.'

                return error_response, 400
            talk = Talk.query.filter_by(id=data['id']).first()
            if not talk:
                error_response['message'] = 'Talk does not exist.'

                return error_response, 400
            if('conference_id' in data):
                conference = Conference.query.filter_by(id=data['conference_id']).first()
                if not conference:
                    error_response['message'] = 'Conference does not exist.'

                    return error_response, 400
            for key in data:
                setattr(talk, key, data[key])
            db.session.commit()
            response['data'] = talk_schema.dump(talk)

            return response, 201
        except ValidationError as err:
            error_response['errors'] = err.messages

            return error_response, 400
        except:
            return error_response, 400