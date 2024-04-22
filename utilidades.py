from validate_email import validate_email
import re


def email_valido(email):
    return validate_email(email)


def pass_valido(clave):
    return re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[^\W]{5,40}', clave)
