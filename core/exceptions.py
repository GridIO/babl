from rest_framework.exceptions import APIException


class UserUnavailable(APIException):
    status_code = 404
    default_detail = 'User not found. Please provide a valid id.'
    default_code = 'user_not_found'