import re

from django.core.exceptions import ValidationError


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'\d', password):
            raise ValidationError(
                'The password must contain at least 1 digit, 0-9.',
                code='password_no_number',
            )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[A-Z]', password):
            raise ValidationError(
                'The password must contain at least 1 uppercase letter, A-Z.',
                code='password_no_upper',
            )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                'The password must contain at least 1 special character: ' +
                '()[]{}|\\`~!@#$%^&*_-+=;:\'",<>./?',
                code='password_no_symbol',
            )
