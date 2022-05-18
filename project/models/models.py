class Device:

    @staticmethod
    def get_schema():
        """
        method to get device schema
        """
        schema = {
            "type": "object",
            "required": ["mac_address", "ip_address", "hostname"]
        }
        props = schema["properties"] = {}

        props["ip_address"] = {
            "type": "string",
            "format": "ip-address"
        }

        props["hostname"] = {
            "description": "Host name",
            "type": "string"
        }
        return schema
