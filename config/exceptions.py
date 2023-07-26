from rest_framework.exceptions import APIException


class JwtException(APIException):
    status_code = 401
    default_detail = 'NO ACCESS TOKEN'


class NoContentException(APIException):
    status_code = 204
    default_detail = 'No Content'