from django.utils import timezone, dateparse
from ..users.error import Error
from dateutil import parser
from datetime import datetime


def trip_form(data):
    errors = []
    if 'destination' in data and 'description' in data and 'start_date' in data and 'end_date' in data:
        valid, msg = destination(data['destination'])
        if not valid:
            errors.append(Error('destination', msg))
        valid, msg = description(data['description'])
        if not valid:
            errors.append(Error('description', msg))
        start_valid, msg = valid_date(data['start_date'])
        if not start_valid:
            errors.append(Error('start_date', 'Start date - ' + msg))
        end_valid, msg = valid_date(data['end_date'])
        if not end_valid:
            errors.append(Error('end_date', 'End date - ' + msg))
        if start_valid and end_valid:
            valid, msg = start_less_than_end(data['start_date'], data['end_date'])
            if not valid:
                errors.append(Error('start_date, end_date', msg))
        # if all the fields look good make sure the user doesnt already exist
    else:
        errors.append(
            Error('form', 'Something went wrong please try to submit the form again'))
    if errors:
        return (False, errors)
    else:
        return (True, data)

def destination(val):
    if len(val) >= 2:
        return True, None
    else:
        return False, 'destination must be at least 2 characters'

def description(val):
    if len(val) > 0:
        return True, None
    else:
        return False, 'description must be entered'

def valid_date(val):
    try:
        print val
        date = dateparse.parse_date(val)        
        if timezone.localdate() <= date:
            print 'valid date'
            return True, None
        else:
            return False, 'date must be in the future'
    except:
        return False, 'Please specify a date in MM/DD/YYYY format'


def start_less_than_end(val1, val2):
    try:
        date1 = dateparse.parse_date(val1)
        date2 = dateparse.parse_date(val2)
        if date1 < date2:
            return True, None
        else:
            return False, 'Please specify a start date before the end date'
    except:
        return False, 'Please specify a date in MM/DD/YYYY format'
  

