from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ProhibitNullCharactersValidator:
    """Validate that the string doesn't contain the null character."""
    message = _('Null characters are not allowed.')
    code = 'null_characters_not_allowed'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if '\x00' in str(value):
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and self.message == other.message and
            self.code == other.code
        )
