import datetime

from exceptions import ValidationError
from utils import prettify_dict
from constants import GENDERS


__all__ = [
    'Field',
    'CharField',
    'ArgumentsField',
    'EmailField',
    'PhoneField',
    'DateField',
    'BirthDayField',
    'GenderField',
    'ClientIDsField',
]


class Field:
    def __init__(self, required=False, nullable=False):
        self.required = required
        self.nullable = nullable

    def validate(self, value):
        if value is None and not self.nullable:
            raise ValidationError('Field cannot be null')
        if not value and self.required:
            raise ValidationError('Field is required')


class CharField(Field):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValidationError('Field is not a string')
        super().validate(value)


class ArgumentsField(Field):
    def validate(self, value):
        if not isinstance(value, dict):
            raise ValidationError('Field is not a dict')
        super().validate(value)


class EmailField(CharField):
    def validate(self, value):
        super().validate(value)
        if not '@' in value:
            raise ValidationError('No @ in email')


class PhoneField(Field):
    number_length = 11

    def validate(self, value):
        if not isinstance(value, (str, int)):
            raise ValidationError('Phone must be a string or number')
        super().validate(value)
        if len(str(value)) != self.number_length:
            raise ValidationError(f'Phone length must be {self.number_length}')
        if not str(value).startswith('7'):
            raise ValidationError('Phone must start with 7')


class DateField(Field):
    def validate(self, value):
        super().validate(value)
        try:
            datetime.datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValidationError('Incorrect date format, DD.MM.YYYY expected')


class BirthDayField(DateField):
    def validate(self, value):
        super().validate(value)
        bdate = datetime.datetime.strptime(value, '%d.%m.%Y')
        if datetime.datetime.now().year - bdate.year > 70:
            raise ValidationError('The age cannot be greater than 70')


class GenderField(Field):
    def validate(self, value):
        super().validate(value)
        if not isinstance(value, int):
            raise ValidationError('Gender must contain only numbers')
        if value not in GENDERS:
            raise ValidationError(f'Gender must contain only numbers from: {prettify_dict(GENDERS)}')


class ClientIDsField(Field):
    def validate(self, value):
        super().validate(value)
        if not isinstance(value, list) and not all(isinstance(x, int) for x in value):
            raise ValidationError('Client ids must be a list of integers')