from re import match


def is_email(email):
    return match(r"[^@]+@[^@]+\.[^@]+", email)
