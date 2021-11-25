from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details
from django.utils.translation import gettext as _


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad Request')
    default_code = 'ERR_BAD_REQUEST'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)


class ValidationError404(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Bad Request')
    default_code = 'ERR_BAD_REQUEST'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)