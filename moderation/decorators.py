# Decorators used to allow or deny access to certain views


def is_moderator(user):
    # Checks whether the user is a moderator
    try:
        return user.is_moderator
    except:
        return False
