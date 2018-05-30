from functools import wraps
import hmac

from django.conf import settings
from django.core.exceptions import PermissionDenied


def messenger_enabled(view_func):
    """
    Decorator for views that checks if the use of
    the messenger chatbot is enabled.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if settings.FACEBOOK_USE_CHATBOT:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator(view_func)


def messenger_secure(view_func):
    """
    Decorator that verifies that the request came from facebook
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            signature = request.META.get('HTTP_X_HUB_SIGNATURE', 'Not Valid').split('sha1=')[1]
            digest = hmac.new(settings.FACEBOOK_SECRET.encode(), request.body, 'sha1').hexdigest()
            if hmac.compare_digest(signature, digest):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator(view_func)
