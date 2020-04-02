import pytest

from fields import (
    CharField,
    ArgumentsField,
    EmailField,
    PhoneField,
    DateField,
    BirthDayField,
    GenderField,
    ClientIDsField,
)

from exceptions import ValidationError


@pytest.mark.parametrize(
    'required, nullable, value',
    [
        (False, True, 'string'),
        (False, True, ''),
        (False, True, None),
        (True, False, 'string'),
        (False, False, 'string'),
        (True, True, 'string'),
    ]
)
def test_charfield_valid(required, nullable, value):
    field = CharField(required, nullable)
    assert not field.validate(value)


@pytest.mark.parametrize(
    'required, nullable, value, ex_mes',
    [
        (False, False, ['string'], 'Field is not a string'),
        (False, False, [1, 2], 'Field is not a string'),
        (False, False, {'key': 'value'}, 'Field is not a string'),
        (False, True, False, 'Field is not a string'),
        (False, False, True, 'Field is not a string'),
        (False, False, 1, 'Field is not a string'),
        (False, False, 1.0, 'Field is not a string'),
        (True, False, None, 'Field is required'),
        (True, False, '', 'Field cannot be empty'),
    ]
)
def test_charfield_not_valid(required, nullable, value, ex_mes):
    field = CharField(required, nullable)
    with pytest.raises(ValidationError) as e:
        field.validate(value)
    assert str(e.value) == ex_mes


@pytest.mark.parametrize(
    'required, nullable, value',
    [
        (False, True, {'key': 'value'}),
        (False, True, {}),
        (False, True, {}),
        (False, True, None),
        (True, False, {'key': 'value'}),
        (False, False, {'key': 'value'}),
        (True, True, {'key': 'value'}),
    ]
)
def test_argumentsfield_valid(required, nullable, value):
    field = ArgumentsField(required, nullable)
    assert not field.validate(value)


@pytest.mark.parametrize(
    'required, nullable, value, ex_mes',
    [
        (False, False, [{'key': 'value'}], 'Field is not a dict'),
        (False, False, [1, 2], 'Field is not a dict'),
        (False, False, 'string', 'Field is not a dict'),
        (False, False, 1, 'Field is not a dict'),
        (False, False, True, 'Field is not a dict'),
        (False, True, False, 'Field is not a dict'),
        (True, False, None, 'Field is required'),
        (True, False, {}, 'Field cannot be empty'),
    ]
)
def test_argumentsfield_not_valid(required, nullable, value, ex_mes):
    field = ArgumentsField(required, nullable)
    with pytest.raises(ValidationError) as e:
        field.validate(value)
    assert str(e.value) == ex_mes


@pytest.mark.parametrize(
    'required, nullable, value',
    [
        (False, True, 'mail@dom.com'),
        (True, False, 'mail@dom.com'),
        (False, False, 'mail@dom.com'),
        (True, True, 'mail@dom.com'),
        (False, True, None),
        (False, True, ''),
    ]
)
def test_emailsfield_valid(required, nullable, value):
    field = EmailField(required, nullable)
    assert not field.validate(value)


@pytest.mark.parametrize(
    'required, nullable, value, ex_mes',
    [
        (False, False, ['string'], 'Field is not a string'),
        (False, False, [1, 2], 'Field is not a string'),
        (False, False, {'key': 'value'}, 'Field is not a string'),
        (False, False, True, 'Field is not a string'),
        (False, True, False, 'Field is not a string'),
        (False, False, 1, 'Field is not a string'),
        (False, False, 1.0, 'Field is not a string'),
        (False, False, 'string', 'No @ in email'),
        (True, False, None, 'Field is required'),
        (True, False, '', 'Field cannot be empty'),
    ]
)
def test_emailfield_not_valid(required, nullable, value, ex_mes):
    field = EmailField(required, nullable)
    with pytest.raises(ValidationError) as e:
        field.validate(value)
    assert str(e.value) == ex_mes


@pytest.mark.parametrize(
    'required, nullable, value',
    [
        (False, True, None),
        (False, True, ''),
        (True, False, '71234567891'),
        (True, False, 71234567891),
        (False, False, '71234567891'),
        (False, False, 71234567891),
        (True, True, '71234567891'),
        (True, True, 71234567891)
    ]
)
def test_phonesfield_valid(required, nullable, value):
    field = PhoneField(required, nullable)
    assert not field.validate(value)


@pytest.mark.parametrize(
    'required, nullable, value, ex_mes',
    [
        (False, False, ['string'], 'Phone must be a string or number'),
        (False, False, [1, 2], 'Phone must be a string or number'),
        (False, False, {'key': 'value'}, 'Phone must be a string or number'),
        (False, False, True, 'Phone must be a string or number'),
        (False, True, False, 'Phone must be a string or number'),
        (False, False, 71234567, 'Phone length must be 11'),
        (False, False, '712345671234', 'Phone length must be 11'),
        (False, False, '12345678901', 'Phone must start with 7'),
        (False, False, 12345678901, 'Phone must start with 7'),
        (False, False, 1.0, 'Phone must be a string or number'),
        (True, False, None, 'Field is required'),
        (True, False, '', 'Field cannot be empty'),
    ]
)
def test_phonefield_not_valid(required, nullable, value, ex_mes):
    field = PhoneField(required, nullable)
    with pytest.raises(ValidationError) as e:
        field.validate(value)
    assert str(e.value) == ex_mes


