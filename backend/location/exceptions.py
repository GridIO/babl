from rest_framework.exceptions import APIException


class LocationUnavailable(APIException):
    status_code = 404
    default_detail = 'Location not found. Please refresh your app.'
    default_code = 'location_not_found'
