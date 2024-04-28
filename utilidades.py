from validate_email import validate_email
import re
from datetime import datetime

def email_valido(email):
    return validate_email(email)


def pass_valido(clave):
    return re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[^\W]{5,40}', clave)

# will return a date as a string in format 'Month Day, Year'
def format_datetime(date) -> str:
    datetime_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return datetime_object.strftime('%B %d, %Y')


def format_comment_datetime(date) -> str:
    try:
        datetime_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        datetime_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    return datetime_object.strftime('%B %d, %Y')