import re


def verify_email_format(email):
    check = re.match('(.*)@sun-asterisk.com', email)
    if check:
        return True
    return False
