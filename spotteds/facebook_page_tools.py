import facebook
from django.conf import settings


def page_graph():
    """Page Graph.

    return graph object from the page token
    """
    graph = facebook.GraphAPI(settings.FACEBOOK_PAGE_TOKEN)
    return graph
