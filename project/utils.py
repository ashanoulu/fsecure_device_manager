from xml.dom import minidom
from flask import abort


def create_error_message(status_code, error, message=None):
    """
    Method to create error message
    Return
        - Error object
    """
    error_message = {
        'Code': status_code,
        'Error': error,
        'Message': message
    }
    return abort(status_code, error_message)


def make_xml(data):
    root = minidom.Document()

    # creat root element
    xml = root.createElement('root')
    root.appendChild(xml)

    for device in data:
        # create child element
        device_child = root.createElement('device')

        # insert user data into element
        device_child.setAttribute('ip_address', device['ip_address'])
        device_child.setAttribute('mac_address', device['mac_address'])
        device_child.setAttribute('hostname', device['hostname'])
        xml.appendChild(device_child)

    return root.toprettyxml(indent="\t")