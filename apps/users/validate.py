# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from .error import Error

def registration_form(data):
    errors = []
    if 'first_name' in data and 'last_name' in data and 'email' in data and 'password' in data and 'c_password' in data:
        valid, msg = first_name(data['first_name'])
        if not valid:
            errors.append(Error('first_name', msg))
        valid, msg = last_name(data['last_name'])
        if not valid:
            errors.append(Error('last_name', msg))
        valid, msg = email(data['email'])
        if not valid:
            errors.append(Error('email', msg))
        valid, msg = password(data['password'])
        if not valid:
            errors.append(Error('password', msg))
        valid, msg = passwords_match(
            data['password'], data['c_password'])
        if not valid:
            errors.append(Error('password', msg))
        # if all the fields look good make sure the user doesnt already exist
    else:
        errors.append(
            Error('form', 'Something went wrong please try to submit the form again'))
    if errors:
        return (False, errors)
    else:
        return (True, data)

def login_form(data):
    errors = []
    if 'email' in data and 'password' in data:
        valid, msg = email(data['email'])
        if not valid:
            errors.append(Error('email', msg))    
        valid, msg = password(data['password'])
        if not valid:
            errors.append(Error('password', msg))
    else:
        errors.append(
            Error('form', 'Something went wrong please try to submit the form again'))
    if errors:
        return (False, errors)
    else:
        return (True, data)

def email(val):
    pattern = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
    if pattern.match(val):
        return True, None
    else:
        # consider putting my error messages here????
        return False, 'email is not a valid email'


def first_name(val):
    # pattern = re.compile(r'([a-z]{2,})', re.UNICODE | re.IGNORECASE)
    # TODO: this condition doesn't allow accented characters need to fix
    if len(val) >= 2 and val.isalpha():
        return True, None
    else:
        return False, 'first name must be at least 2 characters long and alpha only'


def last_name(val):
    # TODO: this condition doesn't allow accented characters need to fix
    if len(val) >= 2 and val.isalpha():
        return True, None
    else:
        return False, 'last name must be at least 2 characters long and alpha only'

def password(val):
    if len(val) >= 8:
        return True, None
    else:
        return False, 'pasword must be at least 8 characters'


def passwords_match(val1, val2):
    if val1 == val2:
        return True, None
    else:
        return False, 'pasword must match the confirmation password'
