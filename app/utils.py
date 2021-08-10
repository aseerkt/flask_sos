from re import match
from flask_login import current_user


def is_email(email):
    return match(r"[^@]+@[^@]+\.[^@]+", email)


def format_url(url: str) -> str:
    if 'postgres://' not in url:
        return url
    else:
        return url.replace('postgres://', 'postgresql://')


def get_location_url(latitude: float, longitude: float) -> str:
    return f'https://www.google.com/maps/@{latitude},{longitude},20z'
