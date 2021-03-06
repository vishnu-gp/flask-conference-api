from flask import Blueprint
from flask_restful import Api
from resources.Welcome import Welcome
from resources.Conference import ConferenceResource
from resources.Talk import TalkResource
from resources.TalkUser import TalkUserResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Welcome, '/')
api.add_resource(ConferenceResource, '/Conference')
api.add_resource(TalkResource, '/Talk')
api.add_resource(TalkUserResource, '/Talk/User')