from ..users.error import Error

def trip_form(data):
    errors = []
    if 'destination' in data and 'description' in data and 'start_date' in data and 'end_date' in data:
        valid, msg = destination(data['destination'])
        if not valid:
            errors.append(Error('destination', msg))
        # valid, msg = description(data['description'])
        # if not valid:
        #     errors.append(Error('description', msg))
        valid, msg = valid_date(data['start_date'])
        if not valid:
            errors.append(Error('start_date', msg))
        valid, msg = valid_date(data['end_date'])
        if not valid:
            errors.append(Error('end_date', msg))
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

def valid_date(val):
    if val:
        #TODO validate it is actually a date
        return True, None
    else:
        return False, 'Please specify a date in MM/DD/YYYY format'

def start_less_than_end(val1, val2):
    if val1<=val2:
        #TODO validate it is actually a date
        return True, None
    else:
        return False, 'Please specify a start date before the end date'


