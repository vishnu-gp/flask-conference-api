from flask import request
from flask_restful import Resource
from Model import db, Conference, ConferenceSchema, Talk, TalkSchema, User, UserSchema
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload, subqueryload


talk_schema = TalkSchema()
user_schema = UserSchema()

response = {'status': 'success'}
error_response = {'status': 'error', 'message': 'Request failed.'}

class TalkUserResource(Resource):
    # To add user to a talk as speaker or participant
    def post(self):
        input_data = request.get_json()
        if not input_data:
            error_response['message'] = 'No input data'

            return error_response, 400
        
        try:
            user_type = input_data.pop('user_type')
            talk = Talk.query.filter_by(id=input_data.pop('talk_id')).first()
            if not talk:
                error_response['message'] = 'Talk not found'

                return error_response, 400
            
            data = user_schema.load(input_data)

            user = User.query.where(User.username==data['username']).where(User.email==data['email']).first()
            if not user:
                user = User(
                    username=data['username'],
                    email=data['email']
                )
                db.session.add(user)
            if(user_type == 'speaker'):
                talk.speakers.append(user)
            else:
                talk.participants.append(user)
            db.session.add(talk)
            db.session.commit()

       
            response['data'] = talk_schema.dump(talk)

            return response, 201
        except ValidationError as err:
            error_response['errors'] = err.messages

            return error_response, 400
        except:
            return error_response, 400

    # To delete a user as a participant or speaker
    def delete(self):
        input_data = request.get_json()
        if not input_data:
            error_response['message'] = 'No input data'

            return error_response, 400
        
        try:
            user_type = input_data.pop('user_type')
            talk = Talk.query.filter_by(id=input_data.pop('talk_id')).first()
            if not talk:
                error_response['message'] = 'Talk not found'

                return error_response, 400
            
            data = user_schema.load(input_data)

            user = User.query.where(User.username==data['username']).where(User.email==data['email']).first()
            if not user:
                error_response['message'] = 'User not found'

                return error_response, 400
            if(user_type == 'speaker'):
                talk.speakers.remove(user)
            else:
                talk.participants.remove(user)
            db.session.add(talk)
            db.session.commit()

       
            response['data'] = talk_schema.dump(talk)

            return response, 201
        except ValidationError as err:
            error_response['errors'] = err.messages

            return error_response, 400
        except:
            return error_response, 400
        