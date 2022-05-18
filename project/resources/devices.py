import re
import ipaddress

from project import cache
from flask import request, jsonify, make_response
from flask_restful import Resource
from project.utils import create_error_message, make_xml
from jsonschema import validate, ValidationError
from project.models.models import Device


class DeviceManager(Resource):

    @classmethod
    @cache.cached(timeout=50)
    def post(cls):

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Device.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        request_data = request.get_json()

        if re.match("[0-9A-F]{2}([-:]?)[0-9A-F]{2}(\\1[0-9A-F]{2}){4}$", request_data['mac_address'].upper()):

            try:
                ipaddress.ip_address(request_data['ip_address'])
            except ValueError:
                print("IP address is not valid")

            device_list: list = []
            if cache.get('devices') is not None:
                device_list:list = cache.get('devices')
            device_list.append({'mac_address': request_data['mac_address'],
                                                    'ip_address': request_data['ip_address'],
                                                    'hostname': request_data['hostname']})
            cache.add('devices', device_list)
            return jsonify({'message': 'Device added successfully!'})
        else:
            return create_error_message(
                400, "Error occurred while adding device!",
                "Error occurred while adding device!"
            )


class DeviceList(Resource):

    @classmethod
    @cache.cached(timeout=50)
    def get(cls, version, type):
        devices = cache.get('devices')

        if version == 'v1':
            v1_device_list = []
            for device in devices:
                v1_device_list.append({'mac_address': device['mac_address'], 'ip_address': device['ip_address']})
            return jsonify(v1_device_list)
        elif version == 'v2':
            if type == 'XML':
                response = make_response(make_xml(devices), 200)
                response.headers["Content-Type"] = "application/xml"
                return response
            else:
                return jsonify(devices)

        return jsonify('Version not found, please check again')

