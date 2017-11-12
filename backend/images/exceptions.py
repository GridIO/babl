from rest_framework.exceptions import APIException


class TooManyImages(APIException):
    status_code = 401
    default_detail = "You may only have 6 profile pictures at a time."
    default_code = 'profile_pic_max_exceeded'


class DuplicateImage(APIException):
    status_code = 400
    default_detail = "You cannot submit the same image twice."
    default_code = 'duplicate_image'


class ImageNotAvailable(APIException):
    status_code = 400
    default_detail = "Image being referenced is not available."
    default_code = 'image_not_available'


class NextImageCannotBeSelf(APIException):
    status_code = 400
    default_detail = "An image's next image cannot be itself."
    default_code = "next_image_invalid"
