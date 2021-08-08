from re import match


def is_email(email):
    return match(r"[^@]+@[^@]+\.[^@]+", email)


def format_url(url: string) -> string:
    if 'postgres://' not in url:
        return url
    else:
        return url.replace('postgres://', 'postgresql://')
