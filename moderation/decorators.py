

def is_moderator(user):
    # Checks whether the user is a moderator
    try:
        return user.is_moderator
    except AttributeError:
        return False