@pytest.mark.parametrize(
    'required, nullable, value',
    [
        (False, True, None),
        (False, True, ''),
        (False, False, '09.08.2015'),
        (True, False, '09.08.2015'),
        (True, True, '09.08.2015'),
        (False, True, '09.08.2015'),
    ]
)
def test_datefield_valid(required, nullable, value):
    field = DateField(required, nullable)
    assert not field.validate(value)


@pytest.mark.parametrize(
    'required, nullable, value, ex_mes',
    [
        (False, False, '12.09.19', 'Incorrect date format, DD.MM.YYYY expected'),
        (False, False, '2009.12.04', 'Incorrect date format, DD.MM.YYYY expected'),
        (False, False, '15/03/2018', 'Incorrect date format, DD.MM.YYYY expected'),
        (False, False, '15:03:2018', 'Incorrect date format, DD.MM.YYYY expected'),
        (False, False, '15032018', 'Incorrect date format, DD.MM.YYYY expected'),
        (True, False, None, 'Field is required'),
        (True, False, '', 'Field cannot be empty'),
    ]
)
def test_datefield_not_valid(required, nullable, value, ex_mes):
    field = DateField(required, nullable)
    with pytest.raises(ValidationError) as e:
        field.validate(value)
    assert str(e.value) == ex_mes


@pytest.mark.parametrize(
    'required, nullable, value',
    [
        (False, True, None),
        (False, True, ''),
        (False, False, '09.08.2015'),
        (True, False, '09.08.2015'),
        (True, True, '09.08.2015'),
        (False, True, '09.08.2015'),
    ]
)
def test_birthdayfield_valid(required, nullable, value):
    field = BirthDayField(required, nullable)
    assert not field.validate(value)


@pytest.mark.parametrize(
    'required, nullable, value, ex_mes',
    [
        (False, False, '12.09.19', 'Incorrect date format, DD.MM.YYYY expected'),
        (False, False, '2009.12.04', 'Incorrect date format, DD.MM.YYYY expected'),
        (False, False, '15/03/2018', 'Incorrect date format, DD.MM.YYYY expected'),
        (False, False, '15:03:2018', 'Incorrect date format, DD.MM.YYYY expected'),
        (False, False, '15032018', 'Incorrect date format, DD.MM.YYYY expected'),
        (False, False, '15.03.1901', 'The age cannot be greater than 70'),
        (False, False, '15.03.1949', 'The age cannot be greater than 70'),
        (True, False, None, 'Field is required'),
        (True, False, '', 'Field cannot be empty'),
    ]
)
def test_birthdayfield_not_valid(required, nullable, value, ex_mes):
    field = BirthDayField(required, nullable)
    with pytest.raises(ValidationError) as e:
        field.validate(value)
    assert str(e.value) == ex_mes


@pytest.mark.parametrize(
    'required, nullable, value',
    [
        (False, True, None),
        (False, True, ''),
        (False, False, 1),
        (True, False, 2),
        (True, True, 0),
        (False, True, 1),
    ]
)
def test_genderfield_valid(required, nullable, value):
    field = GenderField(required, nullable)
    assert not field.validate(value)


@pytest.mark.parametrize(
    'required, nullable, value, ex_mes',
    [
        (False, False, ['string'], 'Gender must contain only numbers'),
        (False, False, [1, 2], 'Gender must contain only numbers'),
        (False, False, {'key': 'value'}, 'Gender must contain only numbers'),
        (False, False, True, 'Gender must contain only numbers'),
        (False, True, False, 'Gender must contain only numbers'),
        (False, False, 3,
         'Gender must contain only numbers from: 0 - unknown, 1 - male, 2 - female'),
        (True, False, None, 'Field is required'),
    ]
)
def test_genderfield_not_valid(required, nullable, value, ex_mes):
    field = GenderField(required, nullable)
    with pytest.raises(ValidationError) as e:
        field.validate(value)
    assert str(e.value) == ex_mes


@pytest.mark.parametrize(
    'required, nullable, value',
    [
        (False, True, None),
        (False, True, ''),
        (False, False, [1, 2]),
        (True, False, [1]),
        (True, True, [0]),
        (False, True, [3, 2, 1]),
    ]
)
def test_clientidsfield_valid(required, nullable, value):
    field = ClientIDsField(required, nullable)
    assert not field.validate(value)


@pytest.mark.parametrize(
    'required, nullable, value, ex_mes',
    [
        (False, False, ['string'], 'Client ids must be a list of integers'),
        (False, False, [{'key': 'value'}], 'Client ids must be a list of integers'),
        (False, False, 1, 'Client ids must be a list of integers'),
        (False, False, 1.0, 'Client ids must be a list of integers'),
        (False, False, {'key': 'value'}, 'Client ids must be a list of integers'),
        (False, False, True, 'Client ids must be a list of integers'),
        (False, True, False, 'Client ids must be a list of integers'),
        (True, False, None, 'Field is required'),
        (True, False, [], 'Field cannot be empty'),
    ]
)
def test_clientidsfield_not_valid(required, nullable, value, ex_mes):
    field = ClientIDsField(required, nullable)
    with pytest.raises(ValidationError) as e:
        field.validate(value)
    assert str(e.value) == ex_mes
