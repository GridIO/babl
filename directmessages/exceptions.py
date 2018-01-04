from rest_framework.exceptions import APIException


class MustHaveRecipient(APIException):
    status_code = 400
    default_detail = '`recipient` must be a selected as a parameter .'
    default_code = 'must_have_recipient'

class RecipientCantBeSelf(APIException):
    status_code = 400
    default_detail = 'Message recipient cannot be self. Please pick a different user.'
    default_code = 'recipient_cant_be_self'

class ContentMustBeSpecified(APIException):
    status_code = 400
    default_detail = 'Message content must be specified as either text or image.'
    default_code = 'content_must_be_specified'

class ContentCanOnlyBeSingleMedium(APIException):
    status_code = 400
    default_detail = 'Message content can only be text or image, not both.'
    default_code = 'content_can_only_be_single_medium'

class ContentMustMatchIndicatedType(APIException):
    status_code = 400
    default_detail = 'Supplied content and indicated type must match.'
    default_code = 'content_must_math_indicated_type'
