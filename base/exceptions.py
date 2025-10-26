from rest_framework.exceptions import APIException

class ExternalAPIUnavailable(APIException):
    def __init__(self, api_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_name = api_name
