from flask import Blueprint
from flask_restful import Api

from project.resources.devices import DeviceManager, DeviceList


api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# device related resources
api.add_resource(DeviceManager, "/createDevice/")
api.add_resource(DeviceList, "/<string:version>/listDevices/<string:type>")
