import datetime

from utils.exceptions import BadValueError
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

    def _validate(self, value):
        if value is None and not self.nullable:
            raise BadValueError('Field cannot be null')
        if not value and self.required:
            raise BadValueError('Field is required')


class CharField(Field):
    def _validate(self, value):
        if not isinstance(value, str):
            raise BadValueError('Field is not a string')
        super()._validate(value)


class ArgumentsField(Field):
    def _validate(self, value):
        if not isinstance(value, dict):
            raise BadValueError('Field is not a dict')
        super()._validate(value)


class EmailField(CharField):
    def _validate(self, value):
        super()._validate(value)
        if not '@' in value:
            raise BadValueError('No @ in email')


class PhoneField(Field):
    number_length = 11

    def _validate(self, value):
        if not isinstance(value, (str, int)):
            raise BadValueError('Phone must be a string or number')
        super()._validate(value)
        if len(str(value)) != self.number_length:
            raise BadValueError(f'Phone length must be {self.number_length}')
        if not str(value).startswith('7'):
            raise BadValueError('Phone must start with 7')


class DateField(Field):
    def _validate(self, value):
        super()._validate(value)
        try:
            datetime.datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise BadValueError('Incorrect date format, DD.MM.YYYY expected')


class BirthDayField(DateField):
    def _validate(self, value):
        super()._validate(value)
        bdate = datetime.datetime.strptime(value, '%d.%m.%Y')
        if datetime.datetime.now().year - bdate.year > 70:
            raise BadValueError('The age cannot be greater than 70')


class GenderField(Field):
    def _validate(self, value):
        super()._validate(value)
        if not isinstance(value, int):
            raise BadValueError('Gender must contain only numbers')
        if value not in GENDERS:
            raise BadValueError(f'Gender must contain only numbers from: {prettify_dict(GENDERS)}')


class ClientIDsField(Field):
    def _validate(self, value):
        super()._validate(value)
        if not isinstance(value, list) and not all(isinstance(x, int) for x in value):
            raise BadValueError('Client ids must be a list of integers')